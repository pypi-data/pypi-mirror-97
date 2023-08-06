import logging
import socket
import time
from enum import Enum

from getmac import get_mac_address
from zeroconf import Error as ZeroconfError
from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceInfo,
    ServiceStateChange,
    current_time_millis,
)

from boschshcpy.exceptions import (
    SHCAuthenticationError,
    SHCConnectionError,
    SHCmDNSError,
)

logger = logging.getLogger("boschshcpy")


class SHCListener:
    """SHC Listener for Zeroconf browser updates."""

    def __init__(self, zeroconf, callback) -> None:
        """Initialize SHC Listener."""
        self.shc_services = {}
        self.waiting = True

        ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[self.service_update])
        current_millis = current_time_millis()
        while (
            self.waiting and current_time_millis() - current_millis < 10000
        ):  # Give zeroconf some time to respond
            time.sleep(0.1)
        callback(self.shc_services)

    def service_update(self, zeroconf, service_type, name, state_change):
        """Service state changed."""

        if state_change != ServiceStateChange.Added:
            return

        try:
            service_info = zeroconf.get_service_info(service_type, name)
        except ZeroconfError:
            logger.exception("Failed to get info for device %s", name)
            return

        if service_info is not None:
            if service_info.name.startswith("Bosch SHC"):
                self.waiting = False
            self.shc_services[name] = service_info

        return


class SHCInformation:
    class UpdateState(Enum):
        NO_UPDATE_AVAILABLE = "NO_UPDATE_AVAILABLE"
        DOWNLOADING = "DOWNLOADING"
        UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
        UPDATE_AVAILABLE = "UPDATE_AVAILABLE"

    def __init__(self, api, zeroconf=None):
        self._api = api
        self._unique_id = None
        self._name = None
        self._pub_info = self._api.get_public_information()
        if self._pub_info == None:
            raise SHCAuthenticationError

        self.get_unique_id(zeroconf)

    @property
    def version(self):
        return self._pub_info["softwareUpdateState"]["swInstalledVersion"]

    @property
    def updateState(self) -> UpdateState:
        return self.UpdateState(self._pub_info["softwareUpdateState"]["swUpdateState"])

    @property
    def shcIpAddress(self):
        return self._pub_info["shcIpAddress"]

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    def filter(self, service_info: ServiceInfo):
        mac_address = None
        name = None

        try:
            host_ip = socket.gethostbyname(self.shcIpAddress)
        except Exception as e:
            raise SHCConnectionError

        for info in service_info.values():
            if "Bosch SHC" in info.name:
                if host_ip in info.parsed_addresses(IPVersion.V4Only):
                    mac_address = info.name[
                        info.name.find("[") + 1 : info.name.find("]")
                    ]
                    server_pos = info.server.find(".local.")
                    if server_pos > -1:
                        name = info.server[:server_pos]
        if mac_address is None or name is None:
            raise SHCmDNSError
        self._unique_id = format_mac(mac_address)
        self._name = name

    def get_mac(self, host):
        """Get the mac address of the given host."""

    def get_unique_id(self, zeroconf):
        if zeroconf is not None:
            self._listener = SHCListener(zeroconf, self.filter)
        else:
            host = self.shcIpAddress
            try:
                mac_address = get_mac_address(ip=host)
                if not mac_address:
                    mac_address = get_mac_address(hostname=host)
            except Exception as err:  # pylint: disable=broad-except
                logger.exception("Unable to get mac address: %s", err)
                mac_address = None
            if mac_address is not None:
                self._unique_id = format_mac(mac_address)
            else:
                self._unique_id = host
                logger.warning(
                    "Cannot obtain unique id, using IP address '%s' instead. Please make sure the IP stays the same!",
                    host,
                )
            self._name = host

    def summary(self):
        print(f"Information:")
        print(f"  shcIpAddress       : {self.shcIpAddress}")
        print(f"  SW-Version         : {self.version}")
        print(f"  updateState        : {self.updateState.name}")
        print(f"  uniqueId           : {self.unique_id}")
        print(f"  name               : {self.name}")


def format_mac(mac: str) -> str:
    """
    Format the mac address string.
    Helper function from homeassistant.helpers.device_registry.py
    """
    to_test = mac

    if len(to_test) == 17 and to_test.count("-") == 5:
        return to_test.lower()

    if len(to_test) == 17 and to_test.count(":") == 5:
        to_test = to_test.replace(":", "")
    elif len(to_test) == 14 and to_test.count(".") == 2:
        to_test = to_test.replace(".", "")

    if len(to_test) == 12:
        # no - included
        return "-".join(to_test.lower()[i : i + 2] for i in range(0, 12, 2))

    # Not sure how formatted, return original
    return mac

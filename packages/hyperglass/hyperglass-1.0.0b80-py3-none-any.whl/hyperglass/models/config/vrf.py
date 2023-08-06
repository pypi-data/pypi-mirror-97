"""Validate VRF configuration variables."""

# Standard Library
import re
from typing import Dict, List, Union, Optional
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

# Third Party
from pydantic import (
    Field,
    FilePath,
    StrictStr,
    StrictBool,
    PrivateAttr,
    conint,
    constr,
    validator,
    root_validator,
)
from typing_extensions import Literal

# Project
from hyperglass.log import log

# Local
from ..main import HyperglassModel, HyperglassModelExtra

ACLAction = constr(regex=r"permit|deny")
AddressFamily = Union[Literal[4], Literal[6]]


def find_vrf_id(values: Dict) -> str:
    """Generate (private) VRF ID."""

    def generate_id(name: str) -> str:
        scrubbed = re.sub(r"[^A-Za-z0-9\_\-\s]", "", name)
        return "_".join(scrubbed.split()).lower()

    display_name = values.get("display_name")

    if display_name is None:
        raise ValueError("display_name is required.")

    return generate_id(display_name)


class AccessList4(HyperglassModel):
    """Validation model for IPv4 access-lists."""

    network: IPv4Network = Field(
        "0.0.0.0/0",
        title="Network",
        description="IPv4 Network/Prefix that should be permitted or denied. ",
    )
    action: ACLAction = Field(
        "permit",
        title="Action",
        description="Permit or deny any networks contained within the prefix.",
    )
    ge: conint(ge=0, le=32) = Field(
        0,
        title="Greater Than or Equal To",
        description="Similar to `ge` in a Cisco prefix-list, the `ge` field defines the **bottom** threshold for prefix size. For example, a value of `24` would result in a query for `192.0.2.0/23` being denied, but a query for `192.0.2.0/32` would be permitted. If this field is set to a value smaller than the `network` field's prefix length, this field's value will be overwritten to the prefix length of the prefix in the `network` field.",
    )
    le: conint(ge=0, le=32) = Field(
        32,
        title="Less Than or Equal To",
        description="Similar to `le` in a Cisco prefix-list, the `le` field defines the **top** threshold for prefix size. For example, a value of `24` would result in a query for `192.0.2.0/23` being permitted, but a query for `192.0.2.0/32` would be denied.",
    )

    @validator("ge")
    def validate_model(cls, value, values):
        """Ensure ge is at least the size of the input prefix.

        Arguments:
            value {int} -- Initial ge value
            values {dict} -- Other post-validation fields

        Returns:
            {int} -- Validated ge value
        """
        net_len = values["network"].prefixlen
        if net_len > value:
            value = net_len
        return value


class AccessList6(HyperglassModel):
    """Validation model for IPv6 access-lists."""

    network: IPv6Network = Field(
        "::/0",
        title="Network",
        description="IPv6 Network/Prefix that should be permitted or denied. ",
    )
    action: ACLAction = Field(
        "permit",
        title="Action",
        description="Permit or deny any networks contained within the prefix.",
    )
    ge: conint(ge=0, le=128) = Field(
        0,
        title="Greater Than or Equal To",
        description="Similar to `ge` in a Cisco prefix-list, the `ge` field defines the **bottom** threshold for prefix size. For example, a value of `64` would result in a query for `2001:db8::/48` being denied, but a query for `2001:db8::1/128` would be permitted. If this field is set to a value smaller than the `network` field's prefix length, this field's value will be overwritten to the prefix length of the prefix in the `network` field.",
    )
    le: conint(ge=0, le=128) = Field(
        128,
        title="Less Than or Equal To",
        description="Similar to `le` in a Cisco prefix-list, the `le` field defines the **top** threshold for prefix size. For example, a value of `64` would result in a query for `2001:db8::/48` being permitted, but a query for `2001:db8::1/128` would be denied.",
    )

    @validator("ge")
    def validate_model(cls, value, values):
        """Ensure ge is at least the size of the input prefix.

        Arguments:
            value {int} -- Initial ge value
            values {dict} -- Other post-validation fields

        Returns:
            {int} -- Validated ge value
        """
        net_len = values["network"].prefixlen
        if net_len > value:
            value = net_len
        return value


class InfoConfigParams(HyperglassModelExtra):
    """Validation model for per-help params."""

    title: Optional[StrictStr]

    class Config:
        """Pydantic model configuration."""

        title = "Help Parameters"
        description = "Set dynamic or reusable values which may be used in the help/information content. Params my be access by using Python string formatting syntax, e.g. `{param_name}`. Any arbitrary values may be added."


class InfoConfig(HyperglassModel):
    """Validation model for help configuration."""

    enable: StrictBool = True
    file: Optional[FilePath]
    params: InfoConfigParams = InfoConfigParams()

    class Config:
        """Pydantic model configuration."""

        fields = {
            "enable": {
                "title": "Enable",
                "description": "Enable or disable the display of help/information content for this query type.",
            },
            "file": {
                "title": "File Name",
                "description": "Path to a valid text or Markdown file containing custom content.",
            },
        }


class Info(HyperglassModel):
    """Validation model for per-VRF, per-Command help."""

    bgp_aspath: InfoConfig = InfoConfig()
    bgp_community: InfoConfig = InfoConfig()
    bgp_route: InfoConfig = InfoConfig()
    ping: InfoConfig = InfoConfig()
    traceroute: InfoConfig = InfoConfig()

    class Config:
        """Pydantic model configuration."""

        title = "VRF Information"
        description = "Per-VRF help & information content."
        fields = {
            "bgp_aspath": {
                "title": "BGP AS Path",
                "description": "Show information about bgp_aspath queries when selected.",
            },
            "bgp_community": {
                "title": "BGP Community",
                "description": "Show information about bgp_community queries when selected.",
            },
            "bgp_route": {
                "title": "BGP Route",
                "description": "Show information about bgp_route queries when selected.",
            },
            "ping": {
                "title": "Ping",
                "description": "Show information about ping queries when selected.",
            },
            "traceroute": {
                "title": "Traceroute",
                "description": "Show information about traceroute queries when selected.",
            },
        }


class DeviceVrf4(HyperglassModelExtra):
    """Validation model for IPv4 AFI definitions."""

    source_address: IPv4Address
    access_list: List[AccessList4] = [AccessList4()]
    force_cidr: StrictBool = True


class DeviceVrf6(HyperglassModelExtra):
    """Validation model for IPv6 AFI definitions."""

    source_address: IPv6Address
    access_list: List[AccessList6] = [AccessList6()]
    force_cidr: StrictBool = True


class Vrf(HyperglassModel):
    """Validation model for per VRF/afi config in devices.yaml."""

    _id: StrictStr = PrivateAttr()
    name: StrictStr
    display_name: StrictStr
    info: Info = Info()
    ipv4: Optional[DeviceVrf4]
    ipv6: Optional[DeviceVrf6]
    default: StrictBool = False

    def __init__(self, **kwargs) -> None:
        """Set the VRF ID."""
        _id = find_vrf_id(kwargs)
        super().__init__(**kwargs)
        self._id = _id

    @root_validator
    def set_dynamic(cls, values: Dict) -> Dict:
        """Set dynamic attributes before VRF initialization."""

        if values["name"] == "default":
            log.warning(
                """You have set the VRF name to 'default'. This is no longer the way to
designate a VRF as the default (or global routing table) VRF. Instead,
add 'default: true' to the VRF definition.
"""
            )

        if values.get("default", False) is True:
            protocol4 = "ipv4_default"
            protocol6 = "ipv6_default"

        else:
            protocol4 = "ipv4_vpn"
            protocol6 = "ipv6_vpn"

        if values.get("ipv4") is not None:
            values["ipv4"].protocol = protocol4
            values["ipv4"].version = 4

        if values.get("ipv6") is not None:
            values["ipv6"].protocol = protocol6
            values["ipv6"].version = 6

        if values.get("default", False) and values.get("display_name") is None:
            values["display_name"] = "Global"

        return values

    def __getitem__(self, i: AddressFamily) -> Union[DeviceVrf4, DeviceVrf6]:
        """Access the VRF's AFI by IP protocol number."""
        if i not in (4, 6):
            raise AttributeError(f"Must be 4 or 6, got '{i}'")

        return getattr(self, f"ipv{i}")

    def __hash__(self) -> int:
        """Make VRF object hashable so the object can be deduplicated with set()."""
        return hash((self.name,))

    def __eq__(self, other: object) -> bool:
        """Make VRF object comparable so the object can be deduplicated with set()."""
        result = False
        if isinstance(other, HyperglassModel):
            result = self.name == other.name
        return result

    class Config:
        """Pydantic model configuration."""

        title = "VRF"
        description = "Per-VRF configuration."
        fields = {
            "name": {
                "title": "Name",
                "description": "VRF name as configured on the router/device.",
            },
            "display_name": {
                "title": "Display Name",
                "description": "Display name of VRF for use in the hyperglass UI. If none is specified, hyperglass will attempt to generate one.",
            },
        }

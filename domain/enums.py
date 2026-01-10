from enum import Enum


class DefaultAction(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"
    ANY = "any"

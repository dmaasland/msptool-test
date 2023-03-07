from enum import IntEnum, StrEnum


class HttpMethod(StrEnum):
    GET = "get"
    POST = "post"


class EntityType(IntEnum):
    ANY = 1000
    HQ = 1001
    DISTRIBUTOR = 1002
    DIVISION = 1003
    MSP_MANAGER = 1004
    MSP = 1005
    MANAGED_MSP = 1006
    MANAGED_BY_MSP = 1007

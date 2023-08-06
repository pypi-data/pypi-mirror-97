import enum


class Region(enum.Enum):
    MOSCOW = 1
    SPB = 2


class AdType(enum.Enum):
    FLAT_SALE = "flatsale"
    HOME_SALE = "suburbansale"
    FLAT_RENT = "flatrent"
    HOME_RENT = "suburbanrent"
    COMMERCIAL_SALE = "commercialsale"
    COMMERCIAL_RENT = "commercialrent"


class Room(enum.Enum):
    ROOM = 0
    ONE_ROOMED = 1
    TWO_ROOMED = 2
    THREE_ROOMED = 3
    FOUR_ROOMED = 4
    FIVE_ROOMED = 5
    SIX_ROOMED = 6
    FREE_LAYOUT = 7
    PART_FLAT = 8
    STUDIO = 9


class BuildingStatus(enum.Enum):
    NEW = 1
    OLD = 2


class ObjectType(enum.Enum):
    HOUSE = 1
    HOUSE_PART = 2
    AREA = 3
    TOWNHOUSE = 4


class Advertiser(enum.Enum):
    DEVELOPER = 1
    OWNER_AND_AGENT = 2

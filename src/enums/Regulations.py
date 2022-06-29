import enum

class Regulation(enum.Enum):
    NO_DATA = -1
    HIGHLY_REGULATED = 0
    MOSTLY_REGULATED = 1
    CONDITIONAL = 2
    MOSTLY_UNREGULATED = 3
    HIGHLY_UNREGULATED = 4
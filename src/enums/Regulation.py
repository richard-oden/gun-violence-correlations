import enum

class Regulation(enum.Enum):
    '''
    An enum representing how regulated a particular aspect of gun legislation is.
    Backing value is an int, which may be used to calulcate average regulation.
    '''
    NO_DATA = -1
    HIGHLY_REGULATED = 100
    MOSTLY_REGULATED = 75
    CONDITIONAL = 50
    MOSTLY_UNREGULATED = 25
    HIGHLY_UNREGULATED = 0
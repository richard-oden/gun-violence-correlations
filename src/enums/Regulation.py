import enum

class Regulation(enum.Enum):
    '''
    An enum representing how regulated a particular aspect of gun legislation is.
    Backing value is an int, which may be used to calulcate average regulation.
    '''
    NO_DATA = -1
    HIGHLY_REGULATED = 0
    MOSTLY_REGULATED = 1
    CONDITIONAL = 2
    MOSTLY_UNREGULATED = 3
    HIGHLY_UNREGULATED = 4
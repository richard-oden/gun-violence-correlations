import enum

class ColumnName(enum.Enum):
    '''
    Represents column names used by dataframes.
    '''
    COUNTRY = 'Country'
    GOOD_REASON = 'Good Reason Required'
    PERSONAL_PROTECTION = 'Personal Protection Permitted'
    LONG_GUNS = 'Long Guns Permitted'
    HANDGUNS = 'Handguns Permitted'
    SEMIAUTOMATIC = 'Semi-Automatic Permitted'
    FULLY_AUTOMATIC = 'Fully Automatic Permitted'
    OPEN_CARRY = 'Open Carry Permitted'
    CONCEALED_CARRY = 'Concealed Carry Permitted'
    FREE_OF_REGISTRATION = 'Free of Registration'
    DEATH_RATE = 'Death Rate by Firearm per 100k Citizens'
    OVERALL_REGULATION = 'Overall Regulation Score'

REGULATION_COLUMN_NAMES = [
    ColumnName.GOOD_REASON,
    ColumnName.PERSONAL_PROTECTION,
    ColumnName.LONG_GUNS,
    ColumnName.HANDGUNS,
    ColumnName.SEMIAUTOMATIC,
    ColumnName.FULLY_AUTOMATIC,
    ColumnName.OPEN_CARRY,
    ColumnName.CONCEALED_CARRY,
    ColumnName.FREE_OF_REGISTRATION
]
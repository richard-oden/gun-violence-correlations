import enum

class ColumnNames(enum.Enum):
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

regulation_column_names = [
    ColumnNames.GOOD_REASON,
    ColumnNames.PERSONAL_PROTECTION,
    ColumnNames.LONG_GUNS,
    ColumnNames.HANDGUNS,
    ColumnNames.SEMIAUTOMATIC,
    ColumnNames.FULLY_AUTOMATIC,
    ColumnNames.OPEN_CARRY,
    ColumnNames.CONCEALED_CARRY,
    ColumnNames.FREE_OF_REGISTRATION
]
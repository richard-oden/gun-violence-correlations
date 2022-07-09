import enum

class ColumnName(enum.Enum):
    '''
    Represents column names used by dataframes.
    '''
    COUNTRY = 'Country'
    GOOD_REASON = 'Good Reason Required (Score)'
    PERSONAL_PROTECTION = 'Personal Protection Permitted (Score)'
    LONG_GUNS = 'Long Guns Permitted (Score)'
    HANDGUNS = 'Handguns Permitted (Score)'
    SEMIAUTOMATIC = 'Semi-Automatic Permitted (Score)'
    FULLY_AUTOMATIC = 'Fully Automatic Permitted (Score)'
    OPEN_CARRY = 'Open Carry Permitted (Score)'
    CONCEALED_CARRY = 'Concealed Carry Permitted (Score)'
    FREE_OF_REGISTRATION = 'Free of Registration (Score)'
    GOOD_REASON_TEXT = 'Good Reason Required'
    PERSONAL_PROTECTION_TEXT = 'Personal Protection Permitted'
    LONG_GUNS_TEXT = 'Long Guns Permitted'
    HANDGUNS_TEXT = 'Handguns Permitted'
    SEMIAUTOMATIC_TEXT = 'Semi-Automatic Permitted'
    FULLY_AUTOMATIC_TEXT = 'Fully Automatic Permitted'
    OPEN_CARRY_TEXT = 'Open Carry Permitted'
    CONCEALED_CARRY_TEXT = 'Concealed Carry Permitted'
    FREE_OF_REGISTRATION_TEXT = 'Free of Registration'
    DEATH_RATE = 'Death Rate by Firearm per 100k Persons'
    CIVILIAN_FIREARMS = 'Estimate of Civilian Firearms per 100 Persons'
    MILITARY_FIREARMS = 'Estimate of Military Firearms per 100 Persons'
    POLICE_FIREARMS = 'Estimate of Law Enforcement Firearms per 100 Persons'
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

TEXT_COLUMN_NAMES = [
    ColumnName.GOOD_REASON_TEXT,
    ColumnName.PERSONAL_PROTECTION_TEXT,
    ColumnName.LONG_GUNS_TEXT,
    ColumnName.HANDGUNS_TEXT,
    ColumnName.SEMIAUTOMATIC_TEXT,
    ColumnName.FULLY_AUTOMATIC_TEXT,
    ColumnName.OPEN_CARRY_TEXT,
    ColumnName.CONCEALED_CARRY_TEXT,
    ColumnName.FREE_OF_REGISTRATION_TEXT
]
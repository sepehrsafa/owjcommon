from enum import Enum


class UserTypeChoices(str, Enum):
    AGENCY_SUPERUSER = "AGENCY_SUPERUSER"
    AGENCY_USER = "AGENCY_USER"
    BUSINESS_SUPERUSER = "BUSINESS_SUPERUSER"
    BUSINESS_USER = "BUSINESS_USER"
    REGULAR_USER = "REGULAR_USER"


class UserSet(Enum):
    AGENCY = [UserTypeChoices.AGENCY_SUPERUSER, UserTypeChoices.AGENCY_USER]
    BUSINESS = [UserTypeChoices.BUSINESS_SUPERUSER, UserTypeChoices.BUSINESS_USER]
    REGULAR = [UserTypeChoices.REGULAR_USER]
    AGENCY_AND_BUSINESS = [
        UserTypeChoices.AGENCY_SUPERUSER,
        UserTypeChoices.AGENCY_USER,
        UserTypeChoices.BUSINESS_SUPERUSER,
        UserTypeChoices.BUSINESS_USER,
    ]

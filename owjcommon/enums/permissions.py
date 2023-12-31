from enum import Enum
from .user_types import UserTypeChoices


class UserPermission(str, Enum):
    USER_ACCOUNT_CREATE = "USER_ACCOUNT:CREATE"
    USER_ACCOUNT_UPDATE = "USER_ACCOUNT:UPDATE"
    USER_ACCOUNT_DELETE = "USER_ACCOUNT:DELETE"
    USER_ACCOUNT_READ = "USER_ACCOUNT:READ"

    USER_GROUP_CREATE = "USER_GROUP:CREATE"
    USER_GROUP_UPDATE = "USER_GROUP:UPDATE"
    USER_GROUP_DELETE = "USER_GROUP:DELETE"
    USER_GROUP_READ = "USER_GROUP:READ"
    USER_GROUP_ADD_USER = "USER_GROUP:ADD_USER"
    USER_GROUP_REMOVE_USER = "USER_GROUP:REMOVE_USER"

    BUSINESS_ACCOUNT_CREATE = "BUSINESS_ACCOUNT:CREATE"
    BUSINESS_ACCOUNT_UPDATE = "BUSINESS_ACCOUNT:UPDATE"
    BUSINESS_ACCOUNT_DELETE = "BUSINESS_ACCOUNT:DELETE"
    BUSINESS_ACCOUNT_READ = "BUSINESS_ACCOUNT:READ"

    WALLET_CREATE = "WALLET:CREATE"
    WALLET_UPDATE = "WALLET:UPDATE"
    WALLET_DELETE = "WALLET:DELETE"
    WALLET_READ = "WALLET:READ"

    WALLET_TRANSACTION_CREATE = "WALLET_TRANSACTION:CREATE"
    WALLET_TRANSACTION_UPDATE = "WALLET_TRANSACTION:UPDATE"
    WALLET_TRANSACTION_DELETE = "WALLET_TRANSACTION:DELETE"
    WALLET_TRANSACTION_READ = "WALLET_TRANSACTION:READ"

    IPG_CREATE = "IPG:CREATE"
    IPG_UPDATE = "IPG:UPDATE"
    IPG_DELETE = "IPG:DELETE"
    IPG_READ = "IPG:READ"

    IPG_TRANSACTION_READ = "IPG_TRANSACTION:READ"

    AIRLINE_CREATE = "AIRLINE:CREATE"
    AIRLINE_UPDATE = "AIRLINE:UPDATE"
    AIRLINE_DELETE = "AIRLINE:DELETE"
    AIRLINE_READ = "AIRLINE:READ"

    CITY_CREATE = "CITY:CREATE"
    CITY_UPDATE = "CITY:UPDATE"
    CITY_DELETE = "CITY:DELETE"
    CITY_READ = "CITY:READ"

    AIRPORT_CREATE = "AIRPORT:CREATE"
    AIRPORT_UPDATE = "AIRPORT:UPDATE"
    AIRPORT_DELETE = "AIRPORT:DELETE"
    AIRPORT_READ = "AIRPORT:READ"


USER_TYPE_PERMISSIONS = {
    UserTypeChoices.REGULAR_USER: [e.value for e in UserPermission],
    UserTypeChoices.AGENCY_SUPERUSER: [e.value for e in UserPermission],
    UserTypeChoices.AGENCY_USER: [e.value for e in UserPermission],
}

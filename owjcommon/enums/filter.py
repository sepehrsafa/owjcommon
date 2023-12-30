from enum import Enum


class MatchType(str, Enum):
    EXACT = "exact"
    NOT_EXACT = "not_exact"
    LIKE = "like"
    NOT_LIKE = "not_like"


class LogicalOperation(str, Enum):
    AND = "and"
    OR = "or"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

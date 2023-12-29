import datetime
import re
from enum import Enum
from typing import Generic, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseConfig, BaseModel, Field, ValidationError, validator

from owjcommon.enums import LogicalOperation, MatchType
from owjcommon.exceptions import exception_codes
from owjcommon.validators import is_valid_phone_number


class Detail(BaseModel):
    loc: List[Union[str, int]] = Field(..., description="Location of the error")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ValidationErrorDetail(BaseModel):
    id: str = Field("E1001", description="Error ID")
    message: str = exception_codes["E1001"]
    detail: List[Detail]


class ValidationErrorResponse(BaseModel):
    success: bool = Field(False, description="Success flag")
    error: ValidationErrorDetail = Field(..., description="Error details")


class ErrorDetail(BaseModel):
    id: str = Field(..., description="Error ID")
    message: str = Field(..., description="Error message")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Success flag")
    error: ErrorDetail = Field(..., description="Error details")


class Response(BaseModel):
    success: bool = Field(True, description="Success flag")


class Password(BaseModel):
    password: str = Field(
        ...,
        description="Password, must be at least 8 characters long, contain at least one number, one uppercase letter and one lowercase letter",
    )

    @validator("password", pre=True, always=True)
    def validate_password(cls, value):
        # Check for minimum length
        if len(value) < 8:
            raise ValueError("Password too short")

        # Ensure password contains at least one number
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")

        # Ensure password contains at least one uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        # Ensure password contains at least one lowercase letter
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        return value


class PhoneNumber(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 format")

    @validator("phone_number", pre=True, always=True)
    def validate_phone_number(cls, value):
        if is_valid_phone_number(value):
            return value
        else:
            raise ValueError("Invalid phone number. It must be in E.164 format.")


class PaginatedResult(Response):
    total_pages: int = Field(..., description="Total number of pages")


class Filters(BaseModel):
    logical_op: LogicalOperation = Field(
        LogicalOperation.AND, description="Logical operation to apply to the filters"
    )
    match_type: MatchType = Field(
        MatchType.LIKE, description="Match type to apply to the filters"
    )


class OwjBaseModel(BaseModel):
    id: int = Field(..., description="Unique identifier")
    created_at: datetime.datetime = Field(..., description="Creation date")
    updated_at: datetime.datetime = Field(..., description="Last update date")

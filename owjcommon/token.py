from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError

from owjcommon.schemas import TokenData


async def validate_token(
    security_scopes, token, types=None, secret_key=None, algorithm=None
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_type = payload.get("token_type")
        if token_type != "access":
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    if types:
        if payload.get("type") not in types:
            raise credentials_exception

    return TokenData(**payload)

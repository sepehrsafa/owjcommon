from fastapi import Depends, Query


def pagination(
    offset: int = Query(0, alias="offset"), size: int = Query(10, alias="size")
) -> dict:
    return {"offset": offset, "size": size}

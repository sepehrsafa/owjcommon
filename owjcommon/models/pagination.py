from enum import Enum
from functools import reduce
from operator import and_, or_
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model

from owjcommon.enums import LogicalOperation, MatchType, SortOrder


def build_conditions(filters: Dict[str, Any]) -> List[Q]:
    conditions = []
    match_type = filters.get("match_type")
    for field, value in filters.items():
        if field not in ["match_type", "logical_op"] and value is not None:
            # check if value is boolean
            if isinstance(value, bool):
                if match_type in [MatchType.NOT_LIKE, MatchType.NOT_EXACT]:
                    conditions.append(~Q(**{field: value}))
                else:
                    conditions.append(Q(**{field: value}))
                continue

            if match_type in [MatchType.LIKE, MatchType.NOT_LIKE]:
                # check if type is enum, convert to string
                if isinstance(value, Enum):
                    value = value.value
                value = str(value)  # Convert value to string only for LIKE and NOT_LIKE
            if match_type == MatchType.LIKE:
                conditions.append(Q(**{f"{field}__contains": value}))
            elif match_type == MatchType.NOT_LIKE:
                conditions.append(~Q(**{f"{field}__contains": value}))
            elif match_type == MatchType.NOT_EXACT:
                conditions.append(~Q(**{field: value}))
            else:
                conditions.append(Q(**{field: value}))
    return conditions


async def get_paginated_results_with_filter(
    model: Type[Model],
    offset: int,
    size: int,
    user_filters: Optional[Union[Dict[str, Any], BaseModel]] = None,
    system_filters: Optional[Union[Dict[str, Any], BaseModel]] = None,
    prefetch_related: Optional[List[str]] = None,
    sort_order: Optional[SortOrder] = None,
    sort_field: Optional[str] = None,
) -> dict:
    query = model.all()

    if user_filters:
        if isinstance(user_filters, BaseModel):
            user_filters = user_filters.dict()
        user_conditions = build_conditions(user_filters)
        if user_conditions:
            query = query.filter(
                reduce(or_, user_conditions)
                if user_filters.get("logical_op") == LogicalOperation.OR
                else reduce(and_, user_conditions)
            )

    if system_filters:
        if isinstance(system_filters, BaseModel):
            system_filters = system_filters.dict()
        system_conditions = build_conditions(system_filters)
        if system_conditions:
            query = query.filter(reduce(and_, system_conditions))

    if prefetch_related:
        query = query.prefetch_related(*prefetch_related)

    if sort_order and sort_field:
        if sort_order == SortOrder.ASC:
            query = query.order_by(sort_field)
        else:
            query = query.order_by(f"-{sort_field}")

    total_items = await query.count()
    total_pages = (total_items - 1) // size + 1
    items = await query.offset(offset).limit(size)

    return {"total_items": total_items, "total_pages": total_pages, "items": items}


async def get_paginated_results(
    model: Type[Model], offset: int, size: int, prefetch_related=None
) -> dict:
    total_items = await model.all().count()
    total_pages = (total_items - 1) // size + 1
    if prefetch_related is None:
        items = await model.all().offset(offset).limit(size)
    else:
        items = (
            await model.all()
            .prefetch_related(*prefetch_related)
            .offset(offset)
            .limit(size)
        )

    return {"total_items": total_items, "total_pages": total_pages, "items": items}


async def get_paginated_data_results(data, offset: int, size: int) -> dict:
    total_items = len(data)
    total_pages = (total_items - 1) // size + 1

    # calculate offset and limit
    offset = offset * size
    limit = offset + size

    # check if offset is greater than total items
    if offset > total_items:
        offset = total_items

    # check if limit is greater than total items
    if limit > total_items:
        limit = total_items

    items = data[offset:limit]

    return {"total_items": total_items, "total_pages": total_pages, "items": items}

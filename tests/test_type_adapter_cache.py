from __future__ import annotations

import gc
import weakref
from types import GenericAlias
from typing import Any, Literal, cast

from openai import _models


def _dynamic_list_type(value: int) -> type[Any]:
    literal = cast(Any, Literal)[value]
    return cast(type[Any], GenericAlias(list, literal))


def _fill_dynamic_type_cache() -> None:
    for value in range(1, 514):
        dynamic_type = _dynamic_list_type(value)
        assert _models.validate_type(type_=dynamic_type, value=[value]) == [value]


def test_type_adapter_cache_evicts_old_dynamic_types() -> None:
    first_type = _dynamic_list_type(0)
    first_ref = weakref.ref(first_type)

    assert _models.validate_type(type_=first_type, value=[0]) == [0]
    del first_type
    gc.collect()
    assert first_ref() is not None

    _fill_dynamic_type_cache()
    gc.collect()
    assert first_ref() is None


def test_type_adapter_cache_reuses_common_types() -> None:
    first = _models.TypeAdapter(list[int])
    second = _models.TypeAdapter(list[int])

    assert first is second

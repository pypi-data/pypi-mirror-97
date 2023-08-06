from collections.abc import Sequence
from functools import singledispatch
from typing import Any, Type

import numpy  # type: ignore
import pandas  # type: ignore
import pyarrow  # type: ignore

from tktl.core.exceptions import UnsupportedInputTypeException
from tktl.core.loggers import LOG
from tktl.core.serializers import arrow
from tktl.core.serializers.base import ObjectSerializer


def deserialize_arrow(model_input: pyarrow.Table):
    cls_name = model_input.schema.metadata[b"CLS"]
    func = getattr(getattr(arrow, cls_name.decode("utf-8")), "deserialize")
    return func(model_input)


@singledispatch
def serialize_arrow(model_input) -> pyarrow.Table:
    return arrow.BinarySerializer.serialize(model_input)


@serialize_arrow.register(Sequence)
def _sequence(model_input):
    return _do_serialize_with_fallback(
        arrow.SequenceSerializer, model_input=model_input
    )


@serialize_arrow.register(dict)
def _dict(model_input):
    return _do_serialize_with_fallback(
        arrow.SequenceSerializer, model_input=model_input
    )


@serialize_arrow.register(numpy.ndarray)
def _ndarry(model_input):
    return _do_serialize_with_fallback(arrow.ArraySerializer, model_input=model_input)


@serialize_arrow.register(pandas.DataFrame)
def _df(model_input):
    return _do_serialize_with_fallback(
        arrow.DataFrameSerializer, model_input=model_input
    )


@serialize_arrow.register(pandas.Series)
def _series(model_input):
    return _do_serialize_with_fallback(arrow.SeriesSerializer, model_input=model_input)


def _do_serialize_with_fallback(
    serializer_cls: Type[ObjectSerializer], model_input: Any
):
    try:
        return serializer_cls.serialize(value=model_input)
    except UnsupportedInputTypeException:
        LOG.warning(
            "Invalid input supported, will use binary representation for object"
        )
    return arrow.BinarySerializer.serialize(model_input)

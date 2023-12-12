import operator
from collections.abc import Callable
from datetime import datetime
from typing import Optional
from typing import TypeAlias
from typing import Union

from .enums import Audio
from .enums import Creation
from .enums import Duration
from .enums import Size
from .read_stream import Stream
from .sort import sort

Attribute: TypeAlias = Union[str, int]
Partition: TypeAlias = Optional[str]


def _sort_ordering(
    attribute: Attribute, value: float, name: str, operation: Callable
) -> Partition:
    _attribute = float(attribute)

    return f"{name}_{value}" if operation(_attribute, value) else None


def _sort_between(
    attribute: Attribute, value: tuple[float, float], name: str
) -> Partition:
    lesser, greater = value

    return (
        f"{name}_{lesser}-{greater}"
        if (lesser <= float(attribute) <= greater)
        else None
    )


@sort()
def sort_audio(stream: Stream) -> str:
    return Audio.AUDIO.value if stream.audio is True else Audio.NO_AUDIO.value


@sort()
def sort_dimension(stream: Stream) -> str:
    return f"{stream.dimension.width}x{stream.dimension.height}"


@sort()
def sort_extension(stream: Stream) -> str:
    return stream.extension


@sort()
def sort_year(stream: Stream, value: int) -> Partition:
    return f"{Creation.YEAR}-{value}" if (stream.creation.year == value) else None


@sort()
def sort_month(stream: Stream, value: int) -> Partition:
    return f"{Creation.MONTH}-{value}" if (stream.creation.month == value) else None


@sort()
def sort_day(stream: Stream, value: int) -> Partition:
    return f"{Creation.DAY}-{value}" if (stream.creation.day == value) else None


@sort(parents=True)
def sort_full_date(stream: Stream) -> str:
    year, month, day = (
        stream.creation.year,
        stream.creation.month,
        stream.creation.day,
    )

    return f"{year}/{year}-{month}/{year}-{month}-{day}"


@sort()
def sort_specific_date(stream: Stream, value: datetime) -> Partition:
    return f"{value}" if (stream.creation == value) else None


@sort()
def sort_duration_long(stream: Stream, value: float) -> Partition:
    return _sort_ordering(
        attribute=stream.duration,
        value=value,
        name=Duration.LONGER.value,
        operation=operator.ge,
    )


@sort()
def sort_duration_short(stream: Stream, value: float) -> Partition:
    return _sort_ordering(
        attribute=stream.duration,
        value=value,
        name=Duration.SHORTER.value,
        operation=operator.le,
    )


@sort()
def sort_duration_between(stream: Stream, value: tuple[float, float]) -> Partition:
    return _sort_between(
        attribute=stream.duration,
        value=value,
        name=Duration.BETWEEN.value,
    )


@sort()
def sort_size_larger(stream: Stream, value: float) -> Partition:
    return _sort_ordering(
        attribute=stream.size,
        value=value,
        name=Size.LARGER.value,
        operation=operator.ge,
    )


@sort()
def sort_size_smaller(stream: Stream, value: float) -> Partition:
    return _sort_ordering(
        attribute=stream.size,
        value=value,
        name=Size.SMALLER.value,
        operation=operator.le,
    )


@sort()
def sort_size_between(stream: Stream, value: tuple[float, float]) -> Partition:
    return _sort_between(
        attribute=stream.size,
        value=value,
        name=Size.BETWEEN.value,
    )

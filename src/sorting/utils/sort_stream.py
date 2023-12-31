import operator
from collections.abc import Callable
from collections.abc import Iterator
from datetime import datetime
from typing import NamedTuple
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


class Result(NamedTuple):
    stream: Stream
    partition: str


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
def sort_audio(streams: Iterator[Stream]) -> Iterator[Result]:
    for stream in streams:
        partition = Audio.AUDIO.value if stream.audio is True else Audio.NO_AUDIO.value
        yield Result(stream, partition)


@sort()
def sort_dimension(streams: Iterator[Stream]) -> Iterator[Result]:
    for stream in streams:
        yield Result(stream, f"{stream.dimension.width}x{stream.dimension.height}")


@sort()
def sort_extension(streams: Iterator[Stream]) -> Iterator[Result]:
    for stream in streams:
        yield Result(stream, stream.extension)


@sort()
def sort_year(streams: Iterator[Stream], value: int) -> Iterator[Result]:
    for stream in streams:
        if stream.creation.year != value:
            continue

        yield Result(stream, f"{Creation.YEAR}-{value}")


@sort()
def sort_month(streams: Iterator[Stream], value: int) -> Iterator[Result]:
    for stream in streams:
        if stream.creation.month != value:
            continue

        yield Result(stream, f"{Creation.MONTH}-{value}")


@sort()
def sort_day(streams: Iterator[Stream], value: int) -> Iterator[Result]:
    for stream in streams:
        if stream.creation.day != value:
            continue

        yield Result(stream, f"{Creation.DAY}-{value}")


@sort(parents=True)
def sort_full_date(streams: Iterator[Stream]) -> Iterator[Result]:
    for stream in streams:
        year, month, day = (
            stream.creation.year,
            stream.creation.month,
            stream.creation.day,
        )

        yield Result(stream, f"{year}/{year}-{month}/{year}-{month}-{day}")


@sort()
def sort_specific_date(streams: Iterator[Stream], value: datetime) -> Iterator[Result]:
    for stream in streams:
        if stream.creation != value:
            continue

        yield Result(stream, f"{value}")


@sort()
def sort_duration_long(streams: Iterator[Stream], value: float) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_ordering(
            attribute=stream.duration,
            value=value,
            name=Duration.LONGER.value,
            operation=operator.ge,
        )

        if partition is None:
            continue

        yield Result(stream, partition)


@sort()
def sort_duration_short(streams: Iterator[Stream], value: float) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_ordering(
            attribute=stream.duration,
            value=value,
            name=Duration.SHORTER.value,
            operation=operator.le,
        )

        if partition is None:
            continue

        yield Result(stream, partition)


@sort()
def sort_duration_between(
    streams: Iterator[Stream], value: tuple[float, float]
) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_between(
            attribute=stream.duration,
            value=value,
            name=Duration.BETWEEN.value,
        )

        if partition is None:
            continue

        yield Result(stream, partition)


@sort()
def sort_size_larger(streams: Iterator[Stream], value: float) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_ordering(
            attribute=stream.size,
            value=value,
            name=Size.LARGER.value,
            operation=operator.ge,
        )

        if partition is None:
            continue

        yield Result(stream, partition)


@sort()
def sort_size_smaller(streams: Iterator[Stream], value: float) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_ordering(
            attribute=stream.size,
            value=value,
            name=Size.SMALLER.value,
            operation=operator.le,
        )

        if partition is None:
            continue

        yield Result(stream, partition)


@sort()
def sort_size_between(
    streams: Iterator[Stream], value: tuple[float, float]
) -> Iterator[Result]:
    for stream in streams:
        partition = _sort_between(
            attribute=stream.size,
            value=value,
            name=Size.BETWEEN.value,
        )

        if partition is None:
            continue

        yield Result(stream, partition)

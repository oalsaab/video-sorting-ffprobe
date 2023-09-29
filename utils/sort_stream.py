from datetime import date
from typing import Optional
from typing import Union

from utils.enums import Audio
from utils.enums import Creation
from utils.enums import Duration
from utils.enums import Size
from utils.read_stream import Stream
from utils.sort import sort


def _sort_greater_than(
    attribute: Union[str, int], value: float, name: str
) -> Optional[str]:
    return f"{name}_{value}" if (float(attribute) >= value) else None


def _sort_less_than(
    attribute: Union[str, int], value: float, name: str
) -> Optional[str]:
    return f"{name}_{value}" if (value >= float(attribute)) else None


def _sort_between(
    attribute: Union[str, int], value: tuple[float, float], name: str
) -> Optional[str]:
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
def sort_year(stream: Stream, value: str) -> Optional[str]:
    return f"{Creation.YEAR}-{value}" if (stream.creation.year == value) else None


@sort()
def sort_month(stream: Stream, value: str) -> Optional[str]:
    return f"{Creation.MONTH}-{value}" if (stream.creation.month == value) else None


@sort()
def sort_day(stream: Stream, value: str) -> Optional[str]:
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
def sort_specific_date(stream: Stream, value: date) -> Optional[str]:
    return f"{value}" if (stream.creation == value) else None


@sort()
def sort_duration_long(stream: Stream, value: float) -> Optional[str]:
    return _sort_greater_than(
        attribute=stream.duration,
        value=value,
        name=Duration.LONGER.value,
    )


@sort()
def sort_duration_short(stream: Stream, value: float) -> Optional[str]:
    return _sort_less_than(
        attribute=stream.duration,
        value=value,
        name=Duration.SHORTER.value,
    )


@sort()
def sort_duration_between(stream: Stream, value: tuple[float, float]) -> Optional[str]:
    return _sort_between(
        attribute=stream.duration,
        value=value,
        name=Duration.BETWEEN.value,
    )


@sort()
def sort_size_larger(stream: Stream, value: float) -> Optional[str]:
    return _sort_greater_than(
        attribute=stream.size,
        value=value,
        name=Size.LARGER.value,
    )


@sort()
def sort_size_smaller(stream: Stream, value: float) -> Optional[str]:
    return _sort_less_than(
        attribute=stream.size,
        value=value,
        name=Size.SMALLER.value,
    )


@sort()
def sort_size_between(stream: Stream, value: tuple[float, float]) -> Optional[str]:
    return _sort_between(
        attribute=stream.size,
        value=value,
        name=Size.BETWEEN.value,
    )

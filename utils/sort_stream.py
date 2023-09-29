from datetime import date
from enum import Enum
from typing import Optional
from typing import Union

from utils.create_stream import StreamMap


class Duration(str, Enum):
    LONGER = "duration_longer_than"
    SHORTEN = "duration_shorter_than"
    BETWEEN = "duration_between"


class Size(str, Enum):
    LARGER = "size_larger_than"
    SMALLER = "size_smaller_than"
    BETWEEN = "size_between"


class Creation(str, Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class Audio(str, Enum):
    AUDIO = "audio"
    NO_AUDIO = "no_audio"


def _sort_greater_than(
    mapped: StreamMap, value: float, name: str, attribute: Union[str, int]
) -> Optional[str]:
    return f"{name}_{value}" if (float(attribute) >= value) else None


def _sort_less_than(
    mapped: StreamMap, value: float, name: str, attribute: Union[str, int]
) -> Optional[str]:
    return f"{name}_{value}" if (value >= float(attribute)) else None


def _sort_between(
    mapped: StreamMap, value: tuple[float, float], name: str, attribute: Union[str, int]
) -> Optional[str]:
    lesser, greater = value

    return (
        f"{name}_{lesser}-{greater}"
        if (lesser <= float(mapped.stream.duration) <= greater)
        else None
    )


def sort_audio(mapped: StreamMap) -> str:
    return Audio.AUDIO.value if mapped.stream.audio is True else Audio.NO_AUDIO.value


def sort_dimension(mapped: StreamMap) -> str:
    return f"{mapped.stream.dimension.width}x{mapped.stream.dimension.height}"


def sort_extension(mapped: StreamMap) -> str:
    return mapped.stream.extension


def sort_year(mapped: StreamMap, value: str) -> Optional[str]:
    return (
        f"{Creation.YEAR}-{value}" if (mapped.stream.creation.year == value) else None
    )


def sort_month(mapped: StreamMap, value: str) -> Optional[str]:
    return (
        f"{Creation.MONTH}-{value}" if (mapped.stream.creation.month == value) else None
    )


def sort_day(mapped: StreamMap, value: str) -> Optional[str]:
    return f"{Creation.DAY}-{value}" if (mapped.stream.creation.day == value) else None


def sort_full_date(mapped: StreamMap) -> str:
    year, month, day = (
        mapped.stream.creation.year,
        mapped.stream.creation.month,
        mapped.stream.creation.day,
    )

    return f"{year}/{year}-{month}/{year}-{month}-{day}"


def sort_specific_date(mapped: StreamMap, value: date) -> Optional[str]:
    return f"{value}" if (mapped.stream.creation == value) else None

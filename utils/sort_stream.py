from datetime import date
from typing import Optional
from typing import Union

from utils.create_stream import StreamMap
from utils.enums import Audio
from utils.enums import Creation
from utils.enums import Duration
from utils.enums import Size


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


def sort_duration_long(mapped: StreamMap, value: float) -> Optional[str]:
    return _sort_greater_than(
        attribute=mapped.stream.duration,
        value=value,
        name=Duration.LONGER.value,
    )


def sort_duration_short(mapped: StreamMap, value: float) -> Optional[str]:
    return _sort_less_than(
        attribute=mapped.stream.duration,
        value=value,
        name=Duration.SHORTER.value,
    )


def sort_duration_between(
    mapped: StreamMap, value: tuple[float, float]
) -> Optional[str]:
    return _sort_between(
        attribute=mapped.stream.duration,
        value=value,
        name=Duration.BETWEEN.value,
    )


def sort_size_larger(mapped: StreamMap, value: float) -> Optional[str]:
    return _sort_greater_than(
        attribute=mapped.stream.size,
        value=value,
        name=Size.LARGER.value,
    )


def sort_size_smaller(mapped: StreamMap, value: float) -> Optional[str]:
    return _sort_less_than(
        attribute=mapped.stream.size,
        value=value,
        name=Size.SMALLER.value,
    )


def sort_size_between(mapped: StreamMap, value: tuple[float, float]) -> Optional[str]:
    return _sort_between(
        attribute=mapped.stream.size,
        value=value,
        name=Size.BETWEEN.value,
    )

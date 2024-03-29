from enum import Enum


class Model(str, Enum):
    STREAMS = "streams"
    CODEC_TYPE = "codec_type"
    AUDIO = "audio"
    WIDTH = "width"
    HEIGHT = "height"
    FORMAT = "format"
    DURATION = "duration"
    TAGS = "tags"
    CREATION_TIME = "creation_time"


class Duration(str, Enum):
    LONGER = "duration_longer_than"
    SHORTER = "duration_shorter_than"
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


class Command(str, Enum):
    AUDIO = "audio"
    DATE = "date"
    SIZE = "size"
    DURATION = "duration"
    DIMENSIONS = "dimensions"
    EXTENSIONS = "extensions"


class Argument(str, Enum):
    DIRECTORY = "directory"
    EXTENSION = "extension"


class Option(str, Enum):
    LARGER = "--larger"
    SMALLER = "--smaller"
    LONGER = "--longer"
    SHORTER = "--shorter"
    BETWEEN = "--between"
    YEAR = "--year"
    MONTH = "--month"
    DAY = "--day"
    SPECIFIC = "--specific"

    @classmethod
    def duration(cls) -> list[str]:
        return [cls.LONGER.value, cls.SHORTER.value, cls.BETWEEN.value]

    @classmethod
    def size(cls) -> list[str]:
        return [cls.LARGER.value, cls.SMALLER.value, cls.BETWEEN.value]

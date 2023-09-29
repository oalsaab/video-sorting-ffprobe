from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import NamedTuple


class Dimensions(NamedTuple):
    width: str
    height: str


@dataclass
class Stream:
    stream: dict
    file: Path

    @cached_property
    def streams(self) -> list[dict]:
        return self.stream.get("streams", [{}])

    @property
    def audio(self) -> bool:
        _codecs = (streams.get("codec_type") for streams in self.streams)

        return "audio" in _codecs

    @property
    def dimension(self) -> Dimensions:
        for item in self.streams:
            width, height = item.get("width"), item.get("height")

            if all(_ is not None for _ in (width, height)):
                return Dimensions(width, height)

    @property
    def duration(self):
        return self.stream["format"]["duration"]

    @property
    def creation(self):
        creation_time_utc = self.stream["streams"][0]["tags"]["creation_time"]
        creation_time_str = creation_time_utc[:10]
        creation_time = creation_time_str.split("-")
        year, month, day = creation_time

        return {"specific": creation_time_str, "year": year, "month": month, "day": day}

    @property
    def size(self):
        size = self.file.stat().st_size
        return size / (1024 * 1024)

    @property
    def extension(self):
        extension_path = self.file.suffix
        _, extension = extension_path.split(".")
        return extension

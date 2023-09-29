from dataclasses import dataclass
from datetime import date, datetime
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
    def duration(self) -> str:
        return self.stream.get("format", {}).get("duration")

    @property
    def creation(self) -> date:
        _tags: dict = next(iter(self.streams), {}).get("tags", {})
        _creation_time = _tags.get("creation_time")

        if _creation_time is None:
            return None

        return datetime.strptime(_creation_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    @property
    def size(self) -> int:
        _size = self.file.stat().st_size
        return _size / (1024 * 1024)

    @property
    def extension(self) -> str:
        _, extension = self.file.suffix.split(".")

        return extension

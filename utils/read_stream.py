from json import loads
from pathlib import Path, WindowsPath
from dataclasses import dataclass

@dataclass
class ReadStream:
    stream: bytes
    file: WindowsPath

    def __post_init__(self):
        self.stream = loads(self.stream)
        self.file = Path(self.file)

    @property
    def audio(self):
        codecs = [streams["codec_type"] for streams in self.stream["streams"]]
        return "audio" if "audio" in codecs else "no_audio"

    @property
    def dimension(self):
        try:
            width = self.stream["streams"][0]["width"]
            height = self.stream["streams"][0]["height"]
        except KeyError:
            width = self.stream["streams"][1]["width"]
            height = self.stream["streams"][1]["height"]

        return (width, height)

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

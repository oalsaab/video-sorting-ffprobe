import subprocess
import json
import shlex
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


class VideoSorting:
    """Spawns a new process of ffprobe or stat object on every file in the user-supplied directory.
    Connects to the output pipes and captures the output for video file sorting."""

    def __init__(self, file, args, path):
        self.file = file
        self.args = args
        self.path = path

        cmd = "ffprobe -v quiet -print_format json -show_format -show_streams"
        cmd_ffprobe = shlex.split(cmd)
        cmd_ffprobe.append(self.file)

        process = subprocess.run(cmd_ffprobe, capture_output=True)
        self.video_json = json.loads(process.stdout)

    def sort(self, folder, parents=False):
        Path(f"{self.path}/{folder}").mkdir(parents=parents, exist_ok=True)
        shutil.move(self.file, f"{self.path}/{folder}")

        logging.info(" %s moved to %s" % (self.file.name, folder))

    def audio(self):
        return [stream["codec_type"] for stream in self.video_json["streams"]]

    def audio_sort(self):
        if "audio" in self.audio():
            self.sort("audio")
        else:
            self.sort("no_audio")

    def dimensions(self):
        try:
            width = self.video_json["streams"][0]["width"]
            height = self.video_json["streams"][0]["height"]
        except KeyError:
            width = self.video_json["streams"][1]["width"]
            height = self.video_json["streams"][1]["height"]

        return (width, height)

    def dimensions_sort(self):
        width, height = self.dimensions()
        self.sort(f"{width}x{height}")

    def durations(self):
        return self.video_json["format"]["duration"]

    def duration_long(self):
        if float(self.durations()) >= self.args.duration_long:
            self.sort(f"longer_than_{self.args.duration_long}")

    def duration_short(self):
        if self.args.duration_short >= float(self.durations()):
            self.sort(f"shorter_than_{self.args.duration_short}")

    def duration_between(self):
        if (
            self.args.duration_between[0]
            <= float(self.durations())
            <= self.args.duration_between[1]
        ):
            self.sort(
                f"between_{self.args.duration_between[0]}-{self.args.duration_between[1]}"
            )

    def creation(self):
        creation_time_utc = self.video_json["streams"][0]["tags"]["creation_time"]
        creation_time_str = creation_time_utc[:10]
        creation_time = creation_time_str.split("-")

        year, month, day = creation_time

        return {"specific": creation_time_str, "year": year, "month": month, "day": day}

    def creation_year(self):
        if self.args.creation_year == int(self.creation()["year"]):
            self.sort(f"year-{self.args.creation_year}")

    def creation_month(self):
        if self.args.creation_month == int(self.creation()["month"]):
            self.sort(f"month-{self.args.creation_month}")

    def creation_day(self):
        if self.args.creation_day == int(self.creation()["day"]):
            self.sort(f"day-{self.args.creation_day}")

    def creation_specific(self):
        if self.args.creation_specific == self.creation()["specific"]:
            self.sort(self.args.creation_specific)

    def creation_full(self):
        creation = self.creation()
        year, month, day = creation["year"], creation["month"], creation["day"]
        self.sort(f"{year}/{year}-{month}/{year}-{month}-{day}", True)

    def size(self):
        size = Path(self.file).stat().st_size
        return size / (1024 * 1024)

    def size_larger(self):
        if float(self.size()) >= self.args.size_larger:
            self.sort(f"size_larger_than_{self.args.size_larger}")

    def size_smaller(self):
        if self.args.size_smaller >= float(self.size()):
            self.sort(f"size_smaller_than_{self.args.size_smaller}")

    def size_between(self):
        if self.args.size_between[0] <= float(self.size()) <= self.args.size_between[1]:
            self.sort(
                f"size_between_{self.args.size_between[0]}-{self.args.size_between[1]}"
            )

    def extensions(self):
        extension_path = Path(self.file).suffix
        _, extension = extension_path.split(".")
        return extension

    def extensions_sort(self):
        self.sort(f"{self.extensions()}")

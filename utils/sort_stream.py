import shutil
import logging
from pathlib import Path
from utils.read_stream import ReadStream

logging.basicConfig(level=logging.INFO)


class SortStream:
    def __init__(self, stream, file, arg, args):
        self.stream = ReadStream(stream, file)
        self.file = file
        self.arg = arg
        self.args = args
        self.path = args.folderPath

    def sort(self, result, folder, parents=False):
        if result:
            Path(f"{self.path}/{folder}").mkdir(parents=parents, exist_ok=True)
            shutil.move(self.file, f"{self.path}/{folder}")
            logging.info(" %s moved to %s" % (self.file.name, folder))

    def audio_sort(self):
        output = self.stream.audio
        self.sort(True, output)

    def dimensions_sort(self):
        width, height = self.stream.dimension
        self.sort(True, f"{width}x{height}")

    def extensions_sort(self):
        extension = self.stream.extension
        self.sort(True, f"{extension}")

    def duration_sort(self):
        duration = self.stream.duration
        obj = DurationSort(duration, self.args)
        result, folder = obj.retrieve[self.arg]()
        self.sort(result, folder)

    def creation_sort(self):
        creation = self.stream.creation
        obj = CreationSort(creation, self.args)

        if self.arg == "creation_full":
            result, folder, parent = obj.retrieve[self.arg]()
            self.sort(result, folder, parent)
        else:
            result, folder = obj.retrieve[self.arg]()
            self.sort(result, folder)

    def size_sort(self):
        size = self.stream.size
        obj = SizeSort(size, self.args)
        result, folder = obj.retrieve[self.arg]()
        self.sort(result, folder)


class DurationSort:
    def __init__(self, duration, args):
        self.duration = duration
        self.args = args

    @property
    def retrieve(self):
        return {
            "duration_long": self.duration_long,
            "duration_short": self.duration_short,
            "duration_between": self.duration_between,
        }

    def duration_long(self):
        result = float(self.duration) >= self.args.duration_long
        return (result, f"longer_than_{self.args.duration_long}")

    def duration_short(self):
        result = self.args.duration_short >= float(self.duration)
        return (result, f"shorter_than_{self.args.duration_short}")

    def duration_between(self):
        lesser, greater = self.args.duration_between
        result = lesser <= float(self.duration) <= greater
        return (result, f"between_{lesser}-{greater}")


class CreationSort:
    def __init__(self, creation, args):
        self.year, self.month, self.day = (
            creation["year"],
            creation["month"],
            creation["day"],
        )
        self.specific = creation["specific"]
        self.args = args

    @property
    def retrieve(self):
        return {
            "creation_year": self.creation_year,
            "creation_month": self.creation_month,
            "creation_day": self.creation_day,
            "creation_specific": self.creation_specific,
            "creation_full": self.creation_full,
        }

    def creation_year(self):
        result = self.args.creation_year == int(self.year)
        return (result, f"year-{self.args.creation_year}")

    def creation_month(self):
        result = self.args.creation_month == int(self.month)
        return (result, f"year-{self.args.creation_month}")

    def creation_day(self):
        result = self.args.creation_day == int(self.day)
        return (result, f"year-{self.args.creation_day}")

    def creation_specific(self):
        result = self.specific == self.args.creation_specific
        return (result, self.args.creation_specific)

    def creation_full(self):
        return (
            True,
            f"{self.year}/{self.year}-{self.month}/{self.year}-{self.month}-{self.day}",
            True,
        )


class SizeSort:
    def __init__(self, size, args):
        self.size = size
        self.args = args

    @property
    def retrieve(self):
        return {
            "size_larger": self.size_larger,
            "size_smaller": self.size_smaller,
            "size_between": self.size_between,
        }

    def size_larger(self):
        result = float(self.size) >= self.args.size_larger
        return (result, f"size_larger_than_{self.args.size_larger}")

    def size_smaller(self):
        result = self.args.size_smaller >= float(self.size)
        return (result, f"size_smaller_than_{self.args.size_smaller}")

    def size_between(self):
        lesser, greater = self.args.size_between
        result = lesser <= float(self.size) <= greater
        return (result, f"size_between_{lesser}-{greater}")

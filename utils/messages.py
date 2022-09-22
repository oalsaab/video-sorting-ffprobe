from argparse import ArgumentTypeError
from datetime import datetime
from pathlib import Path


def valid_path(path):
    """Validate the user-supplied path is a existing directory."""
    if Path(path).is_dir():
        return path
    else:
        raise NotADirectoryError(f"Could not find the directory: {path}")


def valid_date(date):
    """Validate the user-supplied date is a valid format to parse."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        raise ArgumentTypeError("Provide the format: YYYY-MM-DD")


options = {
    "f": "path to folder with video files",
    "v": "extension of videos to sort",
    "-a": "sort videos by audio",
    "-d": "sort videos by dimensions",
    "-e": "sort videos by extension",
    "-dl": "sort videos by duration longer than argument",
    "-ds": "sort videos by duration shorter than argument",
    "-db": "sort videos by duration between arguments",
    "-cy": "sort videos by year",
    "-cm": "sort videos by month",
    "-cd": "sort videos by day",
    "-cs": "sort videos by specific date",
    "-cf": "sort videos by full date",
    "-sl": "sort videos by size larger than argument",
    "-ss": "sort videos by size smaller than argument",
    "-sb": "sort videos by size between arguments",
}

actions = [
    "audio",
    "dimensions",
    "extensions",
    "duration_long",
    "duration_short",
    "duration_between",
    "creation_year",
    "creation_month",
    "creation_day",
    "creation_specific",
    "creation_full",
    "size_larger",
    "size_smaller",
    "size_between",
]

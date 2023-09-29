from pathlib import Path

import click

directory = click.argument("directory", type=click.Path(exists=True))
extension = click.argument("extension", nargs=-1)


@click.group()
def cli():
    """Multimedia sorting CLI

    Provide a sort command followed by path to directory
    and extensions of multimedia files to process

    e.g. sorter.py audio 'path/videos' mov mp4

    """


@cli.command("audio")
@directory
@extension
def audio(directory: Path, extension: tuple):
    """Sort by audio"""

    return directory


@cli.command("dimensions")
@directory
@extension
def dimensions(directory: Path, extension: tuple):
    """Sort by dimensions"""

    return directory


@cli.command("extensions")
@directory
@extension
def extensions(directory: Path, extension: tuple):
    """Sort by extensions"""

    return directory


@cli.command("duration_longer")
@directory
@extension
def duration_longer(directory: Path, extension: tuple):
    """Sort by duration longer than"""

    return directory


@cli.command("duration_shorter")
@directory
@extension
def duration_shorter(directory: Path, extension: tuple):
    """Sort by duration shorter than"""

    return directory


@cli.command("duration_between")
@directory
@extension
def duration_between(directory: Path, extension: tuple):
    """Sort by duration between"""

    return directory


@cli.command("year")
@directory
@extension
def creation_year(directory: Path, extension: tuple):
    """Sort by year"""

    return directory


@cli.command("month")
@directory
@extension
def creation_year(directory: Path, extension: tuple):
    """Sort by month"""

    return directory


@cli.command("day")
@directory
@extension
def creation_day(directory: Path, extension: tuple):
    """Sort by day"""

    return directory


@cli.command("date")
@directory
@extension
def creation_date(directory: Path, extension: tuple):
    """Sort by full date"""

    return directory


@cli.command("specfic_date")
@directory
@extension
def creation_specific(directory: Path, extension: tuple):
    """Sort by specfic date"""

    return directory


@cli.command("size_larger")
@directory
@extension
def size_larger(directory: Path, extension: tuple):
    """Sort by size larger than"""

    return directory


@cli.command("size_smaller")
@directory
@extension
def size_smaller(directory: Path, extension: tuple):
    """Sort by size smaller than"""

    return directory


@cli.command("size_between")
@directory
@extension
def size_between(directory: Path, extension: tuple):
    """Sort by size between"""

    return directory


if __name__ == "__main__":
    cli()

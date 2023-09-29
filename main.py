import argparse
import asyncio
import logging
from pathlib import Path

from utils.arguments import arguments
from utils.create_stream import stream_collection
from utils.messages import actions
from utils.read_stream import Stream
from utils.sort_stream import SortStream


def create_args():
    parser = argparse.ArgumentParser("Video sorting command line utility program")
    arguments(parser)
    return (parser, parser.parse_args())


def action_map():
    maps = {}
    for action in actions:
        if "_" in action:
            name, _ = action.split("_")
            method = name + "_sort"
            maps[action] = getattr(SortStream, method)
        else:
            method = action + "_sort"
            maps[action] = getattr(SortStream, method)

    return maps


def discover_action(args):
    for arg, val in args.items():
        if (arg in actions) and val:
            return arg


def main():
    parser, args = create_args()
    arg = discover_action(vars(args))
    if not arg:
        raise parser.error("Choose a action to perform")

    extensions = [("." + extension) for extension in args.videoExtension]
    files = [
        file
        for file in Path(args.folderPath).iterdir()
        if file.suffix.lower() in extensions
    ]
    streams = asyncio.run(stream_collection(files))

    method = action_map()
    for file, stream in streams.items():
        process = SortStream(
            stream=Stream(stream),
            file=file,
            arg=arg,
            args=args,
        )

        run = method[arg]

        try:
            run(process)
        except KeyError:
            logging.warning(
                "%s : Corrupted or does not contain multimedia streams" % file.name
            )


if __name__ == "__main__":
    main()

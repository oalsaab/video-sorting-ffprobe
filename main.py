import argparse
import logging
from pathlib import Path
from arguments import arguments
from sorting import VideoSorting
from messages import actions


def create_args():
    parser = argparse.ArgumentParser("Video sorting command line utility program")
    arguments(parser)
    return (parser, parser.parse_args())


def actions_dict():
    action_dict = {}

    for action in actions:
        if "_" in action:
            action_dict[action] = getattr(VideoSorting, action)
        else:
            action_dict[action] = getattr(VideoSorting, (action + "_sort"))

    return action_dict


def discover_action(args):
    for (arg, val) in args.items():
        if (arg in actions) and val:
            return arg


def main():
    """Create command-line interface and call VideoSorting to process and sort the files."""
    parser, args = create_args()
    arg = discover_action(vars(args))
    if not arg:
        raise parser.error("Choose a action to perform")

    files = Path(args.folderPath).iterdir()
    videos = [("." + extension) for extension in args.videoExtension]

    action_dict = actions_dict()

    for file in files:
        if file.suffix.lower() in videos:
            process = VideoSorting(file, args, args.folderPath)
            run = action_dict[arg]

            try:
                run(process)
            except KeyError:
                logging.warning(
                    " %s : Corrupted or does not contain multimedia streams" % file.name
                )


if __name__ == "__main__":
    print("Sorting video files...")
    main()
    print("Completed sorting video files")

import messages


def arguments(parser):
    """Command line positionals and optionals for video sorting."""
    abbrv = [arg for arg in messages.options if "-" in arg]
    action_dashes = [("--" + arg) for arg in messages.actions]
    args = dict(zip(abbrv, action_dashes))

    parser.add_argument(
        "folderPath", type=messages.valid_path, help=messages.options["f"]
    )

    parser.add_argument("videoExtension", nargs="+", help=messages.options["v"])

    parser.add_argument(
        "-a", args["-a"], action="store_true", help=messages.options["-a"]
    )

    parser.add_argument(
        "-d", args["-d"], action="store_true", help=messages.options["-d"]
    )

    parser.add_argument(
        "-e", args["-e"], action="store_true", help=messages.options["-e"]
    )

    duration_group = parser.add_argument_group(
        "duration", description="duration in seconds"
    )

    duration_group.add_argument(
        "-dl", args["-dl"], type=float, help=messages.options["-dl"]
    )

    duration_group.add_argument(
        "-ds", args["-ds"], type=float, help=messages.options["-ds"]
    )

    duration_group.add_argument(
        "-db", args["-db"], type=float, nargs=2, help=messages.options["-db"]
    )

    creation_group = parser.add_argument_group(
        "creation time", description="European date format"
    )

    creation_group.add_argument(
        "-cy", args["-cy"], type=int, help=messages.options["-cy"]
    )

    creation_group.add_argument(
        "-cm",
        args["-cm"],
        type=int,
        choices=range(1, 13),
        metavar="[1-12]",
        help=messages.options["-cm"],
    )

    creation_group.add_argument(
        "-cd",
        args["-cd"],
        choices=range(1, 32),
        metavar="[1-31]",
        help=messages.options["-cd"],
    )

    creation_group.add_argument(
        "-cs",
        args["-cs"],
        type=messages.valid_date,
        metavar="[YYYY-MM-DD]",
        help=messages.options["-cs"],
    )

    creation_group.add_argument(
        "-cf", args["-cf"], action="store_true", help=messages.options["-cf"]
    )

    size_group = parser.add_argument_group("size", description="Size in Megabytes")

    size_group.add_argument(
        "-sl", args["-sl"], type=float, help=messages.options["-sl"]
    )

    size_group.add_argument(
        "-ss", args["-ss"], type=float, help=messages.options["-ss"]
    )

    size_group.add_argument(
        "-sb", args["-sb"], type=float, nargs=2, help=messages.options["-sb"]
    )

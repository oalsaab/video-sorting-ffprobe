import messages

def arguments(parser):
    """Command line positionals and optionals for video sorting."""
    
    parser.add_argument(
        'folderPath', 
        type=messages.valid_path, 
        help=messages.options['f']
    )

    parser.add_argument(
        'videoExtension',
        nargs='+',
        help=messages.options['v']
    )
    
    parser.add_argument(
        '-a', 
        '--audio',
        action='store_true',
        help=messages.options['-a']
    )
    
    parser.add_argument(
        '-d', 
        '--dimensions', 
        action='store_true',
        help=messages.options['-d']
    )

    parser.add_argument(
        '-e', 
        '--extension', 
        action='store_true',
        help=messages.options['-e']
    )

    duration_group = parser.add_argument_group('duration', description='duration in seconds')

    duration_group.add_argument(
        '-dl', 
        '--duration_long',
        type=float,
        help=messages.options['-dl']
    )
    
    duration_group.add_argument(
        '-ds', 
        '--duration_short',
        type=float,
        help=messages.options['-ds']
    )
    
    duration_group.add_argument(
        '-db', 
        '--duration_between',
        type=float, 
        nargs=2,
        help=messages.options['-db']
    )
    
    creation_group = parser.add_argument_group('creation time', description='European date format')
    
    creation_group.add_argument(
        '-cy', 
        '--creation_year',
        type=int,
        help=messages.options['-cy']
    )
    
    creation_group.add_argument(
        '-cm', 
        '--creation_month',
        type=int,
        choices=range(1, 13),
        metavar='[1-12]',
        help=messages.options['-cm']
    )
    
    creation_group.add_argument(
        '-cd', 
        '--creation_day',
        choices=range(1, 32),
        metavar='[1-31]',
        help=messages.options['-cd']
    )
    
    creation_group.add_argument(
        '-cs', 
        '--creation_specific',
        type=messages.valid_date,
        metavar='[YYYY-MM-DD]',
        help=messages.options['-cs']
    )
    
    creation_group.add_argument(
        '-cf', 
        '--creation_full', 
        action='store_true',
        help=messages.options['-cf']
    )
    
    size_group = parser.add_argument_group('size', description='Size in Megabytes')
    
    size_group.add_argument(
        '-sl', 
        '--size_larger',
        type=float,
        help=messages.options['-sl']
    )
    
    size_group.add_argument(
        '-ss', 
        '--size_smaller',
        type=float,
        help=messages.options['-ss']
    )
    
    size_group.add_argument(
        '-sb', 
        '--size_between',
        type=float, 
        nargs=2,
        help=messages.options['-sb']
    )


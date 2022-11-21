"""
This module contains a custom Exception class and methods to help parse CLI arguments.
"""
from argparse import ArgumentParser, Namespace

POKEMON = 'pokemon'
ABILITY = 'ability'
MOVE = 'move'


class InvalidModeException(Exception):
    """
    InvalidModeException is a custom Exception class raised when search mode of Request object is not valid.
    """
    pass


def _parse_cli_arguments() -> Namespace:
    """
    Parses CLI arguments.

    :return: Namespace
    """
    parser = ArgumentParser()
    parser.add_argument(
        "mode", help="Change between Pokemon, ability, and move search mode.")
    parser.add_argument('--expanded', action='store_true')
    data_group = parser.add_mutually_exclusive_group()
    parser.add_argument('--output')
    data_group.add_argument(
        "--inputfile", help="The text file that has pokemon, abilities, and moves to search for.")
    data_group.add_argument(
        "--inputdata", help="The input name must be provided")

    return parser.parse_args()


def _parse_requests(fname):
    """
    Parses requests from input file

    :param fname: String, inputfile filepath
    :return: list of strings that will be used to create multiple target_urls
    """
    def strip_lower(msg):
        return msg.strip().lower()

    with open(fname, 'r') as f:
        return list(map(strip_lower, f.readlines()))


def _parse_mode(mode_arg):
    """
    Parses search mode of Request object.

    :param mode_arg: String, search mode of Request object
    :return: String/None, returns mode_arg if valid_option, raises InvalidModeException if not
    """
    valid_option = mode_arg == POKEMON or mode_arg == ABILITY or mode_arg == MOVE

    if valid_option:
        return mode_arg
    else:
        raise InvalidModeException(
            f"Mode must be {POKEMON} or {ABILITY} or {MOVE}!")


def parse_request_requirements():
    """Parses request data from the command-line.

    :return: tuple (search_mode:str, inputfile:str|None, inputdata:str|None, is_expanded:bool)
    """
    parsed_data = _parse_cli_arguments()

    mode = _parse_mode(parsed_data.mode)

    is_expanded = parsed_data.expanded

    return mode, parsed_data.inputfile, parsed_data.inputdata, is_expanded, parsed_data.output

"""
This module contains Modes enum and Request class.
"""
from enum import Enum
from dataclasses import dataclass


class Modes(str, Enum):
    POKEMON = "https://pokeapi.co/api/v2/pokemon"
    ABILITY = "https://pokeapi.co/api/v2/ability"
    MOVE = "https://pokeapi.co/api/v2/move"
    STAT = "https://pokeapi.co/api/v2/stat"


@dataclass
class Request:
    search_mode: str
    input_file: str
    input_data: str
    is_expanded: bool
    output: str


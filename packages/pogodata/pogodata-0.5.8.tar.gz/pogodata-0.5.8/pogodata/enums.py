from enum import Enum

class BasicType(Enum):
    UNSET = 0
    SET = 1

class PokemonType(Enum):
    UNSET = 0
    BASE = 1
    FORM = 2
    TEMP_EVOLUTION = 3

class QuestType(Enum):
    UNSET = 0
    BASE = 1
    EVENT = 2
    SPONSORED = 3
    AR = 4

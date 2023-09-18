from typing import Dict

from config import get_config
from funcs.tools import is_intstr
from ..core import GridSpace, BoardVector, CharacterManager, Character
from bot_core.signals import OutOfBounds


class Stage:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.chars = CharacterManager(set())

    def newc(self, char_id):
        pass

'''class StageO(GridSpace):
    def __init__(self, size: BoardVector):
        GridSpace.__init__(self, size)
        self.chars = CharacterManager(set())
        from ..assets import skills
        self.skill_data = skills
        self.InputValidityChecker = InputValidityChecker
        self.status = "init"
            
    def initial_determine(self, char: Character):
        char.actefs.affect_from_all(char, "initial")

    def ending_determine(self, char: Character):
        char.actefs.affect_from_all(char, "ending")

    def is_tile_occupied(self, tile: BoardVector) -> bool:
        return any(tile == char.pos for char in self.chars)

    def move(self, char, new_pos_data: Dict[str, int]):
        new_pos = BoardVector(**new_pos_data)
        self.InputValidityChecker.movement(self, new_pos)
        char.move_to(new_pos)
        return'''


'''class InputValidityChecker:
    class NoSuchCareer(Exception):
        def __init__(self, career: str):
            super().__init__(career)

    class TeamIDMustBeNumber(Exception):
        pass
        
    @staticmethod
    def movement(stage: Stage, new_pos: BoardVector):
        if not stage.is_in_bound(new_pos):
            raise OutOfBounds
        if stage.is_tile_occupied(new_pos):
            raise stage.TileOccupied

    @staticmethod
    def char_data(career, team_id_str):
        all_careers = get_config("careers","cw")
        if career not in all_careers:
            raise InputValidityChecker.NoSuchCareer(career)
        if not is_intstr(team_id_str):
            raise InputValidityChecker.TeamIDMustBeNumber'''
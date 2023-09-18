from typing import Set
from typing_extensions import Self, List, Dict, Callable, Any


from config import get_config
from funcs.tools import is_intstr


class BoardVector:  #a kind of Vector2i

    def __init__(self, r: int, c: int):
        self.r: int = r
        self.c: int = c

    @classmethod
    def default(cls):
        return cls(0, 0)

    @classmethod
    def square(cls, val):
        return cls(val, val)

    def __eq__(self, other):
        if not isinstance(other, BoardVector):
            raise TypeError
        return self.r == other.r and self.c == other.c
        

class Operation:

    def __init__(self, type: str, value: float, target: str):
        self.type = type
        self.value = value
        self.target = target


class Passive:

    def __init__(self, operations, duration) -> None:
        self.operations = operations
        self.duration = duration


class PassiveEffects(list):

    def __init__(self, li: List[Passive]):
        super().__init__(li)

    def append(self, passive: Passive):
        super().append(passive)

    def get_operations_by_target(self, target) -> Dict[str, float]:
        multiplier = 1.0
        addend = 0.0
        super_multiplier = 1.0

        for passive in self:
            for operation in passive:
                if operation.target != target:
                    continue
                if operation.type == "multiplier":
                    multiplier *= operation.value
                if operation.type == "addend":
                    addend += operation.value
                if operation.type == "super_multiplier":
                    super_multiplier *= operation.value

        return {
            "multiplier": multiplier,
            "addend": addend,
            "super_multiplier": super_multiplier
        }


class Character:

    def __init__(self, pos: BoardVector, name: str,
                 team_id: int, *, mhp: int, mmp: int, at: int, sp: int,
                 df: int, mv: int, skill_list: List[str], career: str):
        self.pos = pos
        self.name = name
        self.team_id = team_id
        self.hp = mhp
        self.mp = mmp
        self.IMHP = mhp
        self.IMMP = mmp
        self.IAT = at
        self.ISP = sp
        self.IDF = df
        self.IMV = mv
        self.skills = skill_list
        self.actefs = ActiveEffects([])
        self.pasefs = PassiveEffects([])
        self.career = career
        #self.stats = CharStatCalculator

    class MoveBeyondMV(Exception):
        pass

    @classmethod
    def create_by_career(cls, career: str, name: str, team_id: int):
        char_properties = get_config("char_properties", "cw")[career]
        return cls(
            BoardVector.default(), 
            name, 
            team_id,
            **char_properties
        )

    def is_in_moving_field(self, destination: BoardVector) -> bool:
        "return dest. - self.pos < self.mv"
        delta_r = destination.r - self.pos.r
        delta_c = destination.c - self.pos.c
        return delta_r + delta_c < self.mv

    def move_to(self, destination: BoardVector) -> None:
        if not self.is_in_moving_field(destination):
            raise self.MoveBeyondMV
        self.pos = destination

    def is_same_team(self, other: Self):
        return self.team_id == other.team_id

    def property_calc(self, target: str, base: int):
        operations = self.pasefs.get_operations_by_target(target)
        return round((base * operations["multiplier"] + operations["addend"]) *
                     operations["super_multiplier"])

    @property
    def mhp(self):
        return self.property_calc("mhp", self.IMHP)

    @property
    def mmp(self):
        return self.property_calc("mmp", self.IMMP)

    @property
    def at(self):
        return self.property_calc("at", self.IAT)

    @property
    def sp(self):
        return self.property_calc("sp", self.ISP)

    @property
    def df(self):
        return self.property_calc("df", self.IDF)

    @property
    def mv(self):
        return self.property_calc("mv", self.IMV)

    pass


class Active:

    def __init__(self, name: str, occasion: str, time: int,
                 affect: Callable[[Character], Any]):
        self.name = name
        self.occasion = occasion
        self.time = time
        self.affect = affect


class ActiveEffects(list):
    def __init__(self, li: List[Active]):
        super().__init__(li)
        from ..assets import actefs
        self.actef_data = actefs

    def append(self, active: Active):
        super().append(active)

    def append_by_name(self, active_name: str):
        self.append(self.actef_data.get_actef(active_name))

    def consume(self, active, amount=1):
        pt = active.time - amount
        if pt <= 0:
            self.remove(active)
            return 0
        active.time = pt
        return pt

    def affect_from_all(self, char: Character, occasion: str):
        for active in self:
            if active.occasion != occasion:
                continue
            active.affect(char)
            self.consume(active)


class GridSpace:
    def __init__(self, size: BoardVector):
        self.board_size = size

    class TileOccupied(Exception):
        pass

    def is_in_bound(self, pos: BoardVector):
        return pos.r >= 0 and pos.r < self.board_size.r and pos.c >= 0 and pos.c < self.board_size.c


class CharacterManager(set):
    def __init__(self, chars: Set[Character]):
        super().__init__(chars)

    #dev
    def first_in_iter(self) -> Character | None:
        for char in self:
            return char
    
    def by_name(self, char_name: str) -> Character:
        for char in self:
            if char.name == char_name:
                return char
        raise KeyError
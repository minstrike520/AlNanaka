from ..core.core import Character

from typing import List


class NoSuchSkill(Exception):
    pass


def attack(caster: Character, target: Character):
    pass

def self_heal(caster: Character):
    pass

def bomb(caster: Character):
    pass

dictionary = {
    "base": {
        "attack": {
            "name": "attack",
            "select_type": "enemy",
            "func": attack
        },
        "self_heal": {
            "name": "self_heal",
            "select_type": "none",
            "func": self_heal
        },
        "bomb": {
            "name": "bomb",
            "select_type": "location",
            "func": bomb
        }
    },
}


def get_skill_names():
    l = []
    for career_data in dictionary.values():
        for skill_name in career_data:
            l.append(skill_name)
    print("[skills] get_skill_names()")
    print(f"[skills] ...-> {l}")
    return l

def by_career(career: str) -> List[str]:
    return list(dictionary[career])

def get_skill(skill_name: str):
    for career_skills in dictionary.values():
        for name, value in career_skills.items():
            if skill_name == name:
                return value
    raise NoSuchSkill
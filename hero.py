from typing import List

from game_object import GameObject
from item import Item

KNIGHT_HEALTH = 5
KNIGHTS_MEDICAL_KIT = 3


class Hero(GameObject):
    def __init__(self, x: int, y: int, name: str):
        super().__init__(x, y, "hero")
        self.__name = name
        self.__health = KNIGHT_HEALTH
        self.__count_medical_kit = KNIGHTS_MEDICAL_KIT
        self.__pocket = []
        self.__old_direction = ""

    def move(self, direction: str):
        match direction:
            case "l":
                self._x -= 1
            case "r":
                self._x += 1
            case "u":
                self._y -= 1
            case "d":
                self._y += 1

    def heal(self):
        self.__health += 1
        self.__count_medical_kit -= 1

    def add_item_in_pocket(self, item: Item):
        self.__pocket.append(item)

    def is_dead(self):
        return self.__health == 0

    def get_damage(self, damage: int):
        self.__health -= damage

    def attack(self, other_hero: "Hero"):
        other_hero.get_damage(1)

    def pick_item(self, item: Item):
        self.__pocket.append(item)

    def die(self):
        self.__health = 0

    @property
    def pocket(self) -> List[Item]:
        return self.__pocket

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, health: int):
        self.__health = health

    @property
    def name(self) -> str:
        return self.__name

    @property
    def old_direction(self) -> str:
        return self.__old_direction

    @old_direction.setter
    def old_direction(self, direction: str):
        self.__old_direction = direction

    @property
    def count_medical_kit(self) -> int:
        return self.__count_medical_kit

    def to_json(self) -> dict:
        json_str_data = super().to_json()
        json_str_data['name'] = self.__name
        return json_str_data

    def __eq__(self, other: "Hero") -> bool:
        return self.__name == other.__name

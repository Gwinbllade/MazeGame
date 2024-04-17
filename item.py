from game_object import GameObject


class Item(GameObject):
    def __init__(self, x: int, y: int, name: str):
        super().__init__(x, y, "item")
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def to_json(self) -> dict:
        return {
            "x": self._x,
            "y": self._y,
            "name": self.__name
        }

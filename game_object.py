class GameObject:
    def __init__(self, x: int, y: int, object_type: str):
        self._x = x
        self._y = y
        self._object_type = object_type

    @property
    def position(self) -> tuple:
        return self._x, self._y

    @position.setter
    def position(self, position: tuple):
        self._x, self._y = position[0], position[1]

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def object_type(self) -> str:
        return self._object_type

    def to_json(self) -> dict:
        return {
            "x": self._x,
            "y": self._y,
            "object_type": self._object_type,
        }

    def __eq__(self, other: "GameObject") -> bool:
        return self._object_type == other._object_type

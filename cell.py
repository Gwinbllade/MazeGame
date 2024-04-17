from game_object import GameObject


class Cell(GameObject):
    def __init__(self, x: int, y: int, cell_type: str):
        super().__init__(x, y, "cell")
        self.__cell_type = cell_type

    @property
    def cell_type(self) -> str:
        return self.__cell_type

    @cell_type.setter
    def cell_type(self, cell_type: str):
        self.__cell_type = cell_type

    def to_json(self) -> dict:
        json_str_data = super().to_json()
        json_str_data['cell_type'] = self.cell_type
        return json_str_data

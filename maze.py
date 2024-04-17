import json
from typing import List
from cell import Cell
import random

class Maze:
    """Represents the maze in the game."""

    def __init__(self):
        """Initialize the Maze object."""
        self.__game_map = []  # Represents the game map with cells
        self.__coord_fire_cells = []  # Stores coordinates of fire cells

    def get_cell(self, x_or_position, y=None):
        """Get the cell at the specified position.

        Args:
            x_or_position (int or tuple): The x coordinate of the cell or its position as a tuple.
            y (int, optional): The y coordinate of the cell.

        Returns:
            Cell: The cell at the specified position.
        """
        if y is None:
            position = x_or_position
            return self.__game_map[position[1]][position[0]]
        else:
            x = x_or_position
            return self.__game_map[y][x]

    def load_map_from_json(self, cells):
        """Load the maze map from a JSON file.

        Args:
            cells (list): A list of dictionaries representing cell data.
        """
        row_cell_obj = []
        self.__game_map.clear()

        for row_cells_dict in cells:
            row_cell_obj.clear()
            for cell in row_cells_dict:
                row_cell_obj.append(Cell(
                    cell["x"],
                    cell["y"],
                    cell["cell_type"]
                ))
            self.__game_map.append(list(row_cell_obj))

    def init_fire_cells(self):
        """Initialize random cells as fire cells."""
        random_passage_cell = random.sample(self.__get_passage_cell(), 4)
        for cell in random_passage_cell:
            cell.update_cell = "fire"
            self.__coord_fire_cells.append(cell.position)

    def __get_passage_cell(self) -> List[Cell]:
        """Get a list of passage cells in the maze.

        Returns:
            List[Cell]: A list of passage cells.
        """
        passage_cells = []
        for cell_row in self.__game_map:
            for cell in cell_row:
                if cell.cell_type == "passage":
                    passage_cells.append(cell)
        return passage_cells

    def put_out_fire_cell(self):
        """Remove fire cells from the maze."""
        for coord in self.__coord_fire_cells:
            self.get_cell(coord[0], coord[1]).cell_type = "passage"

        self.__coord_fire_cells.clear()

    @property
    def game_map(self):
        """Get the game map."""
        return self.__game_map

    @property
    def coord_fire_cells(self) -> List[tuple]:
        """Get the coordinates of fire cells."""
        return self.__coord_fire_cells

    @property
    def width(self) -> int:
        """Get the width of the maze."""
        return len(self.__game_map[0])

    @property
    def height(self) -> int:
        """Get the height of the maze."""
        return len(self.__game_map)

    def to_json(self):
        """Convert the maze data to JSON format."""
        json_map = []
        for row in self.__game_map:
            json_row = [cell.to_json() for cell in row]
            json_map.append(json_row)

        return json.dumps({
            "game_map": json_map
        })

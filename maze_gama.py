import json
from typing import List

from game_object import GameObject
from maze import Maze
from hero import Hero
from item import Item


def print_line(len_line: int) -> None:
    """
    Prints a line of dashes.

    Args:
        len_line (int): The length of the line to be printed.
    """
    print("-" * len_line)


class MazeGame:
    """Class representing the Maze Game."""

    def __init__(self):
        """Initialize MazeGame object."""
        self.__maze = Maze()
        self.__game_objects = []
        self.__is_end = False
        self.__heroes = self.__set_heroes(0, 3)

    def load_game_map_from_json(self, file_name: str) -> None:
        """
        Loads the game map from a JSON file.

        Args:
            file_name (str): The name of the JSON file containing the game map.
        """
        with open(file_name, "r") as f:
            json_data = json.load(f)

        self.__maze.load_map_from_json(json_data["game_map"])
        self.__game_objects.clear()

        for item in json_data["items"]:
            self.__game_objects.append(Item(item["x"], item["y"], item["name"]))

    @staticmethod
    def __set_heroes(start_x: int, start_y: int) -> List[Hero]:
        """
        Set up heroes.

        Args:
            start_x (int): The starting x-coordinate for the heroes.
            start_y (int): The starting y-coordinate for the heroes.

        Returns:
            List[Hero]: A list of Hero objects.
        """
        heroes = []
        count_heroes = int(input("Enter the number of heroes: "))
        i = 0
        while i < count_heroes:
            hero_name = input(f"Enter the name of hero {i + 1} : ")
            hero = Hero(start_x, start_y, hero_name)
            if hero in heroes:
                print("A hero with this name already exists")
            else:
                heroes.append(hero)
                i += 1

        return heroes

    @staticmethod
    def __is_in_map(position: tuple, height: int, width: int) -> bool:
        """
        Check if a position is within the map boundaries.

        Args:
            position (tuple): The position to check.
            height (int): The height of the map.
            width (int): The width of the map.

        Returns:
            bool: True if the position is within the map boundaries, False otherwise.
        """
        return 0 <= position[0] < width and 0 <= position[1] < height

    @staticmethod
    def __check_hero_returns(current_direction: str, old_direction: str) -> bool:
        """
        Check if the hero is trying to move back in the same direction.

        Args:
            current_direction (str): The current direction the hero is trying to move.
            old_direction (str): The previous direction the hero moved.

        Returns:
            bool: True if the hero is trying to move back in the same direction, False otherwise.
        """
        return_direction = {"l": "r", "r": "l", "u": "d", "d": 'u'}
        if return_direction[current_direction] == old_direction:
            return True
        return False

    @staticmethod
    def __check_win(hero: Hero) -> bool:
        """
        Check if the hero has won.

        Args:
            hero (Hero): The hero to check.

        Returns:
            bool: True if the hero has won, False otherwise.
        """
        key = Item(2, 1, "key")
        if key in hero.pocket:
            return True
        else:
            return False

    def start(self):
        """Start the game."""
        count_round = 1
        while True:
            print(f"\n\n{'-' * 10}ROUND - {count_round}{'-' * 10}")
            self.__round()

            if self.__is_end:
                print("***Game Over***")
                break

            elif len(self.__heroes) == 0:
                print("All heroes have been eliminated from the game")
                break

            count_round += 1

    def __get_cell(self, position: tuple) -> str:
        """
        Get the type of cell at a given position.

        Args:
            position (tuple): The position to check.

        Returns:
            str: The type of cell at the given position.
        """
        if not self.__is_in_map(position, self.__maze.height, self.__maze.width):
            cell_type = "wall"
        else:
            cell_type = self.__maze.get_cell(position).cell_type
        return cell_type

    def __get_game_object(self, hero: Hero) -> List[GameObject]:
        """
        Get game objects at hero's position.

        Args:
            hero (Hero): The hero.

        Returns:
            List[GameObject]: A list of GameObjects at the hero's position.
        """
        object_on_hero_position = []
        for obj in self.__game_objects + self.__heroes:
            if obj.position == hero.position and obj != hero:
                object_on_hero_position.append(obj)
        return object_on_hero_position

    def __collider_with_game_objects(self, hero: Hero):
        """
        Handle collision with game objects.

        Args:
            hero (Hero): The hero.
        """
        for obj in self.__get_game_object(hero):
            if obj.position == hero.position and obj != hero:
                match obj.object_type:
                    case "hero":
                        print(f"Hero {obj.name} at this position")
                    case "item":
                        if obj.name == "heart":
                            hero.health = 5
                            print(f"Hero stepped on a green heart and regained health| Current health: "
                                  f"{hero.health}")
                        else:
                            print(f"Object '{obj.name}' at this position ")

    def __player_action(self, hero: Hero):
        """
        Handle player's action.

        Args:
            hero (Hero): The hero.
        """
        while True:
            action = input("Enter hero's action (l,r,d,u,a,h,p): ")
            match action:
                case "l" | "r" | "d" | "u":
                    self.__hero_move_logic(hero, action)
                    break

                case "h":
                    if self.__hero_heal_logic(hero):
                        break

                case "a":
                    if self.__hero_attack_logic(hero):
                        break

                case "p":
                    if self.__hero_pick_item_logic(hero):
                        break
                case _:
                    print("Invalid input")

    @staticmethod
    def __check_hero_dead(hero: Hero):
        """
        Check if the hero is dead.

        Args:
            hero (Hero): The hero.

        Returns:
            bool: True if the hero is dead, False otherwise.
        """
        if hero.health <= 0:
            return True
        else:
            return False

    def __remove_dead_heroes(self, hero):
        """
        Remove dead heroes from the game.

        Args:
            hero: The hero to remove.
        """
        self.__heroes.remove(hero)

    def __round(self):
        """Start a new round."""
        self.__maze.init_fire_cells()

        for hero in self.__heroes:
            print()
            print_line(30)
            print(f"Burning cells {self.__maze.coord_fire_cells}")
            print(f"Hero {hero.name} is moving ")

            if self.__check_hero_dead(hero):
                print("Hero has 0 health points and is eliminated")
                self.__hero_dead_logic(hero)
                continue

            else:
                self.__player_action(hero)

            if self.__check_hero_dead(hero):
                print("Hero has 0 health points and is eliminated")
                self.__hero_dead_logic(hero)

            print_line(30)

        self.__maze.put_out_fire_cell()

    def __hero_move_logic(self, hero: Hero, direction: str):
        """
        Handle hero's movement logic.

        Args:
            hero (Hero): The hero.
            direction (str): The direction in which the hero wants to move.
        """
        old_cell_type = self.__get_cell(hero.position)
        old_position = hero.position
        hero.move(direction)

        if self.__check_hero_returns(direction, hero.old_direction) and old_cell_type != "extra_passage":
            print(f"{hero.name} got scared and ran away")
            hero.die()
            return

        current_cell_type = self.__get_cell(hero.position)

        match current_cell_type:
            case "wall":
                hero.get_damage(1)
                hero.position = old_position
                print(f"{hero.name} hit the wall, -1 health| Current health: {hero.health}")

            case "fire":
                hero.get_damage(1)
                print(f"{hero.name} is on fire, -1 health| Current health: {hero.health}")

            case "end":
                if self.__check_win(hero):
                    print(f"{hero.name} reached the end and won!!!")
                    self.__is_end = True
                else:
                    print(f"{hero.name} killed by the golem because he didn't have the key")

        print(f"Position of {hero.name} is {hero.position}")

        if current_cell_type != "extra_passage" and hero.position != old_position and old_cell_type != "extra_passage":
            hero.old_direction = direction

        self.__collider_with_game_objects(hero)

    def __hero_heal_logic(self, hero: Hero) -> bool:
        """
        Handle hero's healing logic.

        Args:
            hero (Hero): The hero.

        Returns:
            bool: True if the hero successfully healed, False otherwise.
        """
        if hero.count_medical_kit > 0:
            hero.heal()
            print(
                f"{hero.name} healed| Current health {hero.health} | Medical kits left: "
                f"{hero.count_medical_kit}")
            return True
        else:
            print(f"{hero.name} has no medical kits")
            return False

    def __hero_attack_logic(self, hero: Hero) -> bool:
        """
        Handle hero's attack logic.

        Args:
            hero (Hero): The hero.

        Returns:
            bool: True if the hero successfully attacked, False otherwise.
        """
        game_object_on_hero_position = self.__get_game_object(hero)
        count_damages_heros = 0
        for obj in game_object_on_hero_position:
            if obj.object_type == "hero":
                hero.attack(obj)
                print(f"Hero {hero.name} attacked hero {obj.name}, now his health is {obj.health}")
                count_damages_heros += 1

        if count_damages_heros > 0:
            return True
        else:
            print("There is no one to attack at this position")
            return False

    def __hero_pick_item_logic(self, hero: Hero) -> bool:
        """
        Handle hero's item pick logic.

        Args:
            hero (Hero): The hero.

        Returns:
            bool: True if the hero successfully picked an item, False otherwise.
        """
        game_object_on_hero_position = self.__get_game_object(hero)
        count_pick_obj = 0
        for obj in game_object_on_hero_position:
            if obj.object_type == "item":
                if obj.name == "key":
                    hero.pick_item(obj)
                    self.__game_objects.remove(obj)
                    count_pick_obj += 1
                    print(f"Hero picked up {obj.name}")

        if count_pick_obj > 0:
            return True
        else:
            print("There is nothing to pick up at this position")
            return False

    def __hero_dead_logic(self, hero: Hero):
        """
        Handle dead hero logic.

        Args:
            hero (Hero): The hero who died.
        """
        for item in hero.pocket:
            item.position = hero.position
            print(f"Object '{item.name}' dropped at position {item.position}")
            self.__game_objects.append(item)
        self.__remove_dead_heroes(hero)

    def __save_json(self):
        """Save game state to a JSON file."""
        json_str_game_data = "["
        json_str_game_data += self.__maze.to_json() + ","
        json_str_game_data += self.__save_object_to_json("heroes", self.__heroes) + ","
        json_str_game_data += self.__save_object_to_json("items", self.__game_objects) + "]"
        with open("JSON/save.json", 'w') as file:
            file.write(json_str_game_data)

    def __save_object_to_json(self, obj_collection_name, objects):
        """
        Save a collection of objects to JSON format.

        Args:
            obj_collection_name (str): The name of the object collection.
            objects: The collection of objects to be saved.

        Returns:
            str: The JSON string representing the object collection.
        """
        json_obj = []
        for obj in objects:
            json_obj.append(obj.to_json())
        return json.dumps({
            obj_collection_name: json_obj
        })

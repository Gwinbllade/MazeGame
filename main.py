from maze_gama import MazeGame

if __name__ == '__main__':
    game = MazeGame()
    game.load_game_map_from_json("JSON/game_map.json")
    game.start()

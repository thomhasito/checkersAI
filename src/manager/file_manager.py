import os, json
from data.const import *

class FileManager:

    def __init__(self) -> None:
        self.all_grids = []
        self.start_grid = []
        self.last_move = {}
        self.check_files()


    # Checking Part
    def check_files(self) -> None:
        if not os.path.exists(os.path.dirname(FILE_START_GRID)):
            with open(FILE_START_GRID, "w") as file:
                file.write("")
        if not os.path.exists(os.path.dirname(FILE_ALL_GRIDS)):
            with open(FILE_ALL_GRIDS, "w") as file:
                file.write("")
        if not os.path.exists(os.path.dirname(FILE_LAST_MOVE)):
            with open(FILE_LAST_MOVE, "w") as file:
                file.write("")


    # Loading Part
    def load_start_grid(self) -> None:
        self.start_grid = []
        if os.path.exists(os.path.dirname(FILE_START_GRID)):
            with open(FILE_START_GRID, "r") as fichier:
                grid = fichier.readlines()

            for row in grid:
                if row.strip():
                    row = [int(val) for val in row.strip().split(',')]
                    self.start_grid.append(row)
        else:
            print("File {} not found".format(FILE_START_GRID))

    def load_all_grids(self) -> None:
        self.all_grids = []
        if os.path.exists(os.path.dirname(FILE_ALL_GRIDS)):
            with open(FILE_ALL_GRIDS, "r") as f:
                grids = f.readlines()
            
            current_grid = []

            for grid in grids:
                if grid.strip():
                    row = [int(val) for val in grid.strip().split(',')]
                    current_grid.append(row)

                elif current_grid:
                    self.all_grids.append(current_grid)
                    current_grid = []
        else:
            print("File {} not found".format(FILE_ALL_GRIDS))
    
    def load_last_move(self) -> None:
        self.last_move = {}
        if os.path.exists(os.path.dirname(FILE_LAST_MOVE)):
            if os.path.getsize(FILE_LAST_MOVE) > 0:
                with open(FILE_LAST_MOVE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.last_move = data if data else {}
        else:
            print("File {} not found".format(FILE_LAST_MOVE))


    # Saving Part
    def save_start_grid(self, grid: list) -> None:
        self.delete_start_grid()
        with open(FILE_START_GRID, "w") as file:
            file.write(grid)

    def save_last_grid(self, grid: list) -> None:
        with open(FILE_ALL_GRIDS, "a") as file:
            for row in grid:
                row_file = ",".join(map(str, row))
                file.write(row_file + "\n")
            file.write("\n")

    def save_last_move(self, last_movement: dict) -> None:
        self.delete_last_move()
        if last_movement != {}:
            with open(FILE_LAST_MOVE, "w", encoding="utf-8") as file:
                json.dump(last_movement, file, indent=4, ensure_ascii=False)


    # Deleting Part
    def delete_start_grid(self) -> None:
        with open(FILE_START_GRID, "w", encoding="utf-8") as file:
            file.truncate(0)

    def delete_all_grids(self) -> None:
        with open(FILE_ALL_GRIDS, "w", encoding="utf-8") as file:
            file.truncate(0)

    def delete_last_move(self) -> None:
        with open(FILE_LAST_MOVE, "w", encoding="utf-8") as file:
            file.truncate(0)


    # Getting Part
    def get_start_grid(self) -> list:
        self.load_start_grid()
        return self.start_grid
    
    def get_all_grids(self) -> list:
        self.load_all_grids()
        return self.all_grids
    
    def get_last_move(self) -> dict:
        self.load_last_move()
        return self.last_move
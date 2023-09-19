## Installation

To install the project, simply clone the repository to your machine.

```bash
git clone https://github.com/thomhasito/checkersAI.git
```

## Description

This project is a Python implementation of the classic game of Checkers (Draughts). Challenge yourself to play and defeat the AI opponent. The AI is powered by the MinMax algorithm with Alpha-Beta pruning.

## Game Rules

The game follows the standard rules of Checkers. You can find the complete rules on this website: [http://www.ffjd.fr/Web/index.php?page=reglesdujeu](http://www.ffjd.fr/Web/index.php?page=reglesdujeu)

## Usage

This project is designed to run with Python 3.8 or later. To play the game, simply execute the following command:

```bash
python3 main.py
```

## Project File Structure

The project is organized with the following directory structure:

- `main.py`: The main Python script to start and run the game. (python3.8 or later required)
- README.md
- assets/
  - fonts/
    Empty folder for fonts. Feel free to add your own fonts to this folder.
  - image/
    Warning: The images for the pieces are not mine. I found them on the internet and I do not own them. I decided to not include them in the repository to avoid any illegal issues.
- data/
  - json/
    - `last_move.json`: Contains the last move made by the player. Used for the AI and ensure there is attacks or pawn movements.
  - txt/
    - `start_grid.txt`: Contains the starting grid of the game. Used for board initialisation.
    - `grids.txt`: Contains the grids of the game. Used for detect repetitive positions.
  - `const.py`: Contains all the game's constants for better readability and robustness.
- src/
  - board/
    - `board.py`: Manages the game board and its state.
    - `case.py`: Manages the game board's cases and its state.
    - `piece.py`: Manages the game board's pieces and its state.
    - `player.py`: Initilaize player and ai attributes.
  - display/
    - `button.py`: Class for the game's buttons.
    - `legende.py`: Class for the game's legend.
  - game_phase/
    - `menu.py`: Class for the game's menu. Selection of the player name and the ai difficulty.
    - `game.py`: Class for the game's main loop.
    - `end.py`: Class for the game's end screen.
  - logic/
    - `ai.py`: Contains the AI implementation using the MinMax algorithm with Alpha-Beta pruning.
    - `movement.py`: Functions for the game's attacks and movements.
  - manager/
    - `file_manager.py`: Class for the game's file manager. Save and load the game in txt or json format.
    - `event_manager.py`: Handles the game's events due to mouse or keyboard inputs.

Feel free to explore and modify the code in these files to better understand or enhance the game's functionality.

## Project Status

The project is currently in a completed state, but I am open to receiving pull requests from contributors who may want to enhance the AI algorithm further. Your contributions are welcome and will help make the game even better!

## Contact

You can reach me via email at [thomas.balsalobre@edu.ece.fr
](mailto:)


Feel free to replace `https://github.com/thomhasito/checkersAI.git` with the actual URL of your Git repository when sharing this Markdown file. This Markdown document is written in English and includes sections for installation, project description, game rules, usage instructions, project status, and contact information.

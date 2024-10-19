# 2048 Game

This is a console-based implementation of the popular game **2048**.

## Features

- Play the 2048 game in the terminal using WASD keys.
- Dynamic board creation with customizable size.
- Configurable game settings like the number of tiles generated each turn and win conditions.
- Developer mode with debug messages for detailed logging.

## How to Play

1. Start the game by running the Python script.
2. Use the `W`, `A`, `S`, `D` keys to move the tiles up, left, down, and right respectively.
3. Your goal is to combine tiles to create the tile with the target number (e.g., 2048 or higher based on your settings).
4. If all tiles are filled and no further moves can be made, the game is over.

## Setup and Requirements

- **Python 3.x**
- You may need to install a terminal that supports ANSI colors (or configure your existing terminal).

## Controls

- `W`: Move tiles up
- `A`: Move tiles left
- `S`: Move tiles down
- `D`: Move tiles right

## Game Modes

1. **Developer Mode**: Enable detailed logs and board state while playing.
2. **Customizable Board**: Choose your board size and how many tiles generate each turn.
3. **Win Condition**: Set your own target number for a custom win condition (default is 2048).

## Future Improvements

- AI-based move recommendation (currently, the code can evaluate moves but it's not automated).
- Graphical interface for better playability.


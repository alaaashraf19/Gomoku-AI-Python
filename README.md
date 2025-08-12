# Gomoku Game with Minimax AI

A Python-based Gomoku (Five in a Row) game where a human player competes against an AI opponent. The AI uses the **Minimax algorithm** to choose its moves. The project includes a console-based game engine and an optional GUI interface built on top of it.

## Game Overview

**Gomoku** is a classic strategy board game where two players take turns placing their marks on a grid (commonly 15x15). The first to align five marks in a row—**horizontally, vertically, or diagonally**—wins the game.

In this implementation:
- You can play as the human player against an AI opponent.
- The AI uses a **Minimax search algorithm** with depth limitation for efficient decision-making.

## 🗂Project Structure
```
Gomoku-AI-Python/
│
├── Gomoku.py # Core logic and Minimax-based game engine (also supports console play)
├── GUI.py # GUI version of the game using Pygame (depends on Gomoku.py)
└── README.md # Project documentation
```
## Features

- Console and GUI-based gameplay
- Human vs. AI mode
- AI with Minimax algorithm and depth-limited search
- Visual representation of the board (in console and GUI)

## How It Works

### Game Engine (`Gomoku.py`)
- Manages the game state and board updates
- Checks for win conditions
- Implements the **Minimax algorithm** for AI decision-making
- Accepts input from the user (in console) or GUI
- Returns the AI’s chosen move coordinates and updated board

### GUI Interface (`GUI.py`)
- Built using the **Pygame** library
- Draws a visual board and grid
- Handles mouse events to place human player moves
- Interacts with the game engine to process turns and update graphics

## Input

- Human player:
  - Console version: enter row/column coordinates
  - GUI version: click a grid cell to place a mark
- AI:
  - Automatically responds using the Minimax algorithm

## Output

- The board is updated after each move
  - Console: text-based representation printed after each turn
  - GUI: real-time graphical updates with player and AI moves
- AI’s chosen move is shown on the board

## Requirements

- Python 3.x
- `pygame` library

## Running the Game

### Console Version
```bash
python Gomoku.py
```
### GUI Version
```bash
python GUI.py
```
    




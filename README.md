## How to Run

### Requirements

- Python 3.6 or above
- A terminal that supports the `curses` library (Linux/macOS or compatible terminal on Windows)

### Running the Game

From the terminal, navigate to the project folder and run:

```bash
python3 game.py
```

Ensure your terminal window is wide enough (minimum 80x24 recommended) for proper display.

---

## Menu Navigation

Use the arrow keys (↑ and ↓) to move between options and press Enter to select:

- `Start Game` – begin a new game session
- `Top list` – display the top 10 high scores
- `Quit` – exit the game

---

## Game Controls

| Key        | Function                             |
| ---------- | ------------------------------------ |
| Arrow keys | Move tiles in the desired direction  |
| `r`        | Undo the last move (if lives remain) |
| `q`        | Quit the game and save score         |

---

## Features

- **Name Entry**: At the beginning of each game, you will be asked to enter your name. It will be recorded in the top scores.
- **Redo Function**: You start with 3 lives. Each time you press `r`, a redo consumes one life. Redo is unavailable when lives run out.
- **Top Score List**: Your final score is saved if it ranks in the top 10. These scores are stored in `top_list.txt`.

---

## Files in the Project

| File           | Purpose                                 |
| -------------- | --------------------------------------- |
| `game.py`      | Contains all the game logic             |
| `top_list.txt` | Stores the top 10 scores (auto-created) |
| `README.md`    | Instructions for running and playing    |

---

## Notes

- If arrow keys do not respond, make sure your terminal emulator supports `curses`.
- To reset the top score list, simply delete the `top_list.txt` file.

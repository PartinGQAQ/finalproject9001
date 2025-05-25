# 2048 Terminal Game (Curses Version)

This is a terminal-based implementation of the classic **2048 game**, built using Python's `curses` library. It includes a persistent top score list, player name entry, and redo functionality with limited lives.

---

## 🎮 How to Play

### 🔧 Setup

Make sure you are using Python 3.6+ and your terminal supports `curses`.

### 🛠️ Run the Game

In your terminal, execute:

```bash
python3 game.py
```

> Make sure your terminal window is **wide enough** (e.g., 80x24) to display the grid properly.

---

## 🧑 Main Menu

Navigate using **UP** / **DOWN** arrow keys and confirm with **Enter**:

- `> Start Game <` — Begin a new game.
- `Top list` — View top 10 players by score.
- `Quit` — Exit the program.

---

## 🎲 In-Game Controls

| Key       | Action                            |
| --------- | --------------------------------- |
| `↑ ↓ ← →` | Move tiles up/down/left/right     |
| `r`       | Undo last move (if lives > 0)     |
| `q`       | Quit the game and save your score |

---

## ❤️ Special Features

### ✍️ Name Input

At the start of the game, you'll be prompted to enter your **player name** (up to 20 characters). This is used for the Top List.

### 🧠 Redo Feature

You begin with **3 lives**. Press `r` to redo your last move. If you run out of lives, redo will no longer be available.

> ❗ You’ll see: `NO COINS!💰 Give me more money next time!!` if lives are used up.

### 🏆 Top List

Your score will be saved upon quitting or losing the game. The system maintains the **top 10 scores** in a file named `top_list.txt`.

---

## 📁 Files

| File           | Description                       |
| -------------- | --------------------------------- |
| `game.py`      | Main game logic                   |
| `top_list.txt` | Stores top 10 scores persistently |
| `README.md`    | This instruction file             |

---

## ❓ Troubleshooting

- If arrow keys don't work, ensure you're using a terminal that supports `curses` (e.g., VS Code terminal, macOS Terminal, Ubuntu CLI).
- If characters are not aligned, try resizing your terminal window.

---

## 📜 License

This project is for educational and personal use. Feel free to modify and enhance it!

---

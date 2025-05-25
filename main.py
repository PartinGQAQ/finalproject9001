import copy
import os.path
import random
from enum import Enum
import curses


# Define movement directions as an Enum for clarity and safety
class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


# Load the list of top scores from a local file
def load_top_list():
    """
    Load scores from 'top_list.txt' and return a list of (name, score) pairs.
    """
    if not os.path.exists('top_list.txt'):
        return []

    with open('top_list.txt', 'r') as f:
        lines = f.readlines()
    # Convert each line into a (name, score) tuple
    top_list = []
    for line in lines:
        name, score = line.strip().split(',')
        top_list.append((name, int(score)))
    return top_list


# Write the updated top list back to the file
def write_top_list(top_list):
    with open('top_list.txt', 'w') as f:
        for name, score in top_list:
            f.write(f"{name},{score}\n")


# Add a new (name, score) entry, keep only top 10, and write to file
def update_top_list(name, score):
    top_list = load_top_list()
    top_list.append((name, score))
    top_list.sort(key=lambda x: x[1], reverse=True)
    top_list = top_list[:10]
    write_top_list(top_list)


# Prompt the user to input their name using a curses interface
def display_input_name(stdscr):
    """
    Prompt the user to enter their name using the curses screen.

    :param stdscr: curses screen object
    :return: str, the player's name
    """
    curses.echo()
    stdscr.clear()
    stdscr.addstr(5, 5, "Please enter your name (press Enter to confirm): ")
    stdscr.refresh()

    name = stdscr.getstr(6, 5, 20).decode('utf-8')  # maximum length is 20
    curses.noecho()  # turn off echo
    return name


# Display the main menu and handle user navigation with arrow keys
def display_manu(stdscr):
    num = 0
    info_list = [
        "> Start Game <",
        "Top list",
        "Quit"
    ]
    while True:
        stdscr.clear()
        stdscr.addstr(7, 7, f"{info_list[0]:^15}")
        stdscr.addstr(9, 7, f"{info_list[1]:^15}")
        stdscr.addstr(11, 6, f" {info_list[2]:^15}")
        key = stdscr.getch()

        # Navigate menu using up/down arrows
        if key == curses.KEY_UP:
            info_list[num] = info_list[num][2:-2]
            num -= 1
            num = num % 3
            info_list[num] = "> " + info_list[num] + " <"
            continue
        elif key == curses.KEY_DOWN:
            info_list[num] = info_list[num][2:-2]
            num += 1
            num = num % 3
            info_list[num] = "> " + info_list[num] + " <"
            continue
        # Enter key: trigger action based on selection
        elif key in [curses.KEY_ENTER, 10, 13] and num == 0:
            return "start"
        elif key in [curses.KEY_ENTER, 10, 13]  and num == 2:
            return "quit"
        elif key in [curses.KEY_ENTER, 10, 13]  and num == 1:
            return "toplist"


def display_toplist(stdscr):
    stdscr.clear()
    for i, name in enumerate(load_top_list()):
        stdscr.addstr(i + 5, 1, f"Top {i + 1}:")
        stdscr.addstr(i + 5, 7, f" name: {name[0]}, score: {name[1]}")


# Display the game board and game info using curses text UI
def display_in_curses(stdscr, gameboard):
    stdscr.clear()
    stdscr.addstr(1, 7, "Let's 2048! press")
    stdscr.addstr(2, 7, "Use the arrow keys to play the game\n")
    stdscr.addstr(3, 7, "Press Q to exit \n")
    stdscr.addstr(4, 7, f"You have {gameboard.get_life()} chances to redo, and press R to redo.")
    stdscr.addstr(5, 7, f"Score: {gameboard.score}")

    # different colors of different points
    curses.init_pair(1, curses.COLOR_BLACK, 228)  # 4
    curses.init_pair(2, curses.COLOR_BLACK, 220)  # 8
    curses.init_pair(3, curses.COLOR_BLACK, 214)  # 16
    curses.init_pair(4, curses.COLOR_BLACK, 208)  # 32
    curses.init_pair(5, curses.COLOR_BLACK, 202)  # 64
    curses.init_pair(6, 15, 196)  # 128
    curses.init_pair(7, 15, 160)  # 256
    curses.init_pair(8, 15, 124)  # 512
    curses.init_pair(9, 15, 88)  # 1024
    curses.init_pair(10, 15, 52)  # 2048

    # Display the game grid
    y = 4
    for row in gameboard.board:
        y += 2
        x = 7
        for cell in row:
            if cell == 0:
                color = curses.color_pair(0)
                text = f"{"-":^5}"
            else:
                if cell < 4:
                    color = curses.color_pair(12)
                elif cell < 8:
                    color = curses.color_pair(1)
                elif cell < 16:
                    color = curses.color_pair(2)
                elif cell < 32:
                    color = curses.color_pair(3)
                elif cell < 64:
                    color = curses.color_pair(4)
                elif cell < 128:
                    color = curses.color_pair(5)
                elif cell < 256:
                    color = curses.color_pair(6)
                elif cell < 512:
                    color = curses.color_pair(7)
                elif cell < 1024:
                    color = curses.color_pair(8)
                else:
                    color = curses.color_pair(9)
                # be the center of 5 spaces
                text = f"{cell:^5}"

            stdscr.attron(color)
            stdscr.addstr(y, x, text)
            stdscr.attroff(color)
            x += 7  # column spacing
    stdscr.refresh()


class GameBoard:
    def __init__(self, life = 3, top_list=None):
        """
        Initialize the game board (4x4 grid), score, life counter, and player state.

        :param life: int, number of redo opportunities
        :param top_list: optional list of top player scores
        """
        self.top_list = [] if top_list is None else top_list
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.set_new_point()
        self.set_new_point()
        self.__life = life
        self.score = 0
        self.name = ""

    def set_life(self, life):
        self.__life = life

    def get_life(self):
        return self.__life

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name


    def display(self):
        """
        Print the current game board to the terminal.
        Mainly used for non-curses debugging or testing purposes.
        """
        for row in self.board:
            for cell in row:
                print(cell, end=" " * int(4 - len(str(cell))))
            print("\n")

    def set_new_point(self):
        """
        Randomly place a new '2' tile in one of the empty cells on the board.

        :return: bool, True if a tile was placed, False if no empty cells exist
        """
        cell = []
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    cell.append((x, y))
        if len(cell) == 0:
            return False
        else:
            x, y = random.choice(cell)
            self.board[x][y] = 2
            return True

    def check_is_defeated(self) -> bool:
        """
        Check whether the game is over, i.e., no moves or merges possible.

        :return: bool, True if the game is lost, False otherwise
        """
        flag = True
        # check for any empty cell
        for row in self.board:
            if 0 in row:
                return False
        # check for possible merges
        for i in range(0, 4):
            for j in range(0, 4):
                # right
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                # down
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return flag

    def combine(self, direction):
        """
        Perform the shifting phase of the swipe: move tiles in the specified direction
        without merging. Called before and after the merge phase to compact the grid.

        :param direction: Direction enum (UP, DOWN, LEFT, RIGHT)
        :return: bool, True if any tile was moved
        """
        moved = False
        for _ in range(3):
            if direction == Direction.UP:
                for i in range(3, 0, -1):
                    for j in range(4):
                        if self.board[i - 1][j] == 0 and self.board[i][j] != 0:
                            self.board[i - 1][j] = self.board[i][j]
                            self.board[i][j] = 0
                            moved = True
            elif direction == Direction.DOWN:
                for i in range(0, 3):
                    for j in range(4):
                        if self.board[i + 1][j] == 0 and self.board[i][j] != 0:
                            self.board[i + 1][j] = self.board[i][j]
                            self.board[i][j] = 0
                            moved = True
            elif direction == Direction.LEFT:
                for i in range(3, 0, -1):
                    for j in range(4):
                        if self.board[j][i - 1] == 0 and self.board[j][i] != 0:
                            self.board[j][i - 1] = self.board[j][i]
                            self.board[j][i] = 0
                            moved = True
            elif direction == Direction.RIGHT:
                for i in range(0, 3):
                    for j in range(4):
                        if self.board[j][i + 1] == 0 and self.board[j][i] != 0:
                            self.board[j][i + 1] = self.board[j][i]
                            self.board[j][i] = 0
                            moved = True
        if moved:
            self.score += 10
        return moved

    def swipe(self, command):
        """
        Perform a full move in the specified direction, including merging and compacting.

        Steps:
        1. Shift tiles in the given direction (via combine)
        2. Merge adjacent tiles of equal value
        3. Shift again to fill in any new gaps

        :param command: Direction enum (UP, DOWN, LEFT, RIGHT)
        :return: bool, True if the board state changed
        """
        moved = self.combine(command)
        if command == Direction.UP:
            for i in range(1, 4):
                for j in range(4):
                    if self.board[i][j] == self.board[i - 1][j] and self.board[i][j] != 0:
                        self.board[i - 1][j] *= 2
                        self.board[i][j] = 0
                        moved = True
        elif command == Direction.DOWN:
            for i in range(2, -1, -1):
                for j in range(4):
                    if self.board[i][j] == self.board[i + 1][j] and self.board[i][j] != 0:
                        self.board[i + 1][j] *= 2
                        self.board[i][j] = 0
                        moved = True
        elif command == Direction.LEFT:
            for i in range(1, 4):
                for j in range(4):
                    if self.board[j][i] == self.board[j][i - 1] and self.board[j][i] != 0:
                        self.board[j][i - 1] *= 2
                        self.board[j][i] = 0
                        moved = True
        elif command == Direction.RIGHT:
            for i in range(2, -1, -1):
                for j in range(4):
                    if self.board[j][i] == self.board[j][i + 1] and self.board[j][i] != 0:
                        self.board[j][i + 1] *= 2
                        self.board[j][i] = 0
                        moved = True
        moved = self.combine(command) or moved
        if moved:
            self.score += 5
        return moved


# using original terminal
# game_board = GameBoard()
# while True:
#     game_board.display()
#     command = input("w, a, s, d")
#     if command == "w":
#         game_board.swipe(Direction.UP)
#     if command == "a":
#         game_board.swipe(Direction.LEFT)
#     if command == "d":
#         game_board.swipe(Direction.RIGHT)
#     if command == "s":
#         game_board.swipe(Direction.DOWN)
#     is_new = game_board.set_new_point()
#     print()


def main(stdscr):
    top_list = load_top_list()
    curses.start_color()
    curses.init_pair(12, curses.COLOR_BLACK, 15)
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.bkgd(curses.color_pair(12))
    # save pre_boards to redo it
    pre_board = []
    key = curses.KEY_UNDO

    while True:
        game_board = GameBoard()
        res = display_manu(stdscr)
        if res == "quit":
            return
        elif res == "toplist":
            display_toplist(stdscr)
            stdscr.getch()
            continue
        # start game
        stdscr.clear()
        name = display_input_name(stdscr)
        game_board.set_name(name)
        while True:
            stdscr.clear()
            display_in_curses(stdscr, game_board)
            key = stdscr.getch()
            moved = False
            if key == curses.KEY_UP:
                pre_board.append(copy.deepcopy(game_board))
                moved = game_board.swipe(Direction.UP)
            elif key == curses.KEY_DOWN:
                pre_board.append(copy.deepcopy(game_board))
                moved = game_board.swipe(Direction.DOWN)
            elif key == curses.KEY_RIGHT:
                pre_board.append(copy.deepcopy(game_board))
                moved = game_board.swipe(Direction.RIGHT)
            elif key == curses.KEY_LEFT:
                pre_board.append(copy.deepcopy(game_board))
                moved = game_board.swipe(Direction.LEFT)
            elif key == ord('q'):
                update_top_list(game_board.name, game_board.score)
                break
            # redo the action
            elif key == ord('r'):
                # judge if the user could redo
                if len(pre_board) > 0 and game_board.get_life() > 0:
                    game_board.set_life(game_board.get_life() - 1)
                    game_board.board = pre_board.pop(-1).board
                else:
                    stdscr.addstr(13, 5, "NO COINS!💰 Give me more money next time!!")
                    stdscr.refresh()
                    stdscr.getch()
            if moved:
                game_board.set_new_point()
                if game_board.check_is_defeated():
                    stdscr.clear()
                    stdscr.addstr(10, 10, "💀 Game Over! Press any key to quit.")
                    update_top_list(game_board.name, game_board.score)
                    stdscr.refresh()
                    stdscr.getch()
                    break  # quit


if __name__ == '__main__':
    curses.wrapper(main)

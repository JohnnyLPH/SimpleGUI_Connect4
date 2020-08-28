# Create a Connect 4 game with GUI, includes an AI.
import tkinter
import random
import math
import copy
import sys
import os


game_window = tkinter.Tk()
game_window.title("Connect 4 By JohnnyLPH")


# 1 for playing with AI; 2 for 2 Players Mode.
total_player = 1
# Ranging from 1 - 8. This will be the search depth of minimax function.
ai_difficulty = tkinter.IntVar()


game_mode_frame = tkinter.LabelFrame(game_window, text="Game Mode", padx=5, pady=5)
game_mode_frame.grid(row=0, column=1, padx=10, pady=10)
game_window.resizable(0, 0)


def game_mode():
    global ai_difficulty
    ai_difficulty.set(1)

    # AI mode is chosen, now select either one of 8 difficulties.
    def single_player():
        global total_player
        global ai_difficulty

        total_player = 1
        choose_mode_1 = tkinter.Button(game_mode_frame, text="Single Player", padx=5, pady=2, state="disabled",
                                       relief="sunken", bg="#99ff00")
        choose_mode_2 = tkinter.Button(game_mode_frame, text="Two Players", padx=5, pady=2, command=two_player)
        choose_ai2 = tkinter.Label(game_mode_frame, text="AI Difficulty =")
        choose_difficulty2 = tkinter.OptionMenu(game_mode_frame, ai_difficulty, 1, 2, 3, 4, 5, 6, 7, 8)

        choose_mode_1.grid(row=0, column=0, padx=3)
        choose_mode_2.grid(row=0, column=1, padx=3)
        choose_ai2.grid(row=1, column=0, padx=3, sticky="e")
        choose_difficulty2.grid(row=1, column=1, padx=3, sticky="w")

    def two_player():
        global total_player
        total_player = 2

        choose_mode_1 = tkinter.Button(game_mode_frame, text="Single Player", padx=5, pady=2, command=single_player)
        choose_mode_2 = tkinter.Button(game_mode_frame, text="Two Players", padx=5, pady=2, state="disabled",
                                       relief="sunken", bg="#99ff00")
        choose_ai2 = tkinter.Label(game_mode_frame, text="AI Difficulty =", state="disabled")
        choose_difficulty2 = tkinter.OptionMenu(game_mode_frame, ai_difficulty, 1, 2, 3, 4, 5, 6, 7, 8)
        choose_difficulty2.configure(state="disabled", relief="flat")

        choose_mode_1.grid(row=0, column=0, padx=3)
        choose_mode_2.grid(row=0, column=1, padx=3)
        choose_ai2.grid(row=1, column=0, padx=3, sticky="e")
        choose_difficulty2.grid(row=1, column=1, padx=3, sticky="w")

    choose_mode1 = tkinter.Button(game_mode_frame, text="Single Player", padx=5, pady=2, state="disabled",
                                  relief="sunken", bg="#99ff00")
    choose_mode2 = tkinter.Button(game_mode_frame, text="Two Players", padx=5, pady=2, command=two_player)
    choose_ai = tkinter.Label(game_mode_frame, text="AI Difficulty =")
    choose_difficulty = tkinter.OptionMenu(game_mode_frame, ai_difficulty, 1, 2, 3, 4, 5, 6, 7, 8)

    choose_mode1.grid(row=0, column=0, padx=3)
    choose_mode2.grid(row=0, column=1, padx=3)
    choose_ai.grid(row=1, column=0, padx=3, sticky="e")
    choose_difficulty.grid(row=1, column=1, padx=3, sticky="w")

    return


# There are 7 columns and 6 rows in game.
# Each list represents a COLUMN not ROW.
game_grid = [
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "]
]


frame_1 = tkinter.LabelFrame(game_window, text="Connect 4 Game Board", padx=5, pady=5, bg="black", fg="white")
frame_1.grid(row=0, column=0, padx=10, pady=10, rowspan=6)


def show_grid(grid):
    frame_row = -1

    for row in range(5, -1, -1):
        frame_row += 1

        frame_col = -1
        for column in grid:
            frame_col += 1

            block = tkinter.Canvas(frame_1, width=59, height=59, bg="blue")
            block.grid(row=frame_row, column=frame_col)

            if column[row] == "x":
                disc_colour = "red"
            elif column[row] == "o":
                disc_colour = "yellow"
            else:
                disc_colour = "white"

            y_coord, x_coord, rad = 31, 31, 25
            block.create_oval(x_coord - rad, y_coord - rad, x_coord + rad, y_coord + rad, fill=disc_colour, outline="")

    for number in range(7):
        col_button2 = tkinter.Button(frame_3, text=f"{number + 1}", padx=19, pady=5, state="disabled")
        col_button2.grid(row=0, column=number, padx=5, pady=10)

    return


def find_non_full_col(grid):
    col_list = []

    for num in range(7):
        if " " in grid[num]:
            col_list.append(num)

    return col_list


# 1 for Player 1 (x); 2 for AI or Player 2 (o)
# Refers to run_whole_program(), for Player 1 to start the game first, the value needs to be 2. Reverse for Player 2.
current_player_num = random.choice([1, 2])


def fill_disc(grid, col_num, player_num):
    index_num = grid[int(col_num)].index(" ")

    if player_num == 1:
        grid[int(col_num)][index_num] = "x"
    else:
        grid[int(col_num)][index_num] = "o"

    return


def win_game(grid, last_player_num):
    if last_player_num == 1:
        player_disc = "x"
    else:
        player_disc = "o"

    for column in range(7):
        for row in range(6):
            # Check only blocks that are filled with either x or o.
            if grid[column][row] != player_disc:
                continue

            # Check horizontal. Only for column 1 to 4 // [0 - 3].
            if column <= 3:
                if grid[column][row] == grid[column + 1][row] == grid[column + 2][row] == grid[column + 3][row]:
                    return True

            # Check vertical. Only for row 1 to 3 // [0 - 2]
            if row <= 2:
                if grid[column][row] == grid[column][row + 1] == grid[column][row + 2] == grid[column][row + 3]:
                    return True

            # Check diagonal (Towards Top Right). Only for column 1 to 4 // [0 - 3] and row 1 to 3 // [0 - 2]
            if column <= 3 and row <= 2:
                if grid[column][row] == grid[column + 1][row + 1] == grid[column + 2][row + 2] == \
                        grid[column + 3][row + 3]:
                    return True

            # Check diagonal (Towards Top Left). Only for column 4 to 7 // [3 - 6] and row 1 to 3 // [0 - 2]
            if column >= 3 and row <= 2:
                if grid[column][row] == grid[column - 1][row + 1] == grid[column - 2][row + 2] == \
                        grid[column - 3][row + 3]:
                    return True

    return False


frame_2 = tkinter.LabelFrame(game_window, text="Game Info", padx=5, pady=5)  # For guiding players.
frame_2.grid(row=1, column=1, rowspan=6, padx=10, pady=10, sticky="news")
frame_3 = tkinter.LabelFrame(game_window, text="Choose Column", padx=5, pady=5)  # For players to choose column.
frame_3.grid(row=6, column=0, padx=10, pady=10, sticky="ew")


def player_input(grid):
    def player_fill(col):
        fill_disc(grid, col, current_player_num)
        run_whole_program()

    # Refer to what is displayed in the game grid.
    if 0 in find_non_full_col(grid):  # Button for column 1.
        col_button = tkinter.Button(frame_3, text=f"{0 + 1}", padx=19, pady=5, command=lambda: player_fill(0))
        col_button.grid(row=0, column=0, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{0 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=0, padx=5, pady=10)

    if 1 in find_non_full_col(grid):  # Button for column 2.
        col_button = tkinter.Button(frame_3, text=f"{1 + 1}", padx=19, pady=5, command=lambda: player_fill(1))
        col_button.grid(row=0, column=1, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{1 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=1, padx=5, pady=10)

    if 2 in find_non_full_col(grid):  # Button for column 3.
        col_button = tkinter.Button(frame_3, text=f"{2 + 1}", padx=19, pady=5, command=lambda: player_fill(2))
        col_button.grid(row=0, column=2, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{2 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=2, padx=5, pady=10)

    if 3 in find_non_full_col(grid):  # Button for column 4.
        col_button = tkinter.Button(frame_3, text=f"{3 + 1}", padx=19, pady=5, command=lambda: player_fill(3))
        col_button.grid(row=0, column=3, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{3 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=3, padx=5, pady=10)

    if 4 in find_non_full_col(grid):  # Button for column 5.
        col_button = tkinter.Button(frame_3, text=f"{4 + 1}", padx=19, pady=5, command=lambda: player_fill(4))
        col_button.grid(row=0, column=4, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{4 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=4, padx=5, pady=10)

    if 5 in find_non_full_col(grid):  # Button for column 6.
        col_button = tkinter.Button(frame_3, text=f"{5 + 1}", padx=19, pady=5, command=lambda: player_fill(5))
        col_button.grid(row=0, column=5, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{5 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=5, padx=5, pady=10)

    if 6 in find_non_full_col(grid):  # Button for column 7.
        col_button = tkinter.Button(frame_3, text=f"{6 + 1}", padx=19, pady=5, command=lambda: player_fill(6))
        col_button.grid(row=0, column=6, padx=5, pady=10)
    else:
        col_button = tkinter.Button(frame_3, text=f"{6 + 1}", padx=19, pady=5, state="disabled")
        col_button.grid(row=0, column=6, padx=5, pady=10)

    return


def window_score(window, ai_num):
    # 3 discs together with 1 empty block, + 5 for AI, - 4 for opponent.
    # 2 discs together with 2 empty blocks, + 2 for AI, - 1 for opponent.
    score = 0

    # AI plays as Player 1.
    if ai_num == 1:
        ai_disc = "x"
        opponent_disc = "o"
    # AI plays as Player 2.
    else:
        ai_disc = "o"
        opponent_disc = "x"

    # 3 discs and 2 discs for AI.
    if window.count(ai_disc) == 3 and window.count(" ") == 1:
        score += 5
    elif window.count(ai_disc) == 2 and window.count(" ") == 2:
        score += 2

    # 3 discs and 2 discs for opponent.
    if window.count(opponent_disc) == 3 and window.count(" ") == 1:
        score -= 4
    elif window.count(opponent_disc) == 2 and window.count(" ") == 2:
        score -= 1

    return score


# Count score for horizontal, vertical and diagonal lines.
def find_score(grid, ai_num):
    score = 0

    # AI plays as Player 1.
    if ai_num == 1:
        ai_disc = "x"
    # AI plays as Player 2.
    else:
        ai_disc = "o"

    # Bonus for middle column: + (Filled blocks // 3) scores.
    middle_column = grid[3]
    middle_count = middle_column.count(ai_disc)
    score += (middle_count // 3)

    # Check horizontal score // check every row.
    for row in range(6):
        row_content = []

        for col in grid:
            row_content.append(col[row])

        # Check 4 columns each time. Check until the 4th column only.
        for check in range(4):
            horizontal_line_window = row_content[check:(check + 4)]

            score += window_score(horizontal_line_window, ai_num)

    # Check vertical score // check every column.
    for col in grid:
        # Check 4 rows each time. Check until the 3th row only.
        for check in range(3):
            vertical_line_window = col[check:(check + 4)]

            score += window_score(vertical_line_window, ai_num)

    # Check diagonal score (towards right).
    # Check until 3th row only.
    for row in range(3):
        # Check until 4th column only.
        for col in range(4):
            diagonal_window = [grid[col + i][row + i] for i in range(4)]

            score += window_score(diagonal_window, ai_num)

    # Check diagonal score (towards left).
    # Check until 3th row only.
    for row in range(3):
        # Check from 4th column until the last column.
        for col in range(4):
            diagonal_window = [grid[col + i][row + 3 - i] for i in range(4)]

            score += window_score(diagonal_window, ai_num)

    return score


# Terminal node means the game is end at this point.
def is_terminal_node(grid):
    return win_game(grid, 1) or win_game(grid, 2) or len(find_non_full_col(grid)) == 0


# Minimax plus Alpha-Beta pruning.
def minimax(grid, ai_num, depth, alpha, beta, maximizing_player):
    inner_col_list = find_non_full_col(grid)
    is_terminal = is_terminal_node(grid)

    if ai_num == 1:
        opponent_num = 2
    else:
        opponent_num = 1

    if depth == 0 or is_terminal:
        if is_terminal:
            if win_game(grid, ai_num):  # AI wins here.
                win_score = 1000 + depth
                return None, win_score
            elif win_game(grid, opponent_num):  # Opponent wins here.
                win_score = -1000 - depth
                return None, win_score
            else:  # Game is a draw.
                return None, 0
        else:  # Reaching 0 depth.
            return None, find_score(grid, ai_num)

    if maximizing_player:  # Maximizing AI score.
        value = -math.inf
        column = random.choice(inner_col_list)

        for col in inner_col_list:
            inner_grid = copy.deepcopy(grid)
            fill_disc(inner_grid, col, ai_num)

            new_score = minimax(inner_grid, ai_num, depth - 1, alpha, beta, False)[-1]

            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return column, value
    else:  # Minimizing opponent score.
        value = math.inf
        column = random.choice(inner_col_list)

        for col in inner_col_list:
            inner_grid = copy.deepcopy(grid)
            fill_disc(inner_grid, col, opponent_num)

            new_score = minimax(inner_grid, ai_num, depth - 1, alpha, beta, True)[-1]

            if new_score < value:
                value = new_score
                column = col

            beta = min(beta, value)

            if alpha >= beta:
                break

        return column, value


move_num = 0


def run_whole_program():
    global current_player_num
    global frame_2
    global move_num

    while True:
        show_grid(game_grid)
        game_window.update()

        if current_player_num == 1:
            player_name = "Player 1"
        else:
            if total_player == 1:
                player_name = "AI"
            else:
                player_name = "Player 2"

        if win_game(game_grid, current_player_num) is True:  # Winner is born.
            frame_2.destroy()
            frame_2 = tkinter.LabelFrame(game_window, text="Game Info", padx=5, pady=5)  # For guiding players.
            frame_2.grid(row=1, column=1, rowspan=6, padx=10, pady=10, sticky="news")

            reminder_choose_mode = tkinter.Label(frame_2, text="Game Ends!!!")
            reminder_choose_mode2 = tkinter.Label(frame_2, text=f"Total Moves = {move_num}")
            reminder_choose_mode3 = tkinter.Label(frame_2, text=f"Game Winner = {player_name}")
            reminder_choose_mode4 = tkinter.Label(frame_2, text="\nYou can choose to play another")
            reminder_choose_mode5 = tkinter.Label(frame_2, text="game by pressing Reset Game")
            reminder_choose_mode6 = tkinter.Label(frame_2, text="button or close the window to")
            reminder_choose_mode7 = tkinter.Label(frame_2, text="terminate the program.")

            reminder_choose_mode.grid(row=0, column=0, sticky="w")
            reminder_choose_mode2.grid(row=1, column=0, sticky="w")
            reminder_choose_mode3.grid(row=2, column=0, sticky="w")
            reminder_choose_mode4.grid(row=3, column=0, sticky="w")
            reminder_choose_mode5.grid(row=4, column=0, sticky="w")
            reminder_choose_mode6.grid(row=5, column=0, sticky="w")
            reminder_choose_mode7.grid(row=6, column=0, sticky="w")
            return

        if len(find_non_full_col(game_grid)) == 0:  # Game is a draw.
            frame_2.destroy()
            frame_2 = tkinter.LabelFrame(game_window, text="Game Info", padx=5, pady=5)  # For guiding players.
            frame_2.grid(row=1, column=1, rowspan=6, padx=10, pady=10, sticky="news")

            reminder_choose_mode = tkinter.Label(frame_2, text="Game Ends!!!")
            reminder_choose_mode2 = tkinter.Label(frame_2, text=f"Total Moves = {move_num}")
            reminder_choose_mode3 = tkinter.Label(frame_2, text="Game Winner = DRAW")
            reminder_choose_mode4 = tkinter.Label(frame_2, text="\nYou can choose to play another")
            reminder_choose_mode5 = tkinter.Label(frame_2, text="game by pressing Reset Game")
            reminder_choose_mode6 = tkinter.Label(frame_2, text="button or close the window to")
            reminder_choose_mode7 = tkinter.Label(frame_2, text="terminate the program.")

            reminder_choose_mode.grid(row=0, column=0, sticky="w")
            reminder_choose_mode2.grid(row=1, column=0, sticky="w")
            reminder_choose_mode3.grid(row=2, column=0, sticky="w")
            reminder_choose_mode4.grid(row=3, column=0, sticky="w")
            reminder_choose_mode5.grid(row=4, column=0, sticky="w")
            reminder_choose_mode6.grid(row=5, column=0, sticky="w")
            reminder_choose_mode7.grid(row=6, column=0, sticky="w")
            return

        # If the game didn't end, proceed to the next player turn.
        if current_player_num == 1:
            current_player_num = 2
        else:
            current_player_num = 1

        # For refreshing frame_2 [Game Info].
        if current_player_num == 1:
            player_name = "Player 1"
            disc_colour = "red"
        else:
            if total_player == 1:
                player_name = "AI"
            else:
                player_name = "Player 2"
            disc_colour = "yellow"

        move_num += 1
        frame_2.destroy()
        frame_2 = tkinter.LabelFrame(game_window, text="Game Info", padx=5, pady=5)  # For guiding players.
        frame_2.grid(row=1, column=1, rowspan=6, padx=10, pady=10, sticky="news")

        player_info = tkinter.Label(frame_2, text=f"Current Turn = {player_name}")
        player_info2 = tkinter.Label(frame_2, text=f"Current Move = {move_num} of 42")
        player_info.grid(row=0, column=0, columnspan=2, sticky="w")
        player_info2.grid(row=1, column=0, columnspan=2, sticky="w")

        player_info3 = tkinter.Label(frame_2, text="Player's Disc =")
        player_info3.grid(row=2, column=0, sticky="w")
        player_disc = tkinter.Canvas(frame_2, width=59, height=59)
        player_disc.grid(row=2, column=1, sticky="w")
        player_disc.create_oval(31 - 25, 31 - 25, 31 + 25, 31 + 25, fill=disc_colour, outline="")

        reminder_choose_mode6 = tkinter.Label(frame_2, text="\nReminder:")
        reminder_choose_mode7 = tkinter.Label(frame_2, text="-The program is definitely still")
        reminder_choose_mode8 = tkinter.Label(frame_2, text=" running even if it is not")
        reminder_choose_mode9 = tkinter.Label(frame_2, text=" responding so don't close it.")

        reminder_choose_mode6.grid(row=3, column=0, columnspan=2, sticky="w")
        reminder_choose_mode7.grid(row=4, column=0, columnspan=2, sticky="w")
        reminder_choose_mode8.grid(row=5, column=0, columnspan=2, sticky="w")
        reminder_choose_mode9.grid(row=6, column=0, columnspan=2, sticky="w")

        game_window.update()

        # Player 1's turn.
        if current_player_num == 1:
            player_input(game_grid)
            return

        # Player 2's turn.
        if total_player == 2 and current_player_num == 2:
            player_input(game_grid)
            return

        # AI's turn.
        if total_player == 1 and current_player_num == 2:
            final_col_score_tuple = minimax(game_grid, 2, ai_difficulty.get(), -math.inf, math.inf, True)

            fill_disc(game_grid, final_col_score_tuple[0], 2)
            continue


def restart_program():
    game_mode()
    show_grid(game_grid)

    def start_g():
        if total_player == 1:
            choose_mode2 = tkinter.Button(game_mode_frame, text="Two Players", padx=5, pady=2)
            choose_ai = tkinter.Label(game_mode_frame, text="AI Difficulty =")
            choose_difficulty = tkinter.OptionMenu(game_mode_frame, ai_difficulty, 1, 2, 3, 4, 5, 6, 7, 8)

            choose_mode2.configure(state="disabled")
            choose_ai.configure(state="disabled")
            choose_difficulty.configure(state="disabled", relief="sunken", bg="#99ff00")
            choose_mode2.grid(row=0, column=1, padx=3)
            choose_ai.grid(row=1, column=0, padx=3, sticky="e")
            choose_difficulty.grid(row=1, column=1, padx=3, sticky="w")
        else:
            choose_mode1 = tkinter.Button(game_mode_frame, text="Single Player", padx=5, pady=2)

            choose_mode1.configure(state="disabled")
            choose_mode1.grid(row=0, column=0, padx=3)

        start_game2 = tkinter.Button(game_mode_frame, text="Start Game", state="disabled", relief="sunken")
        reset_game2 = tkinter.Button(game_mode_frame, text="Reset Game", command=reset_g, bg="#ff0000", fg="#ffffff")
        start_game2.grid(row=2, column=0, padx=3)
        reset_game2.grid(row=2, column=1, padx=3)
        run_whole_program()

    def reset_g():  # Restart the whole program.
        os.execl(sys.executable, sys.executable, *sys.argv)

    start_game = tkinter.Button(game_mode_frame, text="Start Game", command=start_g, bg="#99ff00", fg="black")
    reset_game = tkinter.Button(game_mode_frame, text="Reset Game", state="disabled")
    start_game.grid(row=2, column=0, padx=3)
    reset_game.grid(row=2, column=1, padx=3)

    reminder_choose_mode = tkinter.Label(frame_2, text="Choose a Game Mode above,")
    reminder_choose_mode2 = tkinter.Label(frame_2, text="then press Start Game button.")
    reminder_choose_mode3 = tkinter.Label(frame_2, text="\nFor Single Player Mode:")
    reminder_choose_mode4 = tkinter.Label(frame_2, text="-AI needs more time to make a")
    reminder_choose_mode5 = tkinter.Label(frame_2, text=" move at higher AI Difficulty.")
    reminder_choose_mode6 = tkinter.Label(frame_2, text="\nReminder:")
    reminder_choose_mode7 = tkinter.Label(frame_2, text="-The program is definitely still")
    reminder_choose_mode8 = tkinter.Label(frame_2, text=" running even if it is not")
    reminder_choose_mode9 = tkinter.Label(frame_2, text=" responding so don't close it.")

    reminder_choose_mode.grid(row=0, column=0, sticky="w")
    reminder_choose_mode2.grid(row=1, column=0, sticky="w")
    reminder_choose_mode3.grid(row=2, column=0, sticky="w")
    reminder_choose_mode4.grid(row=3, column=0, sticky="w")
    reminder_choose_mode5.grid(row=4, column=0, sticky="w")
    reminder_choose_mode6.grid(row=5, column=0, sticky="w")
    reminder_choose_mode7.grid(row=6, column=0, sticky="w")
    reminder_choose_mode8.grid(row=7, column=0, sticky="w")
    reminder_choose_mode9.grid(row=8, column=0, sticky="w")

    # Center the window on screen.
    game_window.update_idletasks()

    window_width = game_window.winfo_reqwidth()
    window_height = game_window.winfo_reqheight()
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    x_coord = int((screen_width / 2) - (window_width / 2))
    y_coord = int((screen_height / 2) - (window_height / 2))

    game_window.geometry(f"+{x_coord}+{y_coord}")

    game_window.mainloop()
    return


restart_program()


# This program is COMPLETED. Date : 16/7/2020 12:57 PM

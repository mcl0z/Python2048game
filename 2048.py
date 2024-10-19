from random import *
import os
import msvcrt
import ctypes
import time

# Initialize the board
board = []
possible_values = [0, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 8]
_debug_ = True
new_tile_count = 1
n = 4  # Default board size is 4x4

# Define color list (for reuse)
colors = [
    "\033[94m",  # Blue
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[91m",  # Red
    "\033[95m",  # Purple
    "\033[96m",  # Cyan
    "\033[31m",  # Dark Red
    "\033[32m",  # Dark Green
    "\033[33m",  # Dark Yellow
    "\033[34m",  # Dark Blue
    "\033[35m",  # Dark Purple
    "\033[36m",  # Dark Cyan
    "\033[37m",  # White
]

# Dynamically create an n*n board
def create_board():
    global board
    board = [[0 for _ in range(n)] for _ in range(n)]

def create():
    for i in range(n):
        for j in range(n):
            board[i][j] = possible_values[randint(0, 11)]
            if(_debug_):
                print("creating game.. at" + "(" + str(i) +"," + str(j) + ")")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print the board and add RGB color to each number
def print_2048():
    clear_screen()
    for i in range(n):
        row = ""
        for j in range(n):
            value = board[i][j]
            color = color_map.get(value, color_map[0])  # Get the corresponding RGB color, default to gray
            row += color + f"{value:4}" + color_map['reset'] + " "  # Add color and reset
        print(row)
    if _debug_:
        print("Printed \n Geted RGB")

# Move Up
def up():
    for j in range(n):
        for i in range(1, n):
            if board[i][j] != 0: 
                k = i
                while k > 0 and board[k-1][j] == 0:
                    board[k-1][j], board[k][j] = board[k][j], 0
                    k -= 1
                if k > 0 and board[k-1][j] == board[k][j]: 
                    board[k-1][j] *= 2
                    board[k][j] = 0
    print_2048()

# Move Down
def down():
    for j in range(n):
        for i in range(n-2, -1, -1):
            if board[i][j] != 0:
                k = i
                while k < n-1 and board[k+1][j] == 0:
                    board[k+1][j], board[k][j] = board[k][j], 0
                    k += 1
                if k < n-1 and board[k+1][j] == board[k][j]: 
                    board[k+1][j] *= 2
                    board[k][j] = 0
    print_2048()

# Move Left
def left():
    for i in range(n): 
        for j in range(1, n):
            if board[i][j] != 0:
                k = j
                while k > 0 and board[i][k-1] == 0: 
                    board[i][k-1], board[i][k] = board[i][k], 0
                    k -= 1
                if k > 0 and board[i][k-1] == board[i][k]: 
                    board[i][k-1] *= 2
                    board[i][k] = 0
    print_2048()

# Move Right
def right():
    for i in range(n):
        for j in range(n-2, -1, -1):
            if board[i][j] != 0:
                k = j
                while k < n-1 and board[i][k+1] == 0:
                    board[i][k+1], board[i][k] = board[i][k], 0
                    k += 1
                if k < n-1 and board[i][k+1] == board[i][k]:
                    board[i][k+1] *= 2
                    board[i][k] = 0
    print_2048()

# Move function
def move(way):
    if way == "w":
        up()
        if _debug_:
            print("Moved up")
    elif way == "s":
        down()
        if _debug_:
            print("Moved down")
    elif way == "a":
        left()
        if _debug_:
            print("Moved left")
    elif way == "d":
        right()
        if _debug_:
            print("Moved right")

# Generate a new random tile
def create_new_one():
    for i in range(new_tile_count):
        temp_1 = randint(0, n-1)
        temp_2 = randint(0, n-1)
        temp_3 = possible_values[randint(0, 11)]
        if board[temp_1][temp_2] != 0:
            continue
        else:
            board[temp_1][temp_2] = temp_3
            if _debug_:
                print(f"At ({temp_1+1}, {temp_2+1}) Created val = {temp_3}")

win_number = 0

# Check if the player wins
def check_win():
    for i in range(n):
        for j in range(n):
            if board[i][j] >= win_number:
                return True
    return False

# Check if the game is over
def check_game_over():
    occupied_tiles = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                occupied_tiles += 1
    return occupied_tiles == n*n

# Evaluate move based on number of empty spaces, smoothness, maximum tile position, etc.
def evaluate_move(direction):
    temp_board = [row[:] for row in board]  # Copy the current board
    move(direction)  # Simulate the move

    # Evaluation criteria
    score = 0

    # 1. Calculate number of empty spaces
    empty_spaces = sum(row.count(0) for row in board)
    score += empty_spaces * 10  # Add weight to empty spaces

    # 2. Smoothness evaluation (smaller difference between adjacent tiles is better)
    smoothness = 0
    for i in range(n):
        for j in range(n-1):
            smoothness -= abs(board[i][j] - board[i][j+1])  # Horizontal difference
            smoothness -= abs(board[j][i] - board[j+1][i])  # Vertical difference
    score += smoothness

    # 3. Max tile position (prefer max tile in the corner)
    max_tile = max(max(row) for row in board)
    if board[0][0] == max_tile:
        score += 100  # Reward if the max tile is in the top-left corner

    # 4. Merge opportunities (reward moves that merge more tiles)
    merges = 0
    for i in range(n):
        for j in range(n-1):
            if board[i][j] == board[i][j+1]:
                merges += 1  # Horizontal merge
            if board[j][i] == board[j+1][i]:
                merges += 1  # Vertical merge
    score += merges * 5

    # Restore the original board
    board[:] = temp_board
    return score

# Choose the best move
def best_move():
    directions = ['w', 'a', 's', 'd']
    best_direction = None
    best_score = -float('inf')
    
    for direction in directions:
        score = evaluate_move(direction)
        if score > best_score:
            best_score = score
            best_direction = direction
            
    return best_direction

# Game Start
print("2048 By Mcl")
temp_debug = input("Continue as a developer? (entry y/n) ")
_debug_ = temp_debug.lower() == 'y'

n = int(input("Enter the board size n: "))
if _debug_:
    print("n set")
new_tile_count = int(input("How many random numbers to generate each time: "))
if _debug_: 
    print("new_tile_count set")
win_number = int(input("Set the number that triggers a win: "))
if _debug_:
    print("win_number set")

print("Main start")
# Dynamically generate color_map from 2^1 to 2^20
color_map = {0: "\033[90m"}  # 0 is default gray
for i in range(1, 21):
    color_map[2**i] = colors[(i - 1) % len(colors)]  # Loop through the color list
    if(_debug_):
        print("Color "+str(i)+" Loaded!")

color_map['reset'] = "\033[0m"  # Reset color
if(_debug_):
    print("Color Set!")

def getchar():
    return msvcrt.getch().decode('utf-8')

create_board()
create()

if _debug_:
    print("Create 2048 Successful")

print_2048()
tries = 0
print("Checking...")
time.sleep(0.1)
print("Done")
print("Game will start after 1 sec")
time.sleep(1)
won = False

while True:
    # Get user input for movement
    print("PRESS W/A/S/D: ")
    char = getchar()
    move(char)
    tries += 1
    create_new_one()

    if check_win():
        print_2048()
        if not won:
            print('YOU WON 2048!!!')
            print("After " + str(tries) + " tries")
            input("Press Enter to continue")
            won = True
    if check_game_over():
        print_2048()
        print('YOU LOSE 2048!!!')
        print("After " + str(tries) + " tries")
        break

input("Press Enter to exit")

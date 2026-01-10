import numpy as np
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Game board settings for Four Connect (7 columns and 6 rows)
ROWS = 6
COLUMNS = 7

# Initialize a new game board
def create_new_board():
    return np.zeros((ROWS, COLUMNS))

# Check if the column is full
def is_valid_location(board, col):
    return board[0][col] == 0

# Find the next available row in the column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

# Drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if the current player won
def winning_move(board, piece):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Bot makes a move by selecting a random valid column
def bot_move(board):
    valid_locations = [col for col in range(COLUMNS) if is_valid_location(board, col)]
    return random.choice(valid_locations)

# Initialize a global variable for the game board and turn
game_board = create_new_board()
turn = 0  # 0 is for player, 1 is for bot

@app.route('/new_game', methods=['POST'])
def new_game():
    global game_board, turn
    game_board = create_new_board()
    turn = 0  # Player starts first
    return jsonify({"message": "New game started", "board": game_board.tolist()})

@app.route('/player_move', methods=['POST'])
def player_move():
    global game_board, turn

    # Get the player's move from request
    data = request.json
    column = data.get('column')

    if not is_valid_location(game_board, column):
        return jsonify({"error": "Invalid move. Column is full."}), 400

    # Player is always piece 1
    row = get_next_open_row(game_board, column)
    drop_piece(game_board, row, column, 1)

    if winning_move(game_board, 1):
        return jsonify({"message": "Player wins!", "board": game_board.tolist()})

    # Now it's the bot's turn
    bot_column = bot_move(game_board)
    bot_row = get_next_open_row(game_board, bot_column)
    drop_piece(game_board, bot_row, bot_column, 2)

    if winning_move(game_board, 2):
        return jsonify({"message": "Bot wins!", "board": game_board.tolist()})

    return jsonify({"message": "Move successful", "player_move": column, "bot_move": bot_column, "board": game_board.tolist()})

if __name__ == '__main__':
    app.run(debug=True)

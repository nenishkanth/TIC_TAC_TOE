from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Game Board
board = ['' for _ in range(9)]  # Empty board

# Minimax Algorithm for AI Move
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "X":  # Player wins
        return -1
    elif winner == "O":  # AI wins
        return 1
    elif is_board_full(board):  # Tie
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

# AI Move Function
def best_move():
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == '':
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

# Check for a Winner
def check_winner(board):
    # Winning combinations
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]
    return None

# Check if the Board is Full
def is_board_full(board):
    return '' not in board

# Route to Render the Main Page
@app.route('/')
def index():
    return render_template('index.html')

# Route to Reset the Board
@app.route('/reset', methods=['POST'])
def reset_board():
    global board
    board = ['' for _ in range(9)]  # Reset board
    return jsonify({'status': 'success'})

# Route for Player Move
@app.route('/move', methods=['POST'])
def player_move():
    global board
    data = request.get_json()
    position = data['position']
    position = int(position)  # Convert position to integer
    board[position] = "X"     # Update the board with the player's move


    # Check if the player wins
    if check_winner(board) == "X":
        return jsonify({'winner': 'X'})

    # Check if the game is a tie
    if is_board_full(board):
        return jsonify({'winner': 'tie'})

    # AI makes its move
    ai_position = best_move()
    board[ai_position] = "O"

    # Check if the AI wins
    if check_winner(board) == "O":
        return jsonify({'ai_position': ai_position, 'winner': 'O'})

    # Check for a tie again
    if is_board_full(board):
        return jsonify({'ai_position': ai_position, 'winner': 'tie'})

    # Continue the game
    return jsonify({'ai_position': ai_position, 'winner': None})

if __name__ == '__main__':
    app.run(debug=True)

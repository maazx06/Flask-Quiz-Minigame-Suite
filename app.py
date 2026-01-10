import sys
import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from random import choice

# Initialize the Flask application
app = Flask(__name__)

# Get the absolute path to the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure the database directory exists
os.makedirs(os.path.join(basedir, "db"), exist_ok=True)

# Configure the database URIs with an absolute path and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/default.db')  # Default database URI
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///' + os.path.join(basedir, 'db/UserDB.db'),
    'quiz': 'sqlite:///' + os.path.join(basedir, 'db/quiz.db')
}
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define the Users model for the users table in the UserDB.db database
class Users(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define the Question model for the questions table in the quiz.db database
class Question(db.Model):
    __bind_key__ = 'quiz'
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, nullable=False)
    question_type = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    options = db.Column(db.String)  # Store as JSON string for multiple choice
    answer = db.Column(db.String, nullable=False)

# Route for the index page which renders the login page    
@app.route('/')
def index():
    return render_template('login_page.html')

# Route for displaying the signup form
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# Helper function to validate email
def is_valid_email(email):
    return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None

# Helper function to validate password
def validate_password_strength(password):
    min_length = 8
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'[0-9]', password)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    if len(password) < min_length:
        return "Password must be at least 8 characters long."
    if not has_upper:
        return "Password must contain at least one uppercase letter."
    if not has_lower:
        return "Password must contain at least one lowercase letter."
    if not has_digit:
        return "Password must contain at least one number."
    if not has_special:
        return "Password must contain at least one special character."

    return None

# Route for handling user signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    # Check if the email is valid
    if not is_valid_email(username):
        flash("Invalid email address.", "error")
        return render_template('signup.html')
    
    # Check if the password is strong enough
    validation_error = validate_password_strength(password)
    if validation_error:
        flash(validation_error, "error")
        return render_template('signup.html')

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    # Check if the username already exists
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        flash("Username already exists.", "error")
        return render_template('signup.html')
    
    # Create a new user
    new_user = Users(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('quiz_selection'))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while adding the user.", "error")
        return render_template('signup.html')

# Route for handling user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()
    
    if user is None or not check_password_hash(user.password, password):
        show_popup("Incorrect email or password.")
        return redirect(url_for('index'))

    session['user_id'] = user.id
    return redirect(url_for('quiz_selection'))

def show_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Login Error", message)
    root.destroy()

@app.route('/quiz_selection')
def quiz_selection():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('index'))
    return render_template('quiz_selection.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    subject = request.form['subject']
    question = get_next_question(subject)
    if question:
        return render_template('quiz_page.html', subject=subject, question=question)
    else:
        flash("No questions available for this subject.", "error")
        return redirect(url_for('quiz_selection'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    question_id = request.form['question_id']
    user_answer = request.form['answer'].strip().lower()

    question = Question.query.filter_by(id=question_id).first()
    correct_answer = question.answer.strip().lower()

    if user_answer == correct_answer:
        next_question = get_next_question(question.subject, question_id)
        if next_question:
            return render_template('quiz_page.html', subject=question.subject, question=next_question)
        else:
            return redirect(url_for('minigame_selection'))
    else:
        flash("Incorrect answer, please try again.", "error")
        return render_template('quiz_page.html', subject=question.subject, question=question)

def get_next_question(subject, current_question_id=None):
    if current_question_id:
        question = Question.query.filter(Question.subject == subject, Question.id > current_question_id).first()
    else:
        question = Question.query.filter_by(subject=subject).first()
    
    if question:
        return {
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'options': json.loads(question.options) if question.options else [],
            'answer': question.answer
        }
    return None

# Route for selecting a minigame
@app.route('/minigame_selection')
def minigame_selection():
    return render_template('minigame_selection.html')

# Route for handling minigame selection
@app.route('/start_minigame', methods=['POST'])
def start_minigame():
    selected_game = request.form['minigame']
    if selected_game == "four_connect":
        return redirect(url_for('four_connect'))
    elif selected_game == "hangman":
        return redirect(url_for('hangman'))
    elif selected_game == "rock_paper_scissors":
        return redirect(url_for('rock_paper_scissors'))
    else:
        flash("Invalid minigame selection.", "error")
        return redirect(url_for('minigame_selection'))

# ---------- Four Connect Game API ----------

ROWS = 6
COLUMNS = 7

def create_new_board():
    return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

def is_valid_location(board, col):
    col = int(col)  # Ensure column is an integer
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

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

def bot_move(board):
    valid_locations = [col for col in range(COLUMNS) if is_valid_location(board, col)]
    if not valid_locations:
        return None  # No valid locations left
    return choice(valid_locations)

game_board = create_new_board()

@app.route('/new_game', methods=['POST'])
def new_game():
    global game_board
    game_board = create_new_board()
    return jsonify({"message": "New game started", "board": game_board})

@app.route('/player_move', methods=['POST'])
def player_move():
    global game_board

    try:
        data = request.json
        column = int(data.get('column'))  # Ensure column is an integer

        if not is_valid_location(game_board, column):
            return jsonify({"error": "Invalid move. Column is full."}), 400

        # Player move (always player 1)
        row = get_next_open_row(game_board, column)
        drop_piece(game_board, row, column, 1)

        if winning_move(game_board, 1):
            return jsonify({"message": "Player wins!", "board": game_board})

        # Bot move (always bot is player 2)
        bot_column = bot_move(game_board)
        bot_row = get_next_open_row(game_board, bot_column)
        drop_piece(game_board, bot_row, bot_column, 2)

        if winning_move(game_board, 2):
            return jsonify({"message": "Bot wins!", "board": game_board})

        # Return successful moves
        return jsonify({
            "message": "Move successful",
            "player_move": column,
            "bot_move": bot_column,
            "board": game_board
        })
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ---------- End of Four Connect Game API ----------

# Route for Four Connect
@app.route('/four_connect')
def four_connect():
    return render_template('four_connect.html')

# Route for Rock Paper Scissors
@app.route('/rock_paper_scissors')
def rock_paper_scissors():
    return render_template('rock_paper_scissors.html')

# Route for Hangman
@app.route('/hangman')
def hangman():
    return render_template('hangman.html')

# Function to run the Flask app in a separate thread
def run_flask():
    with app.app_context():
        db.create_all()
    app.run(debug=False, threaded=True, use_reloader=False)

# PyQt application class
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Flask App in PyQt")
        self.setGeometry(100, 100, 1280, 720)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/"))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.exit_app)
        layout.addWidget(exit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def exit_app(self):
        print("Exiting application...")
        os._exit(0)

# Run Flask app in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Run the PyQt application
qt_app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(qt_app.exec_())

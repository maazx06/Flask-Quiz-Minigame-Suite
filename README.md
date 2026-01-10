# Flask Quiz & Minigame Suite

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![PyQt5](https://img.shields.io/badge/PyQt-5-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 Overview

This project is a hybrid desktop-web application that combines an educational quiz platform with an arcade of classic minigames. Built using **Flask** for the backend and **PyQt5** for a native desktop window wrapper, the application offers a seamless user experience. It features secure user authentication, database-driven quizzes, and interactive games powered by Python and JavaScript.

## ✨ Features

### 🔐 User Authentication
- **Secure Signup/Login:** Users can create accounts with password strength validation.
- **Security:** Passwords are hashed using `werkzeug.security` (PBKDF2 SHA256) before storage.
- **Session Management:** Flask sessions are used to track logged-in users.

### 🧠 Quiz Module
- **Subject Selection:** Users can choose from Computer Science, Product Design, or Psychology.
- **Dynamic Questions:** Questions are fetched from a SQLite database (`quiz.db`).
- **Feedback Loop:** Instant validation of answers with "Win/Try Again" logic.

### 🎮 Minigame Arcade
- **Four Connect:** Play against a bot in this grid-based strategy game. Logic is handled server-side using NumPy.
- **Rock Paper Scissors:** A quick-fire game implemented with client-side JavaScript.
- **Hangman:** interactive word guessing game with visual updates.

### 🖥️ Technical Architecture
- **Hybrid Interface:** The app runs a local Flask server (`127.0.0.1:5000`) within a PyQt5 `QWebEngineView`, mimicking a native desktop app.
- **Database:** Uses `SQLAlchemy` with multiple SQLite database binds (`UserDB` and `quiz`).

## 🛠️ Technologies Used

* **Backend:** Python, Flask, SQLAlchemy
* **Frontend:** HTML5, CSS3, JavaScript
* **GUI Wrapper:** PyQt5 (QtWebEngineWidgets)
* **Data Processing:** NumPy (for game logic)
* **Database:** SQLite

## 📂 Project Structure

```text
├── app.py                  # Main application logic, routes, and PyQt wrapper
├── db/                     # SQLite Databases
│   ├── UserDB.db           # Stores user credentials
│   └── quiz.db             # Stores quiz questions and answers
├── templates/              # HTML Templates (Jinja2)
│   ├── login_page.html     # User login
│   ├── quiz_selection.html # Subject selection
│   ├── four_connect.html   # Connect 4 game interface
│   └── ...                 # Other templates
└── static/
    └── css/                # Custom Stylesheets
        ├── LPstyles.css    # Login page styles
        └── SPstyles.css    # Signup page styles

import tkinter as tk
from random import choice

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.word = choice(["PYTHON", "FLASK", "QUIZ"]).upper()  # The word being guessed
        self.guesses = ""
        self.max_attempts = 6
        self.attempts = 0
        self.create_widgets()

    def create_widgets(self):
        # Exit button
        exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        exit_button.pack(side=tk.BOTTOM, pady=10)

        # Frame for the word display
        top_frame = tk.Frame(self.master)
        top_frame.pack(padx=20, pady=20)

        # Display the word to be guessed as underscores
        self.word_display = tk.StringVar()
        self.word_display.set("_ " * len(self.word))
        self.label = tk.Label(top_frame, textvariable=self.word_display, font=("Helvetica", 24))
        self.label.pack()


        # Frame for letter buttons arranged in a triangular grid
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=20)

        # Create letter buttons grid including all required letters for the word
        letters = set("ARBZTIEXOYPNDWVSUME")  # Initial letters from the image
        letters.update(self.word)  # Ensure all letters from the word are included
        letters = sorted(letters)  # Sort the letters to display them in a structured way
        
        # We now have enough positions for all the letters
        positions = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), 
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), 
            (3, 2), (3, 3), (3, 4) 
        ]

        self.buttons = {}
        for i, letter in enumerate(letters):
            button = tk.Button(self.buttons_frame, text=letter, width=4, height=2,
                               command=lambda l=letter: self.guess(l), bg="lightblue")
            self.buttons[letter] = button
            row, col = positions[i]
            button.grid(row=row, column=col, padx=5, pady=5)

    def guess(self, letter):
        letter = letter.upper()
        if letter in self.word and letter not in self.guesses:
            self.guesses += letter
            display_word = " ".join([l if l in self.guesses else "_" for l in self.word])
            self.word_display.set(display_word)
            if "_" not in display_word:
                self.label.config(text="You Win!", fg="green")
                self.disable_buttons()
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.label.config(text=f"You lose! The word was {self.word}", fg="red")
                self.disable_buttons()

    def disable_buttons(self):
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

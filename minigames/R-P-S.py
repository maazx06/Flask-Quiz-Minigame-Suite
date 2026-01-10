import tkinter as tk
from random import choice
from tkinter.font import Font

class RockPaperScissorsGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Rock Paper Scissors Game")
        self.master.configure(bg='#002366')

        self.options = ["Rock", "Paper", "Scissors"]
        self.user_score = 0
        self.computer_score = 0

        self.create_widgets()

    def create_widgets(self):
        # Exit button
        exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        exit_button.pack(side=tk.BOTTOM, pady=10)
    
        title_frame = tk.Frame(self.master, bg='#002366')
        title_frame.pack(pady=10)
        title_label = tk.Label(title_frame, text="Rock Paper Scissors Game", fg="white", bg="#002366", font=Font(size=24, weight='bold'))
        title_label.pack()
        
        score_frame = tk.Frame(self.master, bg='#002366')
        score_frame.pack(pady=10)
        
        self.player_label = tk.Label(score_frame, text="Player: 0", fg="white", bg="#002366", font=Font(size=14))
        self.player_label.pack(side=tk.LEFT, padx=50)
        
        self.computer_label = tk.Label(score_frame, text="Computer: 0", fg="white", bg="#333333", font=Font(size=14))
        self.computer_label.pack(side=tk.RIGHT, padx=50)
        
        button_frame = tk.Frame(self.master, bg='#002366')
        button_frame.pack(pady=20)

        self.rock_button = tk.Button(button_frame, text="✊", command=lambda: self.play("Rock"), font=Font(size=36), bg="white", width=5)
        self.rock_button.pack(side=tk.LEFT, padx=10)

        self.paper_button = tk.Button(button_frame, text="✋", command=lambda: self.play("Paper"), font=Font(size=36), bg="white", width=5)
        self.paper_button.pack(side=tk.LEFT, padx=10)

        self.scissors_button = tk.Button(button_frame, text="✌️", command=lambda: self.play("Scissors"), font=Font(size=36), bg="white", width=5)
        self.scissors_button.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(self.master, text="Make Your Selection", fg="black", bg="white", font=Font(size=18))
        self.result_label.pack(pady=20)

        restart_button = tk.Button(self.master, text="Restart Game", command=self.restart_game, font=Font(size=14), bg="white")
        restart_button.pack(pady=10)

    def play(self, user_choice):
        self.user_choice = user_choice
        self.computer_choice = choice(self.options)
        result = self.determine_winner()
        self.update_scores(result)
        self.result_label.config(text=f"You chose {self.user_choice}. Computer chose {self.computer_choice}. {result}")

    def determine_winner(self):
        if self.user_choice == self.computer_choice:
            return "It's a tie!"
        elif (self.user_choice == "Rock" and self.computer_choice == "Scissors") or \
             (self.user_choice == "Paper" and self.computer_choice == "Rock") or \
             (self.user_choice == "Scissors" and self.computer_choice == "Paper"):
            return "You win!"
        else:
            return "You lose!"

    def update_scores(self, result):
        if "win" in result:
            self.user_score += 1
            self.player_label.config(text=f"Player: {self.user_score}")
        elif "lose" in result:
            self.computer_score += 1
            self.computer_label.config(text=f"Computer: {self.computer_score}")

    def restart_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.player_label.config(text="Player: 0")
        self.computer_label.config(text="Computer: 0")
        self.result_label.config(text="Make Your Selection")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()

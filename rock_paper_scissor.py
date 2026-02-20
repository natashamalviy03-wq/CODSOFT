import tkinter as tk
from tkinter import messagebox
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scrissor")
        self.root.geometry("500x650")
        self.root.configure(bg="#1a1a1a")

        self.user_score = 0
        self.computer_score = 0
        self.target_score = 3  
        self.choices = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}

        self.setup_ui()

    def setup_ui(self):
        #Header
        tk.Label(self.root, text="LET'S PLAY", font=("Impact", 32), 
                 fg="#00d4ff", bg="#1a1a1a").pack(pady=10)
        
        tk.Label(self.root, text="First 3 wins the trophy!", font=("Arial", 10), 
                 fg="#888", bg="#1a1a1a").pack()
        
        #score
        self.score_label = tk.Label(self.root, text="You: 0  |  Computer: 0", 
                                    font=("Consolas", 22, "bold"), fg="white", bg="#333")
        self.score_label.pack(fill="x", padx=50, pady=15)

        #area
        self.arena_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.arena_frame.pack(pady=20)

        self.user_move_label = tk.Label(self.arena_frame, text="?", font=("Segoe UI Emoji", 80), 
                                        fg="#ff007f", bg="#1a1a1a", width=3)
        self.user_move_label.grid(row=0, column=0)

        tk.Label(self.arena_frame, text="VS", font=("Impact", 40), fg="white", bg="#1a1a1a").grid(row=0, column=1, padx=20)

        self.cpu_move_label = tk.Label(self.arena_frame, text="?", font=("Segoe UI Emoji", 80), 
                                       fg="#00d4ff", bg="#1a1a1a", width=3)
        self.cpu_move_label.grid(row=0, column=2)

        # Round Winner Display
        self.winner_banner = tk.Label(self.root, text="READY?", font=("Arial", 22, "bold"), 
                                      fg="#aaa", bg="#1a1a1a", pady=10)
        self.winner_banner.pack()

        # Select Buttons
        self.btn_container = tk.Frame(self.root, bg="#1a1a1a")
        self.btn_container.pack(pady=20)

        self.choice_btns = []
        for name, emoji in self.choices.items():
            btn = tk.Button(self.btn_container, text=f"{emoji}\n{name}", font=("Arial", 12, "bold"),
                            width=8, height=3, bg="#333", fg="white", activebackground="#444",
                            command=lambda n=name: self.start(n))
            btn.pack(side="left", padx=10)
            self.choice_btns.append(btn)

        self.next_round_btn = tk.Button(self.root, text="NEW MATCH", font=("Arial", 10, "bold"), 
                                        bg="#ff4b2b", fg="white", width=20, height=2,
                                        command=self.reset)
        self.next_round_btn.pack(side="bottom", pady=40)

    def start(self, user_choice):
        
        if self.user_score == self.target_score or self.computer_score == self.target_score:
            return

        cpu_choice = random.choice(list(self.choices.keys()))
        
        self.user_move_label.config(text=self.choices[user_choice])
        self.cpu_move_label.config(text=self.choices[cpu_choice])

        if user_choice == cpu_choice:
            result = "ROUND TIE!"
            color = "#ffd700" 
        elif (user_choice == "Rock" and cpu_choice == "Scissors") or \
             (user_choice == "Paper" and cpu_choice == "Rock") or \
             (user_choice == "Scissors" and cpu_choice == "Paper"):
            result = "YOUR SCORE! 🎉"
            color = "#2ecc71"
            self.user_score += 1
        else:
            result = "Computer SCORE! 🤖"
            color = "#e74c3c"
            self.computer_score += 1

        #round winner
        self.winner_banner.config(text=result, fg=color)
        self.score_label.config(text=f"You: {self.user_score}  |  Computer: {self.computer_score}")

        if self.user_score == self.target_score:
            self.root.after(500, lambda: self.end_tournament("🏆 WINNER : YOU!"))
        elif self.computer_score == self.target_score:
            self.root.after(500, lambda: self.end_tournament("🏆 WINNER : Computer"))

    def end_tournament(self, message):
        self.winner_banner.config(text=message, fg="#00d4ff")
        messagebox.showinfo("Tournament Over", message)
        for btn in self.choice_btns:
            btn.config(state="disabled")

    def reset(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_move_label.config(text="?")
        self.cpu_move_label.config(text="?")
        self.winner_banner.config(text="READY?", fg="#aaa")
        self.score_label.config(text="You: 0  |  Computer: 0")
        for btn in self.choice_btns:
            btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = Game(root)
    root.mainloop()

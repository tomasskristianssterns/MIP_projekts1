import random
import time
import ttkbootstrap as ttk
from tkinter import messagebox

# Skaitļu ģenerēšana (kas dalās ar 2, 3, 4)
def numbers_random_generator():
    numbers = []
    while len(numbers) < 5:
        num = random.randint(20000, 30000)
        if num % 2 == 0 and num % 3 == 0 and num % 4 == 0:
            numbers.append(num)
    return numbers

# Spēles klase
class Game:
    def __init__(self, number):
        self.now_number = number
        self.player_points = 0
        self.ai_points = 0
        print(f"Game started with number: {self.now_number}")

    def move(self, divisor, is_human):
        """Izpilda gājienu, dalot skaitli un piešķirot punktus"""
        if self.now_number % divisor == 0:
            new_number = self.now_number // divisor
            if new_number % 2 == 0:
                if is_human:
                    self.ai_points -= 1
                else:
                    self.player_points += 1
            else:
                if is_human:
                    self.player_points += 1
                else:
                    self.ai_points += 1
            self.now_number = new_number
            return True
        return False

    def heuristic(self):
        return self.player_points - self.ai_points
    
# Min Max algoritms izveidots dali ar ChatGPT dali ar savām zināšānām
    def Minimax(self, depth, is_maximizing):
        if self.now_number <= 10 or depth == 0:
            print(f"Minimax called: now_number={self.now_number}, depth={depth}, is_max={is_maximizing}")
            return self.heuristic()

        moving_variants = [2, 3, 4]
        best_value = float('-infinity') if is_maximizing else float('infinity')
        move_found = False

        for move in moving_variants:
            if self.now_number % move == 0:
                if move not in [2,3,4]:
                    print(f"Kļūda! Nepareizs dalītājs: {move} priekš {self.now_number}")
                else:
                    print(f"Pareizs gājiens: {self.now_number} ÷ {move} = {self.now_number // move}")
                move_found = True
                new_state = Game(self.now_number // move)  # Izveidojam jaunu spēles stāvokli
                new_state.player_points = self.player_points
                new_state.ai_points = self.ai_points
                new_state.move(move, is_maximizing)

                eval = new_state.Minimax(depth - 1, not is_maximizing)
                best_value = max(best_value, eval) if is_maximizing else min(best_value, eval)

        return best_value if move_found else self.heuristic()
    
# Alpha Bet algoritms izveidots dali ar ChatGPT dali ar savām zināšānām
    def Alpha_Beta(self, depth, alpha, beta, is_maximizing):
        if self.now_number <= 10 or depth == 0:
            print(f"Alpha-Beta: now={self.now_number}, depth={depth}, alpha={alpha}, beta={beta}, is_max={is_maximizing}")
            return self.heuristic()

        moving_variants = [2, 3, 4]
        move_found = False

        if is_maximizing:
            max_eval = float('-infinity')
            for move in moving_variants:
                if self.now_number % move == 0:
                    if move not in [2,3,4]:
                        print(f"Kļūda! Nepareizs dalītājs: {move} priekš {self.now_number}")
                    else:
                        print(f"Pareizs gājiens: {self.now_number} ÷ {move} = {self.now_number // move}")
                    move_found = True
                    new_state = Game(self.now_number // move)
                    new_state.player_points = self.player_points
                    new_state.ai_points = self.ai_points
                    new_state.move(move, True)

                    eval = new_state.Alpha_Beta(depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval if move_found else self.heuristic()
        else:
            min_eval = float('infinity')
            for move in moving_variants:
                if self.now_number % move == 0:
                    if move not in [2,3,4]:
                        print(f"Kļūda! Nepareizs dalītājs: {move} priekš {self.now_number}")
                    else:
                        print(f"Pareizs gājiens: {self.now_number} ÷ {move} = {self.now_number // move}")
                    move_found = True
                    new_state = Game(self.now_number // move)
                    new_state.player_points = self.player_points
                    new_state.ai_points = self.ai_points
                    new_state.move(move, False)

                    eval = new_state.Alpha_Beta(depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval if move_found else self.heuristic()

class GameGUI:
  def set_algorithm(self, algo):
        self.algorithm = algo
        self.status_label.config(text=f"Izvēlēts algoritms: {algo}")

  def start_game(self, player_starts):
        self.game = Game(self.selected_number.get())
        self.player_turn = player_starts
        self.update_status()
        if not self.player_turn:
            self.ai_move()

  def player_move(self, divisor):
        if self.game.move(divisor, True):
            self.player_turn = False
            self.update_status()
            if self.game.now_number > 10:
                self.ai_move()
        else:
            messagebox.showerror("Kļūda", "Nevar dalīt šo skaitli ar " + str(divisor))
# Simulē AI domāšanu no ChatGPT
  def ai_move(self):
        time.sleep(1)  
        best_move = None
        best_value = float('-inf')

        for move in [2, 3, 4]:
            if self.game.now_number % move == 0:
                new_state = Game(self.game.now_number)
                new_state.player_points, new_state.ai_points = self.game.player_points, self.game.ai_points
                new_state.move(move, False)

                eval = (new_state.Minimax if self.algorithm == "Minimax" else new_state.Alpha_Beta)(new_state, 3, float('-inf'), float('inf'), False)
                if eval > best_value:
                    best_value = eval
                    best_move = move

        if best_move:
            self.game.move(best_move, False)
            self.player_turn = True
            self.update_status()
# no ChatGPT
  def update_status(self):
        self.status_label.config(text=f"Skaitlis: {self.game.now_number} | Spēlētāja punkti: {self.game.player_points} | AI punkti: {self.game.ai_points}")

        if self.game.now_number <= 10:
            winner = "Neizšķirts!" if self.game.player_points == self.game.ai_points else "Tu uzvarēji!" if self.game.player_points > self.game.ai_points else "AI uzvarēja!"
            messagebox.showinfo("Spēle beigusies", winner)
# no ChatGPT
  def restart_game(self):
        self.start_numbers = numbers_random_generator()
        self.create_widgets()

# Palaist spēli
def start_minimax():
    print("Minimax algoritms izvēlēts")
    state = Game(random.choice(numbers_random_generator()))
    result = state.Minimax(34, True)
    print("Minimax rezultāts:", result)

def start_alpha_beta():
    print("Alpha-Beta algoritms izvēlēts")
    state = Game(random.choice(numbers_random_generator()))
    result = state.Alpha_Beta(34, float('-inf'), float('inf'), True)
    print("Alpha-Beta rezultāts:", result)

# Tkinter UI logs
app = ttk.Window()
app.geometry("400x300")

label = ttk.Label(app, text="Izvēlies algoritmu")
label.pack(pady=30)
label.config(font=("Arial", 20, "bold"))

button_frame = ttk.Frame(app)
button_frame.pack(pady=50, padx=80, fill="x")

ttk.Button(button_frame, text="Min-Max", bootstyle="primary", command=start_minimax).pack(side="left", padx=10)
ttk.Button(button_frame, text="Alpha-Beta", bootstyle="success", command=start_alpha_beta).pack(side="right", padx=10)

app.mainloop()

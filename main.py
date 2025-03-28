import random
import time
import ttkbootstrap as ttk  # https://ttkbootstrap.readthedocs.io/en/latest/
from tkinter import messagebox  # https://docs.python.org/3/library/tkinter.messagebox.html

# === Spēles koka mezgls ===
# Izmantojam, lai reprezentētu katru iespējamo spēles stāvokli
# https://en.wikipedia.org/wiki/Game_tree
class GameTreeNode:
    def __init__(self, number, player_points=0, ai_points=0):
        self.number = number
        self.player_points = player_points
        self.ai_points = ai_points
        self.children = []

    def generate_children(self):
        for move in [2, 3, 4]:
            if self.number % move == 0:
                new_number = self.number // move
                child = GameTreeNode(new_number, self.player_points, self.ai_points)
                self.children.append(child)

# === Funkcija, kas ģenerē sākotnējos skaitļus, kuri dalās ar 2, 3 un 4 ===
# Šādi mēs nodrošinām, ka visām darbībām ir jēga spēles sākumā
def generate_valid_numbers():
    numbers = []
    while len(numbers) < 5:
        num = random.randint(20000, 30000)  # https://docs.python.org/3/library/random.html
        if num % 2 == 0 and num % 3 == 0 and num % 4 == 0:
            numbers.append(num)
    return numbers

# === Spēles loģikas klase ===
# Šeit tiek ieviesti visi noteikumi, kustības un AI algoritmi
class Game:
    def __init__(self, number):
        self.now_number = number
        self.player_points = 0
        self.ai_points = 0
        self.visited_nodes = 0
        self.start_time = time.time()

    # Lietotāja vai AI gājiens
    def move(self, divisor, is_human):
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

    # Heiristikas funkcija, kas nosaka stāvokļa vērtību
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
    def heuristic(self):
        return self.player_points - self.ai_points

    # Minimax algoritms (bez griešanas)
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-implementation/
    def minimax(self, depth, is_maximizing):
        self.visited_nodes += 1
        if self.now_number <= 10 or depth == 0:
            return self.heuristic()

        best_value = float('-inf') if is_maximizing else float('inf')
        for move in [2, 3, 4]:
            if self.now_number % move == 0:
                new_state = Game(self.now_number // move)
                new_state.player_points = self.player_points
                new_state.ai_points = self.ai_points
                new_state.move(move, is_maximizing)
                eval = new_state.minimax(depth - 1, not is_maximizing)
                best_value = max(best_value, eval) if is_maximizing else min(best_value, eval)
        return best_value

    # Alfa-beta griešana — optimizēts minimax
    # https://www.geeksforgeeks.org/practical-implementation-of-alpha-beta-pruning/
    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        self.visited_nodes += 1
        if self.now_number <= 10 or depth == 0:
            return self.heuristic()

        if is_maximizing:
            max_eval = float('-inf')
            for move in [2, 3, 4]:
                if self.now_number % move == 0:
                    new_state = Game(self.now_number // move)
                    new_state.player_points = self.player_points
                    new_state.ai_points = self.ai_points
                    new_state.move(move, True)
                    eval = new_state.alpha_beta(depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Griešana
            return max_eval
        else:
            min_eval = float('inf')
            for move in [2, 3, 4]:
                if self.now_number % move == 0:
                    new_state = Game(self.now_number // move)
                    new_state.player_points = self.player_points
                    new_state.ai_points = self.ai_points
                    new_state.move(move, False)
                    eval = new_state.alpha_beta(depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

# === Lietotāja saskarne ar ttkbootstrap (Tkinter uzlabotā versija) ===
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.algorithm = "Minimax"
        self.start_numbers = generate_valid_numbers()

        # Paziņojums par algoritma izvēli
        self.status_label = ttk.Label(root, text="Izvēlieties sākotnējo skaitli un algoritmu")
        self.status_label.pack(padx=10, pady=10)

        self.create_selection_screen()

    def create_selection_screen(self):
        self.selection_frame = ttk.Frame(self.root)
        self.selection_frame.pack(padx=10, pady=10)

        self.label = ttk.Label(self.selection_frame, text="Izvēlies sākotnējo skaitli un algoritmu")
        self.label.grid(row=0, column=0, columnspan=2)

        self.start_number_label = ttk.Label(self.selection_frame, text="Sākotnējais skaitlis:")
        self.start_number_label.grid(row=1, column=0, padx=5, pady=5)

        self.start_number_option = ttk.Combobox(self.selection_frame, values=self.start_numbers)
        self.start_number_option.grid(row=1, column=1, padx=5, pady=5)
        self.start_number_option.set(self.start_numbers[0])

        self.algorithm_label = ttk.Label(self.selection_frame, text="Izvēlieties algoritmu:")
        self.algorithm_label.grid(row=2, column=0, padx=5, pady=5)

        self.algorithm_option = ttk.Combobox(self.selection_frame, values=["Minimax", "Alfa-beta"])
        self.algorithm_option.grid(row=2, column=1, padx=5, pady=5)
        self.algorithm_option.set("Minimax")

        self.start_button = ttk.Button(self.selection_frame, text="Sākt spēli", command=self.start_game_from_selection)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

    def start_game_from_selection(self):
        number = int(self.start_number_option.get())
        algorithm = self.algorithm_option.get()
        self.set_algorithm(algorithm)
        self.selection_frame.destroy()
        self.start_game(number, player_starts=True)

    def set_algorithm(self, algo):
        self.algorithm = algo
        self.status_label.config(text=f"Izvēlēts algoritms: {algo}")

    def start_game(self, number, player_starts):
        self.game = Game(number)
        self.player_turn = player_starts
        self.create_game_screen()
        self.update_status()
        if not self.player_turn:
            self.ai_move()

    def create_game_screen(self):
        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)

        self.status_label = ttk.Label(self.game_frame, text="Spēles sākums")
        self.status_label.grid(row=0, column=0, columnspan=3)

        self.move_buttons = []
        for i, move in enumerate([2, 3, 4]):
            button = ttk.Button(self.game_frame, text=f"Dalīt ar {move}", command=lambda move=move: self.player_move(move))
            button.grid(row=1, column=i)
            self.move_buttons.append(button)

    def player_move(self, divisor):
        if self.game.move(divisor, True):
            self.player_turn = False
            self.update_status()
            if self.game.now_number > 10:
                self.ai_move()
        else:
            messagebox.showerror("Kļūda", f"Nevar dalīt šo skaitli ar {divisor}")

    def ai_move(self):
        time.sleep(1)
        best_move = None
        best_value = float('-inf')
        start_time = time.time()

        for move in [2, 3, 4]:
            if self.game.now_number % move == 0:
                new_state = Game(self.game.now_number)
                new_state.player_points = self.game.player_points
                new_state.ai_points = self.game.ai_points
                new_state.move(move, False)

                if self.algorithm == "Minimax":
                    eval = new_state.minimax(3, False)
                else:
                    eval = new_state.alpha_beta(3, float('-inf'), float('inf'), False)

                if eval > best_value:
                    best_value = eval
                    best_move = move

        end_time = time.time()
        print(f"AI izvēlējās {best_move}, aprēķina laiks: {end_time - start_time:.4f} sekundes")

        if best_move:
            self.game.move(best_move, False)
            self.player_turn = True
            self.update_status()

    def update_status(self):
        self.status_label.config(text=f"Skaitlis: {self.game.now_number} | Spēlētāja punkti: {self.game.player_points} | AI punkti: {self.game.ai_points}")
        if self.game.now_number <= 10 or not any(self.game.now_number % move == 0 for move in [2, 3, 4]):
            self.show_game_end_screen()

    def show_game_end_screen(self):
        winner = "Neizšķirts!" if self.game.player_points == self.game.ai_points else "Tu uzvarēji!" if self.game.player_points > self.game.ai_points else "AI uzvarēja!"
        messagebox.showinfo("Spēle beigusies", f"{winner}\n\nSpēlētāja punkti: {self.game.player_points}\nAI punkti: {self.game.ai_points}")
        self.restart_game()

    def restart_game(self):
        self.root.destroy()
        main()

# === Spēles palaišana ===
# https://docs.python.org/3/library/tkinter.html
def main():
    app = ttk.Window()
    app.geometry("400x400")
    gui = GameGUI(app)
    app.mainloop()

main()

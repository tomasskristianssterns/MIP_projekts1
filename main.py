import random
import time
import ttkbootstrap as ttk
from tkinter import messagebox

LEFT_BOUND = 20_000
RIGHT_BOUND = 30_000
MAXIMUM_STARTING_NUMBERS = 5
VALID_DIVISORS = [2, 3, 4]
ENDING_NUMBER = 10
VISITED_NODES = 0
COMPUTER_MOVE_TIMES = []


class GameTreeNode:
    """
    Spēles koka mezgls.
    Izmantojam, lai reprezentētu katru iespējamo spēles stāvokli
    https://en.wikipedia.org/wiki/Game_tree
    """

    def __init__(self, number, player_points=0, ai_points=0):
        self.number = number
        self.player_points = player_points
        self.ai_points = ai_points
        self.children = []

    def generate_children(self):
        for move in VALID_DIVISORS:
            if self.number % move == 0:
                new_number = self.number // move
                child = GameTreeNode(new_number, self.player_points, self.ai_points)
                self.children.append(child)


def generate_valid_numbers() -> list[int]:
    """
    Funkcija, kas ģenerē sākotnējos skaitļus, kuri dalās ar 2, 3 un 4.
    Šādi mēs nodrošinām, ka visām darbībām ir jēga spēles sākumā
    """

    numbers = []
    while len(numbers) < MAXIMUM_STARTING_NUMBERS:
        num = random.randint(LEFT_BOUND, RIGHT_BOUND)
        if num % 2 == 0 and num % 3 == 0 and num % 4 == 0:
            numbers.append(num)
    return numbers


def upgraded_generate_valid_numbers():
    """
    Funkcija, kas ģenerē sākotnējos skaitļus, kuri VIENMĒR dalās ar 2, 3 vai 4 un ka spēle beigsies ar skaitli, kas ir <= 10.
    Šādi mēs nodrošinām, ka spēle notiek ilgāk un ir vairāk iespēju
    """

    numbers = set()
    while len(numbers) < MAXIMUM_STARTING_NUMBERS:
        starting_number = random.choice([1 * 12, 5 * 12, 7 * 12])

        next_multiplier = random.randint(2, 3)
        while starting_number < LEFT_BOUND:
            starting_number *= next_multiplier
            next_multiplier = random.randint(2, 3)
            if LEFT_BOUND <= starting_number <= RIGHT_BOUND:
                numbers.add(starting_number)
                break

    return list(numbers)


class Game:
    """
    Spēles loģikas klase
    Šeit tiek ieviesti visi noteikumi, kustības un AI algoritmi
    """

    def __init__(self, number: int):
        self.now_number = number
        self.player_points = 0
        self.ai_points = 0

    def move(self, divisor: int, is_human: bool) -> bool:
        """
        Lietotāja vai AI gājiens
        """

        if self.now_number % divisor == 0:
            new_number = self.now_number // divisor
            if new_number % 2 == 0:
                if is_human:
                    self.ai_points -= 1
                else:
                    self.player_points -= 1
            else:
                if is_human:
                    self.player_points += 1
                else:
                    self.ai_points += 1
            self.now_number = new_number
            return True
        return False

    def heuristic(self) -> int:
        """
        Heiristikas funkcija, kas nosaka stāvokļa vērtību
        https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
        """
        return self.player_points - self.ai_points

    def minimax(self, depth, is_maximizing) -> int:
        """
        Minimax algoritms (bez griešanas)
        https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-implementation/
        """
        global VISITED_NODES
        VISITED_NODES += 1
        if self.now_number <= ENDING_NUMBER or depth == 0:
            return self.heuristic()

        best_value = float("-inf") if is_maximizing else float("inf")
        for move in VALID_DIVISORS:
            if self.now_number % move == 0:
                new_state = Game(self.now_number // move)
                new_state.player_points = self.player_points
                new_state.ai_points = self.ai_points
                new_state.move(move, is_maximizing)
                eval = new_state.minimax(depth - 1, not is_maximizing)
                best_value = (
                    max(best_value, eval) if is_maximizing else min(best_value, eval)
                )
        return best_value

    def alpha_beta(self, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        """
        Alfa-beta griešana — optimizēts minimax
        https://www.geeksforgeeks.org/practical-implementation-of-alpha-beta-pruning/
        """
        global VISITED_NODES
        VISITED_NODES += 1
        if self.now_number <= ENDING_NUMBER or depth == 0:
            return self.heuristic()

        if is_maximizing:
            max_eval = float("-inf")
            for move in VALID_DIVISORS:
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
            min_eval = float("inf")
            for move in VALID_DIVISORS:
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


class GameGUI:
    """
    Lietotāja saskarne ar ttkbootstrap (Tkinter uzlabotā versija)
    """

    def __init__(self, root):
        self.root = root
        self.algorithm = "Minimax"
        self.start_numbers = upgraded_generate_valid_numbers()

        # Paziņojums par algoritma izvēli
        self.status_label = ttk.Label(
            root, text="Izvēlieties sākotnējo skaitli un algoritmu"
        )
        self.status_label.pack(padx=10, pady=10)
        self.create_selection_screen()
        self.history_list = []
        self.history_tree = None

    def create_selection_screen(self):
        self.selection_frame = ttk.Frame(self.root)
        self.selection_frame.pack(padx=10, pady=10)

        self.label = ttk.Label(
            self.selection_frame, text="Izvēlies sākotnējo skaitli un algoritmu"
        )
        self.label.grid(row=0, column=0, columnspan=2)

        self.start_number_label = ttk.Label(
            self.selection_frame, text="Sākotnējais skaitlis:"
        )
        self.start_number_label.grid(row=1, column=0, padx=5, pady=5)

        self.start_number_option = ttk.Combobox(
            self.selection_frame, values=self.start_numbers
        )
        self.start_number_option.grid(row=1, column=1, padx=5, pady=5)
        self.start_number_option.set(self.start_numbers[0])

        self.algorithm_label = ttk.Label(
            self.selection_frame, text="Izvēlieties algoritmu:"
        )
        self.algorithm_label.grid(row=2, column=0, padx=5, pady=5)

        self.algorithm_option = ttk.Combobox(
            self.selection_frame, values=["Minimax", "Alfa-beta"]
        )
        self.algorithm_option.grid(row=2, column=1, padx=5, pady=5)
        self.algorithm_option.set("Minimax")

        self.first_player_label = ttk.Label(
            self.selection_frame, text="Izvēlieties kurš sāk:"
        )
        self.first_player_label.grid(row=3, column=0, padx=5, pady=5)

        self.player_option = ttk.Combobox(
            self.selection_frame, values=["Spēlētājs", "Dators"]
        )
        self.player_option.grid(row=3, column=1, padx=5, pady=5)
        self.player_option.set("Spēlētājs")

        self.start_button = ttk.Button(
            self.selection_frame,
            text="Sākt spēli",
            command=self.start_game_from_selection,
        )
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

    def start_game_from_selection(self):
        number = int(self.start_number_option.get())
        algorithm = self.algorithm_option.get()
        player = self.set_player(self.player_option.get())
        self.set_algorithm(algorithm)
        self.selection_frame.destroy()
        self.start_game(number, player_starts=player)

    def set_player(self, player):
        self.player = player == "Spēlētājs"
        return self.player

    def set_algorithm(self, algo):
        self.algorithm = algo
        self.status_label.config(text=f"Izvēlēts algoritms: {algo}")

    def start_game(self, number, player_starts):
        self.game = Game(number)
        self.player_turn = player_starts
        self.create_game_screen()
        self.update_status()
        if not self.player_turn:
            self.update_player_status("AI")
            self.ai_move()
        else:
            self.update_player_status("Spēlētājs")

    def create_game_screen(self):
        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)

        self.status_label = ttk.Label(self.game_frame, text="Spēles sākums")
        self.status_label.grid(row=0, column=0, columnspan=3)

        self.turn_label = ttk.Label(self.game_frame, text="Gājiena kārta:")
        self.turn_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.move_buttons = []
        for i, move in enumerate(VALID_DIVISORS):
            button = ttk.Button(
                self.game_frame,
                text=f"Dalīt ar {move}",
                command=lambda move=move: self.player_move(move),
            )
            button.grid(row=1, column=i)
            self.move_buttons.append(button)

    def player_move(self, divisor: int):
        if self.game.move(divisor, True):
            new_node = GameTreeNode(self.game.now_number)  # Create a new node
            if self.history_tree is None:
                self.history_tree = new_node
            else:
                self.history_tree.children.append(new_node)

            self.history_list.append(f"Spēlētājs: {self.game.now_number} (/{divisor})")

            self.player_turn = False
            self.update_status()
            if self.game.now_number > ENDING_NUMBER:
                self.root.after(1500, self.ai_move)
            else:
                self.show_game_end_screen()
        else:
            messagebox.showerror("Kļūda", f"Nevar dalīt šo skaitli ar {divisor}")

    def ai_move(self):
        self.update_player_status("AI")
        best_move = None
        best_value = float("-inf")
        start_time = time.perf_counter_ns()

        for move in VALID_DIVISORS:
            if self.game.now_number % move == 0:
                new_state = Game(self.game.now_number)
                new_state.player_points = self.game.player_points
                new_state.ai_points = self.game.ai_points
                new_state.move(move, False)

                if self.algorithm == "Minimax":
                    eval = new_state.minimax(10, False)
                else:
                    eval = new_state.alpha_beta(10, float("-inf"), float("inf"), False)

                if eval > best_value:
                    best_value = eval
                    best_move = move

        end_time = time.perf_counter_ns()
        print(
            f"AI izvēlējās {best_move}, aprēķina laiks: {(end_time - start_time)/1_000:.4f} milisekundes"
        )

        global COMPUTER_MOVE_TIMES
        COMPUTER_MOVE_TIMES.append(end_time - start_time)

        if best_move:
            self.game.move(best_move, False)
            self.update_status()

            new_node = GameTreeNode(self.game.now_number)
            if self.history_tree:
                self.history_tree.children.append(new_node)

            self.history_list.append(f"AI: {self.game.now_number} (/{best_move})")

            if self.game.now_number > ENDING_NUMBER:
                self.root.after(1500, self.enable_player_turn)
            else:
                self.show_game_end_screen()

    def enable_player_turn(self):
        self.update_player_status("Spēlētājs")
        self.player_turn = True
        self.update_status()

    def update_status(self):
        self.status_label.config(
            text=f"Skaitlis: {self.game.now_number} | Spēlētāja punkti: {self.game.player_points} | AI punkti: {self.game.ai_points}"
        )

    def update_player_status(self, move):
        self.turn_label.config(text=f"Gājiena kārta: {move}")

    def show_game_end_screen(self):
        if self.game.player_points == self.game.ai_points:
            winner = "Neizšķirts!"
        elif self.game.player_points > self.game.ai_points:
            winner = "Tu uzvarēji!"
        else:
            winner = "AI uzvarēja!"

        global VISITED_NODES, COMPUTER_MOVE_TIMES
        average_time = (
            sum(COMPUTER_MOVE_TIMES) / len(COMPUTER_MOVE_TIMES)
            if COMPUTER_MOVE_TIMES
            else 0
        )

        average_time /= 1_000  # milisekundes

        messagebox.showinfo(
            "Spēle beigusies",
            f"{winner}\n\nSpēlētāja punkti: {self.game.player_points}\nAI punkti: {self.game.ai_points}\nDators apmeklēja {VISITED_NODES} virsotnes\nVidējais datora gājiena laiks: {average_time:.2f} milisekundes\n\n",
        )
        restart_button = ttk.Button(
            self.game_frame, text="Jauna spēle", command=self.restart_game
        )
        restart_button.grid(row=4, column=0)

        history_button = ttk.Button(
            self.game_frame, text="Vēsture", command=self.show_history_text
        )
        history_button.grid(row=4, column=1)

        tree_button = ttk.Button(
            self.game_frame, text="Paradīt koku", command=self.show_tree
        )
        tree_button.grid(row=4, column=2)

    def restart_game(self):
        global VISITED_NODES, COMPUTER_MOVE_TIMES
        VISITED_NODES = 0
        COMPUTER_MOVE_TIMES = []
        self.game_frame.destroy()
        main()

    def show_history_text(self):
        history_window = ttk.Toplevel(self.root)
        history_window.title("Spēles vēsture")

        history_text = "\n".join(self.history_list)
        history_label = ttk.Label(history_window, text=history_text, justify="left")
        history_label.pack(padx=10, pady=10)

        close_button = ttk.Button(
            history_window, text="Close", command=history_window.destroy
        )
        close_button.pack(pady=5)

    def display_tree(self, node, depth=0):
        """
        Rekursīvi rada spēles koku
        """
        if node is None:
            return ""

        result = "  " * depth + f"→ {node.number}\n"

        for child in node.children:
            result += self.display_tree(child, depth + 1)

        return result

    def show_tree(self):
        tree_window = ttk.Toplevel(self.root)
        tree_window.title("Spēles koks")

        tree_text = self.display_tree(self.history_tree)

        tree_label = ttk.Label(tree_window, text=tree_text, justify="left")
        tree_label.pack(padx=10, pady=10)

        close_button = ttk.Button(
            tree_window, text="Close", command=tree_window.destroy
        )
        close_button.pack(pady=5)


def main():
    """
    Spēles palaišana
    https://docs.python.org/3/library/tkinter.html
    """

    app = ttk.Window()
    app.geometry("400x400")
    GameGUI(app)
    app.mainloop()


if __name__ == "__main__":
    main()

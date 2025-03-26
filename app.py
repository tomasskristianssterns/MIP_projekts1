import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

LEFT_BOUND = 20_000
RIGHT_BOUND = 30_000

VALID_DIVISORS = [2, 3, 4]
MAX_STARTING_NUMBERS = 5

def is_valid_number(number: int) -> bool:
  for divisor in VALID_DIVISORS:
    if number % divisor == 0:
      return True
  return False

def get_number() -> int:
  genereted_number = random.randint(LEFT_BOUND, RIGHT_BOUND)
  while not is_valid_number(genereted_number):
    genereted_number = random.randint(LEFT_BOUND, RIGHT_BOUND)
  return genereted_number

def numbers_for_select():
  starting_numbers = [get_number() for _ in range(MAX_STARTING_NUMBERS)]
  return starting_numbers
    
def Start_game():
    print(selected_number.get(), selected_algorithm.get(), selected_first.get())
        

def Choose_options(root):
    global window_first, selected_algorithm, selected_first, selected_number
    window_first = root
    window_first.title("Choose options")
    window_first.geometry("400x300")
    window_first.resizable(width=False, height=False)

    window_first.configure(bg="#CEEDC7")
    style = ttk.Style()
    style.theme_create("loggy", parent="alt", settings={
        "TButton": {
            "configure": {
                "font": ("Calibri Light", 10, "bold"), 
                "foreground": "black", 
                "background": "#86C8BC"
            },
            "map": {
                "background": [("disabled", "black"), ("pressed", "#CBAF87"), ("active", "#E7DEC8")],
                "relief": [("pressed", "sunken"), ("!pressed", "raised")]
            }
        },
        "TRadiobutton": {
            "configure": {
                "font": ("Calibri Light", 12),
                "foreground": "black",
                "background": "#CEEDC7",
                "indicatorcolor": "#86C8BC"
            },
            "map": {
                "background": [("active", "#E7DEC8")],
                "foreground": [("active", "black")],
                "indicatorcolor": [("selected", "#86C8BC"), ("pressed", "#CBAF87")]
            }
        }
    })
    
    style.theme_use("loggy")
    
    tk.Label(window_first, text="Hello, player!", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=1, padx= 130.0, sticky="w")
    tk.Label(window_first, text="Choose who will start first:", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=2, padx=70.0, sticky="w")

    selected_first = tk.StringVar(value = "Human")
     
    human_btn = ttk.Radiobutton(text="Human", variable = selected_first, value="Human")
    human_btn.place(x = 110, y = 80)
    
    computer_btn = ttk.Radiobutton(text="Computer", variable = selected_first, value = "Computer")
    computer_btn.place (x = 200, y = 80)
    
    
    tk.Label(window_first, text="Choose algorithm:", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=3, padx= 100.0, pady = 40, sticky="w")
    
    selected_algorithm = tk.StringVar(value = "MinMax")
    
    MinMax_btn = ttk.Radiobutton(text="MinMax", variable = selected_algorithm, value="MinMax")
    MinMax_btn.place(x = 110, y = 150)
    
    AlfaBeta_btn = ttk.Radiobutton(text="AlfaBeta",variable = selected_algorithm, value = "AlfaBeta")
    AlfaBeta_btn.place (x = 200, y = 150)

        
    tk.Label(window_first, text="Choose number:", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=4, padx= 110.0, sticky="w")
    numbers = numbers_for_select()
    
    selected_number = tk.IntVar()
    selected_number.set(str(numbers[0]))
    
    btn1 = ttk.Radiobutton(text = str(numbers[0]), variable = selected_number, value = numbers[0])
    btn1.place(x = 45, y = 220)
    
    btn2 = ttk.Radiobutton(text = str(numbers[1]), variable = selected_number, value = numbers[1])
    btn2.place(x = 115, y = 220)
    
    btn3 = ttk.Radiobutton(text = str(numbers[2]), variable = selected_number, value = numbers[2])
    btn3.place(x = 175, y = 220)
    
    btn4 = ttk.Radiobutton(text = str(numbers[3]), variable = selected_number, value = numbers[3])
    btn4.place(x = 235, y = 220)
    
    btn5 = ttk.Radiobutton(text = str(numbers[4]), variable = selected_number, value = numbers[4])
    btn5.place(x = 295, y = 220)
    
    button_start = ttk.Button(window_first, text = "Start", command = Start_game)
    button_start.place(height = 40, width = 70, x = 165, y = 250)
    
    
if __name__ == "__main__":
    root = tk.Tk()
    Choose_options(root)
    root.mainloop()
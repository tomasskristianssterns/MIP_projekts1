import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window_login = tk.Tk()
window_login.title("Login Form")
window_login.geometry("400x250")
window_login.resizable(width=False, height=False)

window_login.configure(bg="#CEEDC7")
style_login = ttk.Style()
style_login.theme_create("loggy", parent="alt", settings={
    "TButton": {
        "configure": {"font": ("Calibri Light", 10, "bold"), "foreground": "black", "background": "#86C8BC"},
        "map": {"background": [("disabled", "black"), ("pressed", "#CBAF87"), ("active", "#E7DEC8")],
                "relief": [("pressed", "sunken"), ("!pressed", "raised")]}}})
style_login.theme_use("loggy")

global message, username, password

message = tk.StringVar()
username = tk.StringVar()
password = tk.StringVar()

tk.Label(window_login, text="Labdien, lietotājs!", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=1, padx= 120.0, sticky="w")
tk.Label(window_login, text="Lūdzu pielogojies", background="#CEEDC7", font=('Calibri Light', 17)).grid(column=0, row=2, padx=120.0, sticky="w")

tk.Label(window_login, text="Username", background="#CEEDC7", font=('Calibri Light', 15, 'bold')).grid(column=0, row=3, padx= 10.0, sticky="w")
tk.Entry(window_login, textvariable=username, width=24, font=('Calibri Light', 15)).grid(column=0, row=3, padx=110.0,sticky="w")
tk.Label(window_login, text="Password", background="#CEEDC7",font=('Calibri Light', 15, 'bold')).grid(column=0, row=4, padx=10.0, sticky="w")
tk.Entry(window_login, textvariable=password, show="*", width=15, font=('Calibri Light', 15)).grid(column=0, row=4, padx=110.0, sticky="w")

tk.Label(window_login, text="", textvariable=message,  background="#CEEDC7", font=('Calibri Light', 14)).grid(column=0, row=5, padx=100.0, sticky="w")
# button_login = ttk.Button(window_login, text="Login", command=Login)
button_login = ttk.Button(window_login, text="Login")
button_login.place(height=40, width=70, x=170, y=200)



window_login.mainloop()
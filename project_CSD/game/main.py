# main.py
import tkinter as tk
from gui import WerewolfGame

if __name__ == "__main__":
    root = tk.Tk()
    app = WerewolfGame(root)
    root.mainloop()
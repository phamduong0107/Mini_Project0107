# main.py
import tkinter as tk
from gui.gui import WerewolfGame

def main():
    root = tk.Tk()
    app = WerewolfGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
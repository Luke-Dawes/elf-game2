#main file for sir to run, you can either run it from this file or from the main.py file
from main import ElfGame
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ElfGame(root)
    root.mainloop()
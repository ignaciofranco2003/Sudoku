import tkinter as tk
from gui.App import SudokuGUI

def main():
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

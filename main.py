import tkinter as tk
from gui.App import SudokuGUI

def main():
    root = tk.Tk()          # Creamos la ventana principal
    SudokuGUI(root)         # Inicializamos la interfaz gráfica
    root.mainloop()         # Iniciamos el bucle de eventos de la interfaz

if __name__ == "__main__":
    main()
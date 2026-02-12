import os
import tkinter as tk
from tkinter import messagebox

from SudokuLogica import SudokuLogica

from .Variables import TAM
from .UI import UI
from .Styles import apply_style
from .Tablero import Tablero
from .Eventos import Eventos
from .Acciones import Acciones

class SudokuGUI(UI, Tablero, Eventos, Acciones):
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sudoku - Interfaz Gráfica")
        self.root.resizable(False, False)

        # app.py está dentro de /gui, subimos 1 nivel para quedar en el root del proyecto
        gui_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(gui_dir)
        os.chdir(project_root)

        try:
            self.logica = SudokuLogica()
        except Exception as e:
            messagebox.showerror("Error inicializando lógica", f"{e}")
            raise

        # Estado UI
        self.vars = [[tk.StringVar(value="") for _ in range(TAM)] for _ in range(TAM)]
        self.entries = [[None for _ in range(TAM)] for _ in range(TAM)]
        self.pistas = [[False for _ in range(TAM)] for _ in range(TAM)]      # pistas originales (no se pueden desbloquear)
        self.bloq_manual = [[False for _ in range(TAM)] for _ in range(TAM)]  # bloqueos con click derecho

        # Configuración de generación
        self.dificultad_var = tk.StringVar(value="Medio (35 pistas)")

        # Selección / resaltado
        self.selected = None  # (i, j)
        self.entry_pos = {}   # widget -> (i, j)

        # Para iterar soluciones
        self.puzzle_base = None
        self.puzzle_base_key = None

        self._build_ui()

    # ---------------- Metodos auxiliares ----------------

    def _validate_cell(self, proposed: str) -> bool:
        if proposed == "":
            return True
        if len(proposed) > 1:
            return False
        return proposed.isdigit() and proposed != "0"

    def _set_status(self, text: str):
        self.status.config(text=text)

    def _tablero_desde_ui(self):
        tablero = []
        for i in range(TAM):
            fila = []
            for j in range(TAM):
                s = self.vars[i][j].get().strip()
                fila.append(int(s) if s.isdigit() else 0)
            tablero.append(fila)
        return tablero

    def _cargar_a_ui(self, tablero):
        for i in range(TAM):
            for j in range(TAM):
                v = tablero[i][j]
                self.vars[i][j].set("" if v == 0 else str(v))

    def _marcar_fijos(self, tablero):
        for i in range(TAM):
            for j in range(TAM):
                self.pistas[i][j] = (tablero[i][j] != 0)
                self.bloq_manual[i][j] = False

                e = self.entries[i][j]
                if self.pistas[i][j]:
                    e.config(
                        disabledbackground="#dbeafe",
                        disabledforeground="#1d4ed8",
                        state="disabled"
                    )
                else:
                    e.config(state="normal", bg="#ffffff", fg="#111827")

    def _limpiar_fijos(self):
        for i in range(TAM):
            for j in range(TAM):
                self.pistas[i][j] = False
                self.bloq_manual[i][j] = False
                self.entries[i][j].config(state="normal", bg="#ffffff", fg="#111827")

    def _toggle_lock(self, i: int, j: int):
        # Pistas del tablero NO se pueden desbloquear
        if self.pistas[i][j]:
            self._set_status("Esa celda es una pista del tablero: no se puede desbloquear.")
            return

        # Si ya estaba bloqueada manualmente -> desbloquear
        if self.bloq_manual[i][j]:
            self.bloq_manual[i][j] = False
            e = self.entries[i][j]
            e.config(state="normal")
            e.config(bg="#ffffff", fg="#111827")
            self._set_status("Celda desbloqueada.")
            return

        # Si no estaba bloqueada -> bloquear (solo si tiene número)
        s = self.vars[i][j].get().strip()
        if not (s.isdigit() and s != "0"):
            self._set_status("No se puede bloquear una celda vacía.")
            return

        self.bloq_manual[i][j] = True
        e = self.entries[i][j]
        e.config(
            disabledbackground="#d1fae5",
            disabledforeground="#065f46",
            state="disabled"
        )
        self._set_status("Celda bloqueada.")

    def _puzzle_key(self, tablero):
        return tuple(tuple(row) for row in tablero)

    def _actualizar_puzzle_base_si_cambio(self, tablero_actual):
        key = self._puzzle_key(tablero_actual)
        if self.puzzle_base_key != key:
            self.puzzle_base = tablero_actual
            self.puzzle_base_key = key

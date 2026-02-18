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
        # Ventana principal
        self.root = root
        self.root.title("Sudoku - Interfaz Gráfica")
        self.root.resizable(False, False)

        # Ajustamos el directorio de trabajo al root del proyecto
        gui_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(gui_dir)
        os.chdir(project_root)

        # Inicializa módulo lógico
        try:
            self.logica = SudokuLogica()
        except Exception as e:
            messagebox.showerror("Error inicializando lógica", f"{e}")
            raise

        # Estado de la interfaz -----------------------------------------------------------------------------
        
        self.vars = [[tk.StringVar(value="") for _ in range(TAM)] for _ in range(TAM)]  # Variables de texto asociadas a cada celda del tablero
        self.entries = [[None for _ in range(TAM)] for _ in range(TAM)]     # Referencias a los widgets Entry (celdas visuales)
        self.pistas = [[False for _ in range(TAM)] for _ in range(TAM)]     # Celdas fijas (pistas originales del tablero)
        self.bloq_manual = [[False for _ in range(TAM)] for _ in range(TAM)]    # Celdas bloqueadas manualmente por el usuario

        # Dificultad seleccionada por el usuario (cantidad de pistas)
        self.dificultad_var = tk.StringVar(value="Medio (35 pistas)")

        # Estado de selección actual (celda activa)
        self.selected = None  # (fila, columna)
        self.entry_pos = {}   # Mapeo widget - coordenadas de celda

        # Tablero base para iterar soluciones o validaciones
        self.puzzle_base = None
        self.puzzle_base_key = None

        self._build_ui()

    # Metodos auxiliares -----------------------------------------------------------------------------

    def _validate_cell(self, proposed: str) -> bool:
        """
        Valida el contenido ingresado en una celda.
        Permite solo números del 1 al 9 o vacío.
        """
        if proposed == "":
            return True
        if len(proposed) > 1:
            return False
        return proposed.isdigit() and proposed != "0"

    def _set_status(self, text: str):
        # Actualiza el mensaje de estado
        self.status.config(text=text)

    def _tablero_desde_ui(self):
        """
        Construye una matriz de enteros a partir de los valores visibles en la interfaz.
        Las celdas vacías se interpretan como 0.
        """
        tablero = []
        for i in range(TAM):
            fila = []
            for j in range(TAM):
                s = self.vars[i][j].get().strip()
                fila.append(int(s) if s.isdigit() else 0)
            tablero.append(fila)
        return tablero

    def _cargar_a_ui(self, tablero):
        # Carga un tablero (matriz de enteros) en la interfaz gráfica
        for i in range(TAM):
            for j in range(TAM):
                v = tablero[i][j]
                self.vars[i][j].set("" if v == 0 else str(v))

    def _marcar_fijos(self, tablero):
        """
        Marca como 'pistas' las celdas que ya vienen completas en el tablero.
        Estas celdas quedan bloqueadas y diferenciadas visualmente.
        """
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
        # Elimina cualquier estado de bloqueo y deja todas las celdas editables
        for i in range(TAM):
            for j in range(TAM):
                self.pistas[i][j] = False
                self.bloq_manual[i][j] = False
                self.entries[i][j].config(state="normal", bg="#ffffff", fg="#111827")

    def _toggle_lock(self, i: int, j: int):
        # No se pueden desbloquear pistas originales
        if self.pistas[i][j]:
            self._set_status("Esa celda es una pista del tablero: no se puede desbloquear.")
            return

        # Si estaba bloqueada manualmente → desbloquear
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
        # Genera una representación inmutable del tablero para comparar estados
        return tuple(tuple(row) for row in tablero)

    def _actualizar_puzzle_base_si_cambio(self, tablero_actual):
        """
        Actualiza el tablero base solo si el estado actual cambió.
        Permite detectar modificaciones del usuario.
        """
        key = self._puzzle_key(tablero_actual)
        if self.puzzle_base_key != key:
            self.puzzle_base = tablero_actual
            self.puzzle_base_key = key

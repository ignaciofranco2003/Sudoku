import tkinter as tk
from tkinter import ttk

from .Variables import PANEL_W, CANVAS_W, CANVAS_H
from .Styles import apply_style

class UI:
    def _build_ui(self):
        apply_style(self.root)

        outer = ttk.Frame(self.root, padding=14)
        outer.grid(row=0, column=0, sticky="nsew")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        outer.columnconfigure(0, weight=1)

        # ================= HEADER =================
        header = ttk.Frame(outer)
        header.grid(row=0, column=0, sticky="ew")

        ttk.Label(header, text="Sudoku", style="Title.TLabel") \
            .grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text="Generar / validar / resolver",
            style="Sub.TLabel"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        # ================= CONTENT =================
        content = ttk.Frame(outer)
        content.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=0, minsize=PANEL_W)
        content.rowconfigure(0, weight=1)

        # ================= IZQUIERDA (TABLERO) =================
        left = ttk.Frame(content)
        left.grid(row=0, column=0, sticky="n")

        board_card = ttk.Frame(left, style="Card.TFrame", padding=12)
        board_card.grid(row=0, column=0, sticky="n")

        self.canvas = tk.Canvas(
            board_card,
            width=CANVAS_W,
            height=CANVAS_H,
            highlightthickness=0,
            bg="#ffffff"
        )
        self.canvas.grid(row=0, column=0)

        self._draw_grid()
        self._build_entries()

        # Click derecho: bloquear/desbloquear
        self.root.bind_all("<Button-3>", self._on_right_click, add="+")

        # Click izquierdo fuera del tablero: deseleccionar
        self.root.bind_all("<Button-1>", self._on_any_left_click, add="+")

        # ================= DERECHA (PANEL) =================
        right = ttk.Frame(content)
        right.grid(row=0, column=1, sticky="n", padx=(14, 0))
        right.columnconfigure(0, weight=1)

        panel = ttk.Frame(right, style="Panel.TFrame", padding=12)
        panel.grid(row=0, column=0, sticky="n")
        panel.columnconfigure(0, minsize=PANEL_W, weight=1)

        ttk.Label(panel, text="Acciones", style="PanelTitle.TLabel") \
            .grid(row=0, column=0, sticky="w")

        # -------- Generación --------
        gen = ttk.Labelframe(panel, text="Generación", padding=18)
        gen.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        gen.columnconfigure(0, weight=1)

        ttk.Button(gen, text="Generar tablero completo", command=self.on_generar) \
            .grid(row=0, column=0, sticky="ew")

        ttk.Button(gen, text="Generar tablero para jugar", command=self.on_generar_incompleto) \
            .grid(row=1, column=0, sticky="ew", pady=(8, 0))

        ttk.Button(gen, text="Nuevo tablero vacío", command=self.on_nuevo_vacio) \
            .grid(row=2, column=0, sticky="ew", pady=(8, 0))

        # -------- Juego --------
        play = ttk.Labelframe(panel, text="Juego", padding=10)
        play.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        play.columnconfigure(0, weight=1)

        ttk.Button(play, text="Validar tablero", command=self.on_validar) \
            .grid(row=0, column=0, sticky="ew")

        ttk.Button(play, text="Resolver", command=self.on_resolver) \
            .grid(row=1, column=0, sticky="ew", pady=(8, 0))

        ttk.Button(play, text="Limpiar edición", command=self.on_limpiar_editables) \
            .grid(row=2, column=0, sticky="ew", pady=(8, 0))
        
        ttk.Button(play, text="Completar", command=self.on_completar) \
            .grid(row=3, column=0, sticky="ew", pady=(8, 0))

        # -------- Configuraciones --------
        cfg = ttk.Labelframe(panel, text="Configuraciones", padding=10)
        cfg.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        cfg.columnconfigure(1, weight=1)

        ttk.Label(cfg, text="Dificultad:", style="PanelText.TLabel").grid(row=0, column=0, sticky="w")
        self.cmb_dificultad = ttk.Combobox(
            cfg,
            textvariable=self.dificultad_var,
            state="readonly",
            values=["Muy Fácil (45 pistas)","Fácil (40 pistas)", "Medio (35 pistas)", "Difícil (30 pistas)", "Muy Difícil (25 pistas)"]
        )
        self.cmb_dificultad.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.cmb_dificultad.bind(
            "<FocusIn>",
            lambda e: e.widget.after_idle(
                lambda: (e.widget.selection_clear(), e.widget.icursor("end"))
            ),
            add="+"
        )

        self.cmb_dificultad.bind(
            "<<ComboboxSelected>>",
            lambda e: e.widget.after_idle(
                lambda: (e.widget.selection_clear(), e.widget.icursor("end"))
            ),
            add="+"
        )
        
        self.cmb_dificultad.bind(
            "<<ComboboxSelected>>",
            lambda e: self.root.after_idle(self.root.focus_set),
            add="+"
        )

        self.cmb_dificultad.bind(
            "<Button-1>",
            lambda e: e.widget.after_idle(
                lambda: (e.widget.selection_clear(), e.widget.icursor("end"))
            ),
            add="+"
        )
        # ================= STATUS =================
        status_bg = tk.Frame(panel, bg="#ffffff")
        status_bg.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        status_bg.grid_propagate(False)
        status_bg.configure(height=54)
        status_bg.columnconfigure(0, weight=1)

        self.status = tk.Label(
            status_bg,
            text="Listo.",
            bg="#ffffff",
            fg="#333333",
            justify="left",
            anchor="w",
            wraplength=PANEL_W - 24
        )
        self.status.grid(row=0, column=0, sticky="ew", padx=10, pady=8)

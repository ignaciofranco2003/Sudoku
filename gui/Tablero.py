import tkinter as tk
from .Variables import TAM, CELL, MARGIN, BOARD

class Tablero:
    def _draw_grid(self):
        x0 = MARGIN
        y0 = MARGIN
        x1 = MARGIN + BOARD
        y1 = MARGIN + BOARD

        # borde externo
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#111827", width=2, tags=("grid",))

        # líneas internas
        for i in range(1, TAM):
            w = 2 if i % 3 == 0 else 1
            color = "#111827" if i % 3 == 0 else "#9CA3AF"

            # vertical
            x = MARGIN + i * CELL
            self.canvas.create_line(x, y0, x, y1, fill=color, width=w, tags=("grid",))

            # horizontal
            y = MARGIN + i * CELL
            self.canvas.create_line(x0, y, x1, y, fill=color, width=w, tags=("grid",))

    def _build_entries(self):
        vcmd = (self.root.register(self._validate_cell), "%P")

        for i in range(TAM):
            for j in range(TAM):
                e = tk.Entry(
                    self.canvas,
                    textvariable=self.vars[i][j],
                    width=2,
                    font=("Segoe UI", 18),
                    justify="center",
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    validate="key",
                    validatecommand=vcmd
                )

                # Colores base
                e.configure(
                    bg="#ffffff",
                    fg="#111827",
                    disabledbackground="#dbeafe",   # celeste suave para fijos
                    disabledforeground="#1d4ed8"    # azul fuerte para fijos
                )

                x = MARGIN + j * CELL + 1
                y = MARGIN + i * CELL + 1
                e.place(x=x + 8, y=y + 8, width=CELL - 16, height=CELL - 16)

                self.entry_pos[e] = (i, j)

                # Selección: resaltar fila/columna/celda
                e.bind("<FocusIn>", lambda ev, ii=i, jj=j: self._on_select(ii, jj))
                e.bind("<Button-1>", lambda ev, ii=i, jj=j: self._on_select(ii, jj))

                self.entries[i][j] = e

    # ---------- resaltado ----------
    def _cell_bbox(self, i: int, j: int):
        x = MARGIN + j * CELL + 1
        y = MARGIN + i * CELL + 1
        return x, y, x + CELL - 2, y + CELL - 2

    def _clear_highlight(self):
        self.canvas.delete("hl")

    def _highlight_selection(self, i: int, j: int):
        self._clear_highlight()

        row_col_fill = "#d1fae5"   # verde muy clarito
        cell_fill = "#86efac"      # un poco más fuerte

        # Fila
        for jj in range(TAM):
            x0, y0, x1, y1 = self._cell_bbox(i, jj)
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill=row_col_fill, tags=("hl",))

        # Columna
        for ii in range(TAM):
            x0, y0, x1, y1 = self._cell_bbox(ii, j)
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill=row_col_fill, tags=("hl",))

        # Celda seleccionada
        x0, y0, x1, y1 = self._cell_bbox(i, j)
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill=cell_fill, tags=("hl",))

        # highlight debajo de la grilla
        self.canvas.tag_lower("hl", "grid")

    def _on_select(self, i: int, j: int):
        self.selected = (i, j)
        self._highlight_selection(i, j)

class Eventos:
    def _on_right_click(self, event):
        w = event.widget
        if w in self.entry_pos:
            i, j = self.entry_pos[w]
            self._on_select(i, j)
            self._toggle_lock(i, j)
            return "break"
        return None

    def _on_any_left_click(self, event):
        """Si el click izquierdo fue fuera de una celda, limpia la selección y el resaltado."""
        w = event.widget

        # Si el click fue sobre controles (botones/combobox/etc), no robar el foco.
        # Si no, el Combobox no abre/selecciona correctamente.
        try:
            cls = w.winfo_class()
        except Exception:
            cls = ""
        if cls in {"TCombobox", "TButton", "TMenubutton", "TScrollbar", "TEntry", "TSpinbox"}:
            self.selected = None
            self._clear_highlight()
            return

        # Si el click fue sobre una celda, no limpiar
        if w in self.entry_pos:
            return

        self.selected = None
        self._clear_highlight()

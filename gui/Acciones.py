from tkinter import messagebox
from .Variables import TAM

class Acciones:
    def on_generar(self):
        # Confirma con el usuario antes de borrar el tablero actual
        if not messagebox.askyesno(
            "Generar tablero",
            "Esto va a borrar el tablero actual.\n¿Querés continuar?"
        ):
            return

        try:
            # Genera un tablero completo usando la lógica
            tablero = self.logica.generar()
            if not tablero:
                messagebox.showerror("Error", "No se pudo generar un tablero.")
                return

            self._cargar_a_ui(tablero)  # Carga el tablero en la interfaz
            self._marcar_fijos(tablero) # Marca las celdas originales como fijas

            # Guarda este tablero como base
            self.puzzle_base = tablero
            self.puzzle_base_key = self._puzzle_key(tablero)

            self._clear_highlight()
            self._set_status("Tablero completo generado.")
        except Exception as e:
            messagebox.showerror("Error al generar", str(e))

    def on_generar_incompleto(self):
        # Obtiene la dificultad seleccionada
        dificultad = (self.dificultad_var.get() or "Medio").strip()

        # Confirmación del usuario
        if not messagebox.askyesno(
            "Generar tablero para jugar",
            f"Se perderá el tablero actual.\n"
            f"Dificultad seleccionada:\n{dificultad}\n\n¿Continuar?"
        ):
            return

        try:
            # Cantidad de pistas según dificultad
            pistas = {
                "Muy Fácil (45 pistas)": 45,
                "Fácil (40 pistas)": 40,
                "Medio (35 pistas)": 35,
                "Difícil (30 pistas)": 30,
                "Muy Difícil (25 pistas)": 25
            }.get(dificultad, 35)

            # Genera tablero incompleto
            tablero = self.logica.generar_incompleto(pistas)
            if not tablero:
                messagebox.showerror("Error", "No se pudo generar un tablero para jugar.")
                return

            self._cargar_a_ui(tablero)
            self._marcar_fijos(tablero)

            self.puzzle_base = tablero
            self.puzzle_base_key = self._puzzle_key(tablero)

            self._clear_highlight()
            self._set_status("Tablero para jugar generado.")
        except Exception as e:
            messagebox.showerror("Error al generar incompleto", str(e))

    def on_nuevo_vacio(self):
        # Confirma acción
        if not messagebox.askyesno(
            "Nuevo tablero vacío",
            "Se borrará todo el tablero actual.\n¿Querés continuar?"
        ):
            return

        # Limpia estados y variables
        self._limpiar_fijos()
        for i in range(TAM):
            for j in range(TAM):
                self.vars[i][j].set("")

        empty = [[0] * TAM for _ in range(TAM)]
        self.puzzle_base = empty
        self.puzzle_base_key = self._puzzle_key(empty)

        self._clear_highlight()
        self._set_status("Tablero vacío listo.")

    def on_limpiar_editables(self):
        # Limpia solo las celdas editables
        if not messagebox.askyesno(
            "Limpiar celdas",
            "Se borrarán todas las celdas editables.\n¿Continuar?"
        ):
            return

        self._limpiar()

    def on_validar(self):
        try:
            # Obtiene el tablero actual desde la interfaz
            tablero = self._tablero_desde_ui()
            solucion = self.logica.resolver(tablero)    # Intenta resolverlo

            # Si no tiene solución → inválido
            if solucion is None or solucion is False:
                messagebox.showerror("Inválido", "El tablero NO es válido (no tiene solución).")
                self._set_status("Validación: tablero inválido.")
            else:
                messagebox.showinfo("Válido", "El tablero es válido (existe al menos una solución).")
                self._set_status("Validación: tablero válido.")
        except Exception as e:
            messagebox.showerror("Error al validar", str(e))

    def on_resolver(self):
        try:
            # Limpia las celdas editables antes de resolver
            self._limpiar()
            tablero_actual = self._tablero_desde_ui()
            self._actualizar_puzzle_base_si_cambio(tablero_actual)  # Si el tablero cambió, actualiza la base

            # Resuelve el tablero base
            solucion = self.logica.resolver(self.puzzle_base)

            if solucion is None or solucion is False:
                messagebox.showerror("Sin solución", "No se encontró solución para este tablero.")
                self._set_status("Resolver: tablero sin solución.")
                return

            # Muestra la solución en pantalla
            self._cargar_a_ui(solucion)
            self._set_status("Solución cargada. Podés pedir otra solución.")
        except Exception as e:
            messagebox.showerror("Error al resolver", str(e))

    def on_completar(self):
        try:
            tablero = self._tablero_desde_ui()
            completo = all(all(v != 0 for v in fila) for fila in tablero)   # Verifica si está completo

            solucion = self.logica.resolver(tablero)

            # Si no tiene solución → inválido
            if solucion is None or solucion is False:
                messagebox.showerror("Inválido", "El tablero NO es válido (no tiene solución).")
                self._set_status("Tablero inválido.")
                return

            if not completo:
                self._set_status("El tablero no esta completo!")
                return
            messagebox.showinfo("OK", "¡El tablero está completo y es válido!")
            self._set_status("Tablero válido.")

            # Ofrece generar un nuevo juego
            if messagebox.askyesno("Nuevo juego", "¿Querés generar un nuevo tablero para jugar?"):
                self.on_generar_incompleto()

        except Exception as e:
            messagebox.showerror("Error en completar", str(e))

    def _limpiar(self):
        # Borra solo celdas editables (no pistas ni bloqueadas)
        for i in range(TAM):
            for j in range(TAM):
                if (not self.pistas[i][j]) and (not self.bloq_manual[i][j]):
                    self.vars[i][j].set("")

        self._set_status("Se limpiaron las celdas editables.")
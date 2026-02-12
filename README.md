# Sudoku funcional y lógico (Python funcional + SWI‑Prolog)

Aplicación de **Sudoku funcional** con interfaz gráfica, que permite **jugar, validar y resolver** tableros usando un motor lógico basado en **SWI‑Prolog**.

## ¿Qué es?
Un Sudoku jugable con GUI donde podés:
- **Generar** tableros.
- **Validar** si el tablero actual es consistente.
- **Resolver/Completar** el tablero mediante lógica (Prolog).

## Características
- Interfaz gráfica para edición del tablero.
- Validación de reglas de Sudoku (filas, columnas y subcuadrículas).
- Resolución automática usando **lógica en Prolog**.
- Flujo de juego: generar → jugar → validar/completar → nuevo tablero.

## Requisitos
- **Windows**
- **Python 3.x**
- **SWI‑Prolog instalado y en el `PATH`** (obligatorio)

## Imágenes
![Interfaz Principal](https://drive.google.com/file/d/1wrW0w19CcvfYl_wdmwBVgYz7pcFsYGeY/view?usp=sharing)

## Ejecución
El punto de entrada del proyecto es:

- `main.py`

Ejecutalo desde VS Code (Run) o desde terminal:
```powershell
python main.py

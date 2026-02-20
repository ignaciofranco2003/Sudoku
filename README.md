# Sudoku Híbrido: Programación Lógica y Funcional (Python + SWI-Prolog)

Aplicación de escritorio para jugar, generar y resolver Sudokus, construida bajo un enfoque declarativo híbrido. Utiliza **SWI-Prolog** como motor de inferencia lógica y **Python** para la transformación funcional de datos y la interfaz gráfica.

## Objetivo
Explorar la integración práctica entre programación lógica y funcional en una aplicación real, minimizando el estado mutable y priorizando la corrección declarativa.

## Arquitectura y Diseño
El proyecto destaca por la implementación del patrón arquitectónico **"Functional Core, Imperative Shell"**:
- **Núcleo Funcional (Prolog + Python):** La resolución y generación se delegan a un motor lógico puro usando programación por restricciones sobre dominios finitos (`clpfd`). Python actúa como *middleware*, transformando las matrices de forma inmutable mediante funciones de orden superior (`map`, `lambda`).
- **Caparazón Imperativo (Tkinter):** La interfaz gráfica aísla y gestiona el estado mutable y la interacción del usuario, protegiendo la pureza matemática de la lógica de negocio subyacente.

## Comunicación Python–Prolog
La interacción se realiza mediante consultas dinámicas desde Python hacia el motor Prolog, delegando la resolución y validación del tablero al sistema lógico y recuperando los resultados como estructuras serializables.

## Características Principales
- **Generación garantizada:** Creación de tableros nuevos y jugables a partir de soluciones lógicamente perfectas.
- **Validación estricta:** Comprobación de la consistencia del tablero (filas, columnas y subcuadrantes 3x3).
- **Resolución automática:** Algoritmo optimizado que evita la fuerza bruta tradicional aprovechando la propagación de restricciones nativa de Prolog.
- **Interfaz interactiva:** GUI desacoplada con sistema de bloqueo dual (pistas inmutables generadas por el sistema y protección manual de celdas por el usuario).

## Requisitos
- **Sistema Operativo:** Windows
- **Python:** 3.x
- **SWI-Prolog:** Debe estar instalado y agregado a las variables de entorno (`PATH`).

## Instalación necesaria
Instalar la librería necesaria para comunicar Python con Prolog:
   ```powershell
   pip install pyswip
   ```

## Interfaz
![Interfaz Principal](https://drive.google.com/uc?export=view&id=1wrW0w19CcvfYl_wdmwBVgYz7pcFsYGeY)
- La interfaz está pensada para Windows y Tkinter.
- No se priorizó estética visual sino claridad funcional.

## Ejecución
El punto de entrada del proyecto es:

- `main.py`

Ejecución desde terminal:
```powershell
python main.py
```

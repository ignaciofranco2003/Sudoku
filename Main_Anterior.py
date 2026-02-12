from SudokuLogica import SudokuLogica

logica = SudokuLogica() # Creamos una instancia de la clase que se encarga de hablar con Prolog

print("\n--- PRUEBA 1: Resolver Tablero ---")
# El número 0 representa casillas vacias en los sudokus
tablero_test = [
    [0, 0, 3, 0, 0, 0, 0, 7, 4],
    [0, 0, 0, 7, 0, 0, 3, 0, 0],
    [0, 7, 4, 3, 2, 1, 0, 9, 0],
    [6, 0, 0, 0, 0, 0, 8, 4, 0],
    [0, 3, 0, 0, 6, 0, 9, 0, 0],
    [0, 0, 9, 8, 5, 3, 2, 0, 1],
    [4, 0, 0, 6, 0, 5, 0, 0, 9],
    [0, 0, 0, 0, 1, 8, 0, 3, 2],
    [0, 0, 6, 0, 7, 0, 0, 8, 5]
]

solucion = logica.resolver(tablero_test)
# Llamamos al método resolver, que usa Prolog para completar el tablero
if solucion:
    print("Prolog llego a una solucion")
    for fila in solucion:
        print(fila)
else:
    print("No se encontro solucion (o el tablero era invalido).")

print("\n--- PRUEBA 2: Generar Nuevo tablero completo ---")
# Pedimos a Prolog un tablero totalmente resuelto desde cero
completo = logica.generar()
print("\nTablero generado por Prolog:")
for fila in completo:
    print(fila)

print("\n--- PRUEBA 3: Generar Nuevo con huecos---")
# Genera un tablero completo, pero después le borra algunas casillas (pone ceros)
nuevo = logica.generar_incompleto()
print("\nTablero generado por Prolog:")
for fila in nuevo:
    print(fila)

print("\n--- PRUEBA 4: verificar si uno completo es valido (con el generado en el punto 2)---")
# Le pedimos a Prolog que intente resolver el tablero completo generado antes
# Si Prolog lo puede resolver, significa que era correcto
solucion = logica.resolver(completo)
if solucion:
    print("El tablero es valido")
else:
    print("El tablero era invalido")

print("\n--- PRUEBA 5: Generar una solucion valida (con el generado en el punto 3)---")
# Ahora probamos resolver el tablero incompleto generado en la prueba 3
solucion = logica.resolver(nuevo)
if solucion:
    print("Prolog llego a una solucion")
    for fila in solucion:
        print(fila)
else:
    print("No se encontro solucion (o el tablero era invalido).")
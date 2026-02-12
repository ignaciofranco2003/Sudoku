:- use_module(library(clpfd)).  % Librería restricciones lógicas para resolver el Sudoku
:- use_module(library(random)). % Librería generar valores aleatorios
:- set_random(seed(random)).    % Semilla aleatoria con un valor no determinista

% Predicado principal
% Recibe un tablero de 9 filas con 9 columnas (lista de listas)
sudoku(Tablero) :-
    
    % 1. Validación de Estructura
    length(Tablero, 9),                     % El tablero debe tener 9 filas
    maplist(same_length(Tablero), Tablero), % Cada fila debe tener 9 columnas (matriz 9x9)

    % 2. Definición del Dominio
    append(Tablero, Celdas),    % Aplanamos la matriz para obtener una lista con las 81 celdas (convertimos todas las celdas en una sola lista)
    Celdas ins 1..9,            % Cada celda solo puede tener números del 1 al 9

    % 3. Restricciones del Sudoku
    
    % A. Filas: todos los elementos (números) de cada fila deben ser distintos
    maplist(all_distinct, Tablero),

    % B. Columnas: para tratarlas más fácil, transponemos el tablero (convertimos columnas en filas)
    transpose(Tablero, Columnas),
    maplist(all_distinct, Columnas),    % En cada columna los valores deben ser distintos (al igual que se hace con las filas)

    % C. Bloques 3x3: comprobamos que cada bloque (subcuadrrante) tenga valores distintos
    % Dividimos el tablero en grupos de 3 filas.
    Tablero = [F1, F2, F3, F4, F5, F6, F7, F8, F9],
    bloques(F1, F2, F3),
    bloques(F4, F5, F6),
    bloques(F7, F8, F9),

    % 4. Búsqueda de soluciones.
    % Mezclamos las celdas para que cada ejecución genere una solución distinta
    random_permutation(Celdas, Celdas_Aleatorias),

    % Buscamos valores concretos que cumplan todas las reglas
    labeling([ff],Celdas_Aleatorias).

% -----------------------------------------------------------------------------

% Predicado auxiliar (bloques)
% Toma 3 filas y las procesa de a grupos de 3 elementos
bloques([], [], []).
bloques([A,B,C|Cola1], [D,E,F|Cola2], [G,H,I|Cola3]) :-
    % Todos los 9 valores del bloque 3x3 deben ser distintos
    all_distinct([A,B,C,D,E,F,G,H,I]),
    bloques(Cola1, Cola2, Cola3).

% -----------------------------------------------------------------------------
% Regla para generar un tablero completo válido
generar_tablero(Tablero) :-
    length(Tablero, 9),                     % 9 filas
    maplist(same_length(Tablero), Tablero), % Cada fila tiene 9 columnas
    sudoku(Tablero).                        % Resuelve y obtiene un tablero válido
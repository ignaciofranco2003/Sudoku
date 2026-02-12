TAM = 9          # Tamaño del tablero (9x9 celdas en un Sudoku)
CELL = 52        # Tamaño en píxeles de cada celda individual
MARGIN = 12      # Margen en píxeles alrededor del tablero

BOARD = TAM * CELL      # Tamaño total del tablero sin márgenes (ancho y alto)

CANVAS_W = BOARD + 2 * MARGIN   # Ancho total del canvas (tablero + márgenes)
CANVAS_H = BOARD + 2 * MARGIN   # Alto total del canvas (tablero + márgenes)

PANEL_W = 280    # Ancho del panel derecho (botones, configuraciones, estado)

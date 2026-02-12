from pyswip import Prolog
import random

class SudokuLogica:
    def __init__(self, ruta_archivo="sudoku.pl"):
        # Inicializamos el motor de Prolog
        self.prolog = Prolog()
        # Cargamos el archivo de reglas (Base de Conocimiento)
        try:
            self.prolog.consult(ruta_archivo)
            print(f"Base de conocimientos '{ruta_archivo}' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar Prolog: {e}")

    def _python_a_prolog_str(self, tablero):
        """
        Transforma una matriz de Python (con 0s) a un string de lista Prolog (con _).
        Programacion Funcional: Usamos map y join para evitar bucles imperativos.
        
        Ejemplo:
        Entrada: [[5, 0, ...], ...]
        Salida: "[[5, _, ...], ...]"
        """
        # Función lambda que convierte cada celda: si es 0 = devuelve '_' // si es un número = lo deja igual
        convertir_celda = lambda x: str(x) if x > 0 else "_"

        # Convertimos cada fila
        filas = [f"[{','.join(map(convertir_celda, fila))}]" for fila in tablero]

        # Unimos las filas en una lista de listas
        return f"[{','.join(filas)}]"

    def resolver(self, tablero_entrada):
        # Recibe un tablero incompleto, consulta a Prolog y devuelve la primera solución encontrada.
        tablero_str = self._python_a_prolog_str(tablero_entrada)    # Convertimos el tablero Python al formato que usa Prolog
        consulta = f"Tablero = {tablero_str}, sudoku(Tablero)"      # Definimos la consulta para que Prolog resuelva el Sudoku
        # Ejecutamos la consulta (puede devolver varias soluciones, nos quedamos con la primera)
        generador = self.prolog.query(consulta)
        resultado = next(generador, None)
        generador.close()
        # Si hubo solución, la devolvemos, si no, devolvemos None
        return resultado['Tablero'] if resultado else None

    def generar(self):
        """
        Pide a Prolog que genere un tablero completo válido
        Retorna la primera solución encontrada o una lista vacía si no hay solución
        """
        consulta = "generar_tablero(X)"
        generador_consulta = self.prolog.query(consulta)
        resultado = next(generador_consulta, None)
        generador_consulta.close()
        return resultado['X'] if resultado else []

    def generar_incompleto(self, pistas):
        """
        Genera un tablero válido pero con casillas vacías
        Primero genera un tablero completo usando Prolog y elige la cantidad de pistas que vienen por parametros 
        para determinar cuantas posiciones quedan visibles, el resto se reemplaza con un 0
        """
        tablero_completo = self.generar()   # Generamos un tablero completo

        # Validación funcional: lanzamos excepción ante tablero inválido
        assert tablero_completo and len(tablero_completo) == 9, "Tablero mal formado"

        # cantidad = random.randint(20, 35)   # Elegimos cuántos números dejar visibles
        cantidad = pistas   # Elegimos cuántos números dejar visibles
        posiciones = list(map(lambda x: divmod(x, 9), range(81)))   # Creamos una lista con todas las posiciones posibles del tablero (0 a 80)
        visibles = set(random.sample(posiciones, k=cantidad))   # Elegimos al azar cuáles posiciones van a quedar visibles

        # Construimos el nuevo tablero con casillas vacías
        tablero_con_huecos = list(
            map(
                lambda f: list(
                    map(
                        lambda c: tablero_completo[f][c] if (f, c) in visibles else 0,
                        range(9)
                    )
                ),
                range(9)
            )
        )
        return tablero_con_huecos
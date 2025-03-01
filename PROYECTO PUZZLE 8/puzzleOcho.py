class Puzzle:
    # Constructor de la clase
    def __init__(self, estado_inicial, estado_objetivo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
    # Funcion para encontrar la posicion de un valor en el estado
    def encontrar_posicion(self, estado, valor):
        for fila in range(3):
            for columna in range(3):
                if estado[fila][columna] == valor:
                    return fila, columna
        return None
    # Funcion para calcular la distancia manhattan
    def calcular_distancia_manhattan(self, estado):
        distancia_total = 0
        for fila in range(3):
            for columna in range(3):
                valor = estado[fila][columna]
                if valor != 0:
                    fila_objetivo, columna_objetivo = self.encontrar_posicion(self.estado_objetivo, valor)
                    distancia_total += abs(fila - fila_objetivo) + abs(columna - columna_objetivo)
        return distancia_total
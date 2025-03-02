# Aguilar Recio Jesús Octavio
# Flores Fernandez Emily Karely

import heapq
import time

class Puzzle:
    #Constructor de la clase
    def __init__(self, estado_inicial, estado_objetivo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo

    #Fucion para validar si los estados tienen las mismas fichas
    def validar_estados(self):
        #Convertimos los estados en listas planas
        estado_inicial_flat = [ficha for fila in self.estado_inicial for ficha in fila]
        estado_objetivo_flat = [ficha for fila in self.estado_objetivo for ficha in fila]

        return sorted(estado_inicial_flat) == sorted(estado_objetivo_flat)

    #Funcion para validar si el tablero ya está resuelto
    def validar_solucion(self):
        return self.estado_inicial == self.estado_objetivo

    #Funcion para encontrar la posicion de un valor en el estado
    def encontrar_posicion(self, estado, valor):
        for fila in range(3):
            for columna in range(3):
                if estado[fila][columna] == valor:
                    return fila, columna
        return None
    
    #Funcion para calcular la distancia manhattan
    def calcular_distancia_manhattan(self, estado):
        distancia_total = 0
        for fila in range(3):
            for columna in range(3):
                valor = estado[fila][columna]
                if valor != 0: #El 0 no se cuenta ya que es el espacio vacio
                    fila_objetivo, columna_objetivo = self.encontrar_posicion(self.estado_objetivo, valor)
                    distancia_total += abs(fila - fila_objetivo) + abs(columna - columna_objetivo)
        return distancia_total
    
    #Funcion para obtener los vecinos del estado
    def obtener_vecinos(self, estado):
        vecinos = []
        fila_blanco, columna_blanco = self.encontrar_posicion(estado, 0)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #arriba, abajo, izquierda, derecha
        for mov_fila, mov_columna in movimientos:
            nueva_fila, nueva_columna = fila_blanco + mov_fila, columna_blanco + mov_columna
            if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:
                nuevo_estado = [fila[:] for fila in estado]
                nuevo_estado[fila_blanco][columna_blanco], nuevo_estado[nueva_fila][nueva_columna] = nuevo_estado[nueva_fila][nueva_columna], nuevo_estado[fila_blanco][columna_blanco]
                vecinos.append(nuevo_estado)
        return vecinos
    
    #Funcion para resolver el puzzle utilizando el algoritmo A* y heuristica manhattan
    def resolver_Puzzle(self):

        if self.validar_solucion():
            return [self.estado_inicial]
        
        if not self.validar_estados():
            return None
        
        lista_prioridad = []
        heapq.heappush(lista_prioridad, (0, self.estado_inicial, []))
        visitados = set()
        
        while lista_prioridad:
            _, estado_actual, camino = heapq.heappop(lista_prioridad)
            if estado_actual == self.estado_objetivo:
                return camino + [estado_actual]
            
            visitados.add(tuple(map(tuple, estado_actual)))
            
            for vecino in self.obtener_vecinos(estado_actual):
                if tuple(map(tuple, vecino)) not in visitados: # Si el vecino no ha sido visitado se agregará a la lista de prioridad
                    costo_g = len(camino) + 1
                    costo_h = self.calcular_distancia_manhattan(vecino)
                    heapq.heappush(lista_prioridad, (costo_g + costo_h, vecino, camino + [estado_actual]))
        return None

def imprimir_estado(estado):
    for fila in estado:
        print(fila)
    print()

def main():
    estado_inicial = [
        [0, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
    estado_objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    puzzle = Puzzle(estado_inicial, estado_objetivo)
    
    if puzzle.validar_solucion():
        print("El tablero ya está resuelto")
        return
    
    if not puzzle.validar_estados():
        print("Error: Los estados inicial y final no tienen las mismas fichas")
        return
    
    inicio_tiempo = time.time()
    solucion = puzzle.resolver_Puzzle()
    fin_tiempo = time.time()
    
    if solucion:
        for paso, estado in enumerate(solucion):
            print(f"Paso {paso}:")
            imprimir_estado(estado)
        print(f"Total de movimientos: {len(solucion) - 1}")
        print(f"Tiempo de ejecucion: {fin_tiempo - inicio_tiempo:.1f} segundos")
    else:
        print("No se encontro solucion")

if __name__ == "__main__":
    main()   
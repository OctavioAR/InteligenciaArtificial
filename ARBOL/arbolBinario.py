from nodo import Nodo
class ArbolBinario:
    def __init__(self):
        # Inicializar el árbol
        self.raiz = None

    def insertar(self, dato):
        # Método para insertar una nueva clave en el árbol
        if self.raiz is None:
            self.raiz = Nodo(dato)
        else:
            self._insertar_recursivo(self.raiz, dato)

    def _insertar_recursivo(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self._insertar_recursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self._insertar_recursivo(nodo.derecha, dato)

    def buscar(self, dato):
        # Método para buscar una clave en el árbol
        return self._buscar_recursivo(self.raiz, dato)

    def _buscar_recursivo(self, nodo, dato):
        if nodo is None or nodo.dato == dato:
            return nodo
        if dato < nodo.dato:
            return self._buscar_recursivo(nodo.izquierda, dato)
        else:
            return self._buscar_recursivo(nodo.derecha, dato)

    def imprimir_arbol(self):
        # Método para imprimir el árbol en orden
        self._imprimir_recursivo(self.raiz)

    def _imprimir_recursivo(self, nodo):
        if nodo is not None:
            self._imprimir_recursivo(nodo.izquierda)
            print(nodo.dato, end=' ')
            self._imprimir_recursivo(nodo.derecha)
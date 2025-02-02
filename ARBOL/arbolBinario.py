from nodo import Nodo

class Arbol:
    # Metodo construntor clase arbol
    def __init__(self):
        # inicializamos el arbol con la raiz nula
        self.raiz = None

    # Metodo para insertar un dato en el arbol
    def insertar(self, dato):
        if self.raiz is None:
            self.raiz = Nodo(dato)
        else:
            self.insertarRecursivo(self.raiz, dato)

    
    def insertarRecursivo(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self.insertarRecursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self.insertarRecursivo(nodo.derecha, dato)
 
    # Metodo para buscar un dato en el arbol
    def buscar(self, dato):
        return self.buscarRecursivo(self.raiz, dato)
    
    def buscarRecursivo(self, nodo, dato):
        if nodo is None or nodo.dato == dato:
            return nodo
        if dato < nodo.dato:
            return self.buscarRecursivo(nodo.izquierda, dato)
        else:
            return self.buscarRecursivo(nodo.derecha, dato)
    
    # Metodo para imprimir el arbol
    def imprimirArbol(self):
        self.imprimirRecursivo(self.raiz)
    
    # Impresion recursiva inorden
    def imprimirRecursivo(self, nodo):
        if nodo is not None:
            self.imprimirRecursivo(nodo.izquierda)
            print(nodo.dato, end=" ")
            self.imprimirRecursivo(nodo.derecha)
from arbolBinario import Arbol

if __name__ == '__main__':
    arbol = Arbol()
    arbol.insertar(70)
    arbol.insertar(31)
    arbol.insertar(93)
    arbol.insertar(94)
    arbol.insertar(14)
    arbol.insertar(23)
    arbol.insertar(73)

    print("Arbol en orden: ")
    arbol.imprimirArbol()

    buscar = 31

    resultado = arbol.buscar(buscar)
    if resultado:
        print(f"\n{buscar} encontrado en el arbol")
    else:
        print(f"\n{buscar} no encontrado en el arbol")

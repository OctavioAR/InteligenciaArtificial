from arbolBinario import ArbolBinario

if __name__ == "__main__":
    arbol = ArbolBinario()
    arbol.insertar(50)
    arbol.insertar(30)
    arbol.insertar(70)
    arbol.insertar(20)
    arbol.insertar(40)
    arbol.insertar(60)
    arbol.insertar(80)

    print("Árbol en orden:")
    arbol.imprimir_arbol()

    #clave_a_buscar = 10
    clave_a_buscar = 30
    resultado = arbol.buscar(clave_a_buscar)
    if resultado:
        print(f"\nClave {clave_a_buscar} encontrada en el árbol.")
    else:
        print(f"\nClave {clave_a_buscar} no encontrada en el árbol.")
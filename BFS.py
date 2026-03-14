from arbol import Nodo

def busca_solucion_BFS(estado_inicial, solucion):
    solucionado = False 
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    
    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0) # FIFO (Primero en entrar, primero en salir)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            
            # --- OPERADORES ---
            # Operador Izquierda (Intercambia pos 0 y 1)
            hijo_izq_datos = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izquierdo = Nodo(hijo_izq_datos)
            hijo_izquierdo.set_padre(nodo) # <--- IMPORTANTE para imprimir el camino

            if not hijo_izquierdo.en_lista(nodos_visitados) and not hijo_izquierdo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izquierdo)

            # Operador Centro (Intercambia pos 1 y 2)
            hijo_cen_datos = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_central = Nodo(hijo_cen_datos)
            hijo_central.set_padre(nodo)

            if not hijo_central.en_lista(nodos_visitados) and not hijo_central.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_central)

            # Operador Derecho (Intercambia pos 2 y 3)
            hijo_der_datos = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_derecho = Nodo(hijo_der_datos)
            hijo_derecho.set_padre(nodo)

            if not hijo_derecho.en_lista(nodos_visitados) and not hijo_derecho.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_derecho)

            nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

# --- BLOQUE DE EJECUCIÓN (FUERA DE LA FUNCIÓN) ---
if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    
    print("Buscando solución...")
    nodo_solucion = busca_solucion_BFS(estado_inicial, solucion)
    
    if nodo_solucion is not None:
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        
        resultado.append(estado_inicial)
        resultado.reverse()
        
        print("\n¡Solución encontrada en Amplitud!")
        for i, paso in enumerate(resultado):
            print(f"Paso {i}: {paso}")
    else:
        print("No se encontró solución.")
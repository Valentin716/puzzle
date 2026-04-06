#Puzzle lineal con busqueda en profundidad BFS
from arbol import Nodo
def buscar_solucion_DFS(estado_inical, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inical)
    nodos_frontera.append(nodoInicial)
    while(not solucionado) and len (nodos_frontera):
        nodo = nodos_frontera.pop()
        #Ext4raer el nodo y añadirlo a visitados
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            #solucion encontrada
            solucion = True
            return nodo
        else:
            #Expandir nodos hijo
            dato_nodo= nodo.get_datos()

            #Operador Izquierdo
            hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_izquierdo = Nodo(hijo)
            if not hijo_izquierdo.en_lista(nodos_visitados) and not hijo_izquierdo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izquierdo)
            
             #Operador Central
            hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_central = Nodo(hijo)
            if not hijo_central.en_lista(nodos_visitados) and not hijo_central.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_central)
            
             #Operador derecho
            hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_derecho = Nodo(hijo)
            if not hijo_derecho.en_lista(nodos_visitados) and not hijo_derecho.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_derecho)

            nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

if __name__ == "__main__":
     estado_inical = [4, 2, 3, 1]
     solucion = [1, 2, 3, 4]
     nodo_solucion = buscar_solucion_DFS(estado_inical, solucion)
     #Mostrar resultado
     resultado = []
     nodo = nodo_solucion
     while nodo.get_padre () != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
        resultado.append(estado_inical)
        resultado.reverse()
        print(resultado)
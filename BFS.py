import streamlit as st
from arbol import Nodo

def busca_solucion_BFS(estado_inicial, solucion):
    solucionado = False 
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    
    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            
            hijo_izq_datos = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izquierdo = Nodo(hijo_izq_datos)
            hijo_izquierdo.set_padre(nodo)

            if not hijo_izquierdo.en_lista(nodos_visitados) and not hijo_izquierdo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izquierdo)

            hijo_cen_datos = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_central = Nodo(hijo_cen_datos)
            hijo_central.set_padre(nodo)

            if not hijo_central.en_lista(nodos_visitados) and not hijo_central.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_central)

            hijo_der_datos = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_derecho = Nodo(hijo_der_datos)
            hijo_derecho.set_padre(nodo)

            if not hijo_derecho.en_lista(nodos_visitados) and not hijo_derecho.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_derecho)

            nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])
    return None

# --- INTERFAZ WEB CON STREAMLIT ---
# Esto reemplaza los print() tradicionales
st.title("🧩 Resolución de Puzzle Lineal")
st.subheader("Búsqueda en Amplitud (BFS)")

st.write("**Estado inicial:** `[4, 2, 3, 1]`")
st.write("**Solución deseada:** `[1, 2, 3, 4]`")

# Creamos un botón en la web
if st.button("Buscar Solución"):
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    
    # Muestra un ícono de carga mientras el algoritmo procesa
    with st.spinner("Calculando la mejor ruta..."):
        nodo_solucion = busca_solucion_BFS(estado_inicial, solucion)
    
    if nodo_solucion is not None:
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        
        resultado.append(estado_inicial)
        resultado.reverse()
        
        st.success("¡Solución encontrada!")
        
        # Muestra cada paso en una caja bonita
        for i, paso in enumerate(resultado):
            st.info(f"Paso {i}: {paso}")
    else:
        st.error("No se encontró solución.")
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import deque

# --- 1. CONFIGURACIÓN INICIAL ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PuzzleRequest(BaseModel):
    estado_inicial: List[int]
    solucion: List[int]

# --- 2. CLASE NODO ---
class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
    def get_datos(self): return self.datos
    def get_padre(self): return self.padre

# --- 3. LÓGICA DE BÚSQUEDA (MULTIPLE) ---
def buscar_varias_soluciones(estado_inicial, solucion_esperada, cantidad=12):
    nodos_frontera = deque([Nodo(estado_inicial)])
    soluciones_encontradas = []
    # Para encontrar 12 rutas distintas, limitamos la profundidad para no entrar en bucles infinitos
    max_profundidad = 15 

    while len(nodos_frontera) > 0 and len(soluciones_encontradas) < cantidad:
        nodo = nodos_frontera.popleft()
        
        # Calcular profundidad actual
        profundidad = 0
        p = nodo.get_padre()
        while p:
            profundidad += 1
            p = p.get_padre()
        
        if profundidad > max_profundidad: continue

        if nodo.get_datos() == solucion_esperada:
            ruta = []
            temp = nodo
            while temp:
                ruta.append(temp.get_datos())
                temp = temp.get_padre()
            ruta.reverse()
            # Evitamos duplicados exactos de rutas
            if ruta not in soluciones_encontradas:
                soluciones_encontradas.append(ruta)
            continue

        dato = nodo.get_datos()
        # Operadores
        movimientos = [
            [dato[1], dato[0], dato[2], dato[3]], # Central
            [dato[0], dato[2], dato[1], dato[3]], # Izquierdo
            [dato[0], dato[1], dato[3], dato[2]]  # Derecho
        ]

        for m in movimientos:
            # Para hallar MUCHAS rutas, permitimos volver a estados anteriores
            # siempre que no sea el padre inmediato (evitar rebote simple)
            if nodo.get_padre() and m == nodo.get_padre().get_datos():
                continue
            nodos_frontera.append(Nodo(m, padre=nodo))
            
    return soluciones_encontradas

# --- 4. ENDPOINT ---
@app.post("/resolver")
def resolver_puzzle(request: PuzzleRequest):
    resultados = buscar_varias_soluciones(request.estado_inicial, request.solucion, 12)
    
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron rutas")

    return {
        "cantidad_soluciones": len(resultados),
        "soluciones": resultados
    }
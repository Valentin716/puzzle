from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # <-- IMPORTANTE
from pydantic import BaseModel
from typing import List

# --- 1. CONFIGURACIÓN DE FASTAPI ---
app = FastAPI(title="API Puzzle DFS")

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
        self.hijos = []
        
    def get_datos(self): 
        return self.datos
        
    def set_hijos(self, hijo_izq, hijo_cen, hijo_der): 
        hijo_izq.padre = self
        hijo_cen.padre = self
        hijo_der.padre = self
        self.hijos = [hijo_izq, hijo_cen, hijo_der]
        
    def get_hijos(self): 
        return self.hijos
        
    def get_padre(self): 
        return self.padre

# --- 3. ALGORITMO DFS ---
def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    
    if nodo_inicial.get_datos() == solucion: 
        return nodo_inicial
    else:
        dato_nodo = nodo_inicial.get_datos()
        
        hijo = list(dato_nodo)
        hijo[0], hijo[1] = hijo[1], hijo[0]
        hijo_izquierdo = Nodo(tuple(hijo))
        
        hijo = list(dato_nodo)
        hijo[1], hijo[2] = hijo[2], hijo[1]
        hijo_central = Nodo(tuple(hijo))
        
        hijo = list(dato_nodo)
        hijo[2], hijo[3] = hijo[3], hijo[2]
        hijo_derecho = Nodo(tuple(hijo))
        
        nodo_inicial.set_hijos(hijo_izquierdo, hijo_central, hijo_derecho)

    for nodo_hijo in nodo_inicial.get_hijos():
        if not nodo_hijo.get_datos() in visitados:
            sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol
    return None

# --- 4. RUTA PARA MOSTRAR TU PÁGINA WEB ---
@app.get("/")
def mostrar_pagina_web():
    # Esto buscará tu archivo HTML y lo mostrará en el navegador
    return FileResponse("index.html")

# --- 5. RUTA PARA CALCULAR LA SOLUCIÓN ---
@app.post("/resolver")
def resolver_puzzle(request: PuzzleRequest):
    visitados = []
    nodo_inicial = Nodo(tuple(request.estado_inicial))
    solucion_tupla = tuple(request.solucion)
    
    nodo_solucion = buscar_solucion_DFS_rec(nodo_inicial, solucion_tupla, visitados)
    
    if not nodo_solucion:
        raise HTTPException(status_code=404, detail="No se encontró una ruta")

    resultado = []
    nodo_actual = nodo_solucion
    while nodo_actual is not None:
        resultado.append(list(nodo_actual.get_datos()))
        nodo_actual = nodo_actual.get_padre()
        
    resultado.reverse()

    return {"mejor_ruta": resultado}
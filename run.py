import GameOfSensors as GoS
from sensors import Sensor
from sinks import Sink
import numpy as np

def creaNodos(n):
    nodos = []
    for _ in range(n):
        x = np.random.random()*GoS.areaX
        y = np.random.random()*GoS.areaY
        nodos.append(Sensor('', x, y))
    return nodos

def creaMensaje(nodos):
    condicion = True
    while condicion:
        mensajero = np.random.choice(nodos)
        if mensajero.bateria >= GoS.pcktTx:
            mensajero.task = 'tx'
            GoS.canalLibre = False
            condicion = False

def dinamica(nodos):
    for nodo in nodos:
        if nodo.bateria < GoS.helloTx:
            if nodo.task == 'tx' or nodo.nextTask == 'tx':
                GoS.canalLibre = True
            for vecino in nodo.vecindad:
                vecino.vecindad.remove(nodo)
            nodos.remove(nodo)
            break
        nodo.activos()
        nodo.juegoVida()
        nodo.cicloTrabajo()
    for nodo in nodos:
        nodo.aStar(nodos)

def updateTask(nodos):
    for nodo in nodos:
        nodo.task = nodo.nextTask

if __name__ == '__main__':
    recibidos = 0 
    sink  = Sink()
    sensores = creaNodos(GoS.nSensors)
    for nodo in sensores:
        nodo.creaVecindad(sensores)

    while len(sensores) >= 0:
        if GoS.canalLibre == True:
            creaMensaje(sensores)
        dinamica(sensores)
        #for nodo in sensores:
        #    print(len(nodo.vecindad), nodo.vecinosActivos, nodo.task, nodo.nextTask)
        updateTask(sensores)
        #input()
#        if GoS.nPcktTx > 8000:
#            for nodo in sensores:
#                if nodo.task  == 'tx':
#                    print(GoS.nPcktTx, len(sensores))
#                    print(nodo.x, nodo.y)
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
            nodos.remove(nodo)
            break
        nodo.activos()
        nodo.juegoVida()
        nodo.cicloTrabajo()
    for nodo in nodos:
        nodo.aStar()

def updateTask(nodos):
    for nodo in nodos:
        nodo.task = nodo.nextTask

if __name__ == '__main__':
    sink  = Sink()
    sensores = creaNodos(GoS.nSensors)
    for nodo in sensores:
        nodo.creaVecindad(sensores)

    for i in range(15):
        if GoS.canalLibre == True:
            creaMensaje(sensores)
        for sensor in sensores:
            if sensor.task == 'tx':
                print(sensor.x, sensor.y)
        dinamica(sensores)
        updateTask(sensores)
import numpy as np
import math
import GameOfSensors as GoS

class Sensor:
    def __init__(self, task, x, y):
        self.task = task
        self.nextTask = ''
        if task == '':
            # 'a' => active
            # 'i' => idle
            self.task = np.random.choice(['a', 'i'])
        else:
            self.task = self.task
        self.x = x
        self.y = y
        self.vecindad = []
        self.tiempoActivo = 0
        self.tiempoInactivo = 0
        self.bateria = GoS.initialEnergy
        self.reachSink = False

    def creaVecindad(self, sensores):
        for sensor in sensores:
            if self != sensor:
                if (self.x-sensor.x)**2 + (self.y-sensor.y)**2 <= GoS.txRange**2: # Vecindad de Moore de radio 1
                    self.vecindad.append(sensor)
            if (self.x-GoS.sinkX)**2 + (self.y-GoS.sinkY)**2 <= GoS.txRange**2:
                self.reachSink = True

    def activos(self):
        self.vecinosActivos = 0
        for elemento in self.vecindad:
            if elemento.task!='i':
                self.vecinosActivos += 1
        self.bateria -= self.vecinosActivos * GoS.helloRx

    def juegoVida(self):
        if self.task == 'a':
            self.nextTask = 'a'
            self.bateria -= GoS.helloTx
            if self.vecinosActivos < math.floor((2/8)*len(self.vecindad)):
                self.nextTask = 'i'
            if self.vecinosActivos > math.ceil((3/8)*len(self.vecindad)):
                self.nextTask = 'i'
        elif self.task == 'i':
            self.nextTask = 'i'
            rb = int((3/8)*len(self.vecindad))
            if self.vecinosActivos == rb:
                self.nextTask = 'a'
    
    def cicloTrabajo(self):
        if self.task == 'a':
            self.tiempoActivo += 1
            self.tiempoInactivo = 0
        if self.task == 'i':
            self.tiempoInactivo += 1
            self.tiempoActivo = 0
        if self.task == 'tx':
            self.tiempoActivo = 1
            self.tiempoInactivo = 0
        if self.tiempoActivo >= 5:
            self.nextTask = 'i'
        if self.tiempoInactivo >= 5:
            self.nextTask = 'a'

    def aStar(self):
        if self.task == 'tx':
            self.nextTask = 'tx'
            if self.reachSink:
                self.bateria -= GoS.pcktTx
                self.nextTask = 'i'
                GoS.canalLibre = True
            else:
                actualF = np.inf
                actualH = ((self.x - GoS.sinkX)**2 + (self.y - GoS.sinkY)**2)
                nextJump = self
                for vecino in self.vecindad:
                    if vecino.task != 'i':
                        vecinoG = ((self.x - vecino.x)**2 + (self.y - vecino.y)**2)
                        vecinoH = ((vecino.x - GoS.sinkX)**2 + (vecino.y - GoS.sinkY)**2)
                        vecinoF = vecinoG + vecinoH
                        if vecinoF < actualF:
                            actualF = vecinoF
                            if vecinoH < actualH:
                                nextJump = vecino
                if nextJump.x != self.x or nextJump.y != self.y:
                    self.bateria -= GoS.pcktTx
                    self.nextTask = 'i'
                    nextJump.bateria -= GoS.pcktRx
                    nextJump.nextTask = 'tx'
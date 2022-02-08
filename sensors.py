import numpy as np
import GameOfSensors as GoS

class Sensor:
    def __init__(self, task, x, y):
        self.task = task
        self.nextTask = ''
        if task == '':
            # 'a' => active
            # 'i' => idle
            self.nextTask = np.random.choice(['a', 'i'])
        else:
            self.nextTask = self.task
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
            self.bateria -= GoS.helloTx
            if self.vecinosActivos < 2:
                self.nextTask = 'i'
            if self.vecinosActivos > 3:
                self.nextTask = 'i'
        elif self.task == 'i':
            if self.vecinosActivos == 3:
                self.nextTask = 'a'
    
    def cicloTrabajo(self):
        if self.tiempoActivo > 10:
            self.nextTask = 'i'
        if self.tiempoInactivo > 10:
            self.nextTask = 'a'
        if self.task == 'a':
            self.tiempoActivo += 1
            self.tiempoInactivo = 0
        if self.task == 'i':
            self.tiempoInactivo += 1
            self.tiempoActivo = 0
        if self.task == 'tx':
            self.tiempoActivo = 1
            self.tiempoInactivo = 0

    def aStar(self):
        if self.task == 'tx':
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
                    nextJump.NextTask = 'tx'
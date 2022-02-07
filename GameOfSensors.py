import numpy as np

if __name__ == '__main__':
    areaX = 200
    areaY = 200
    nSensors = 50
    txRange = 80
    sinkX = 200
    sinkY = 200
    initialEnergy = 5
    eElec = 50e-09
    eAmp = 100e-12
    pcktSize = 500*8
    pcktTx = pcktSize*(eElec + (eAmp*(txRange**2)))
    pcktRx = pcktSize*eElec
    helloSize = 200
    helloTx = helloSize*(eElec + (eAmp*(txRange**2)))
    helloRx = helloSize*eElec

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
        self.bateria = initialEnergy

    def creaVecindad(self, sensores):
        for sensor in sensores:
            if self != sensor:
                if (self.x-sensor.x)**2 + (self.y-sensor.y)**2 <= txRange**2: # Vecindad de Moore de radio 1
                    self.vecindad.append(sensor)

    def activos(self):
        self.vecinosActivos = 0
        for elemento in self.vecindad:
            if elemento.task!='i':
                self.vecinosActivos += 1
        self.bateria -= self.vecinosActivos * helloRx

    def juegoVida(self):
        if self.task == 'a':
            self.bateria -= helloTx
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

class Sink:
    def __init__(self):
        self.x = sinkX
        self.y = sinkY
        # 's' => sink
        self.task = 's'
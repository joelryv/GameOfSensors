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

class Sensor:
    def __init__(self, task, x, y):
        self.task = task
        if task == '':
            # 'a' => active
            # 'i' => idle
            self.task = np.random.choice(['a', 'i'])
        self.x = x
        self.y = y
        self.vecindad = []
        self.tiempoActivo = 0
        self.tiempoInactivo = 0
        self.bateria = initialEnergy
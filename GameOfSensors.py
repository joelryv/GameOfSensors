import numpy as np

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
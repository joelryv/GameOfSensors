import numpy as np

canalLibre = True
np.random.seed(0)
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
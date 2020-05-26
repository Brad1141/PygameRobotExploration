import random
import math
import matplotlib.pyplot as plt
import numpy as np
from Classes import SLAM

percentError = 1
position = [0, 0]
laserReadings = []

SlamPosX = []
SlamPosY = []
SlamLX = []
SlamLY = []

# change values according to percent error
# distance must be postive for this to work
def addErrors(sensors, rX, rY):
    # east
    sensors[0] = random.randint(int((1 - (percentError / 100)) * sensors[0]),
                                int((1 + (percentError / 100)) * sensors[0])) if sensors[0] > 0 else 0

    # north
    sensors[1] = random.randint(int((1 - (percentError / 100)) * sensors[1]),
                                int((1 + (percentError / 100)) * sensors[1])) if sensors[1] > 0 else 0

    # west
    sensors[2] = random.randint(int((1 - (percentError / 100)) * sensors[2]),
                                int((1 + (percentError / 100)) * sensors[2])) if sensors[2] > 0 else 0

    # south
    sensors[3] = random.randint(int((1 - (percentError / 100)) * sensors[3]),
                                int((1 + (percentError / 100)) * sensors[3])) if sensors[3] > 0 else 0

    # robot width
    position[0] = random.randint(int((1 - (percentError / 100)) * rX),
                                 int((1 + (percentError / 100)) * rX)) if rX > 0 else 0

    # robot height
    position[1] = random.randint(int((1 - (percentError / 100)) * rY),
                                 int((1 + (percentError / 100)) * rY)) if rY > 0 else 0

    return sensors, position


def setPercentError(self, newError):
    percentError = newError


def printCoords():

    #gray is robot, blue is landmark
    plt.scatter(SlamPosX, SlamPosY, s=(np.pi * 20), c=(0, 0, 0), alpha=0.5)
    plt.scatter(SlamLX, SlamLY, s=(np.pi * 20))
    plt.axes((0, 3200, 0, 3200))
    plt.show()

class coordinates:
    def __init__(self, distance, angle):
        self.angle = angle
        self.x = distance[0]
        self.y = distance[1]

def addCoords(sensors, position):
    for i in range(len(sensors)):
        if i == 0:
            xy = [position[0] + sensors[i] + 64, position[1]]
            newCoord = coordinates(xy, i * 90)
            laserReadings.append(newCoord)
        elif i == 1:
            xy = [position[0], position[1] - sensors[i]]
            newCoord = coordinates(xy, i * 90)
            laserReadings.append(newCoord)
        elif i == 2:
            xy = [position[0] - sensors[i], position[1]]
            newCoord = coordinates(xy, i * 90)
            laserReadings.append(newCoord)
        elif i == 3:
            xy = [position[0], position[1] + sensors[i] + 64]
            newCoord = coordinates(xy, i * 90)
            laserReadings.append(newCoord)

#get position of robot based off of sensor readings
def getSensorBasedPos(sensors, prevSensorData, landmark, lmAngle):
    sensorBasedPos = []
    if lmAngle == 0:
        shortDistance = prevSensorData[0] if prevSensorData[0] < sensors[0] else sensors[0]
        sensorBasedPos.append(landmark.x - (shortDistance + 64))
        sensorBasedPos.append(sensors[1])

    elif lmAngle == 90:
        shortDistance = prevSensorData[1] if prevSensorData[1] < sensors[1] else sensors[1]
        sensorBasedPos.append(sensors[2])
        sensorBasedPos.append(shortDistance + landmark.y)

    elif lmAngle == 180:
        shortDistance = prevSensorData[2] if prevSensorData[2] < sensors[2] else sensors[2]
        sensorBasedPos.append(shortDistance + landmark.x)
        sensorBasedPos.append(sensors[1])

    elif lmAngle == 270:
        shortDistance = prevSensorData[3] if prevSensorData[3] < sensors[3] else sensors[3]
        sensorBasedPos.append(sensors[2])
        sensorBasedPos.append(landmark.y - (shortDistance + 64))

    sensorBasedPos.append(0)

    return sensorBasedPos

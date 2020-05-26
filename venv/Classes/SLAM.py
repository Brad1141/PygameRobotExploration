import random
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from Classes import DataPrep
import pygame
from time import sleep

percentError = 1
position = [0, 0]
laserReadings = []
pairs = []
currentLandmarks = list()
allLandmarks = list()
currentStateEst = list()
prevPos = [0, 400]
prevSensorData = [400, 336, 736, 0]

def expGraph(x, m, b):
    return  (m * x) + b

def demoSlam(sensors, position, screen, roomCoord):
    #run the SLAM stack
    spikes(sensors, position)
    dataAssociation(sensors, position, screen, currentLandmarks)
    EKF(currentLandmarks, position, sensors, screen, roomCoord)


def spikes(sensors, position):
    global prevSensorData

    for i in range(4):
        if abs(prevSensorData[i] - sensors[i]) > 128:
            if i == 0:
                shortDistance = prevSensorData[i] if prevSensorData[i] < sensors[i] else sensors[i]
                newCoord = DataPrep.coordinates([position[0] + shortDistance + 64, position[1]], i * 90)
                currentLandmarks.append(newCoord)
            elif i == 1:
                shortDistance = prevSensorData[i] if prevSensorData[i] < sensors[i] else sensors[i]
                newCoord = DataPrep.coordinates([position[0], position[1] - shortDistance], i * 90)
                currentLandmarks.append(newCoord)
            elif i == 2:
                shortDistance = prevSensorData[i] if prevSensorData[i] < sensors[i] else sensors[i]
                newCoord = DataPrep.coordinates([position[0] - shortDistance, position[1]], i * 90)
                currentLandmarks.append(newCoord)
            elif i == 3:
                shortDistance = prevSensorData[i] if prevSensorData[i] < sensors[i] else sensors[i]
                newCoord = DataPrep.coordinates([position[0], position[1] + shortDistance + 64], i * 90)
                currentLandmarks.append(newCoord)


def dataAssociation(sensors, position, screen, lms):
    if lms and allLandmarks:
        for i in lms:
            #associate the landmark we have observed with the closest landmark that is near it
            min = math.sqrt( (i.x - allLandmarks[0].x)**2 + (i.y - allLandmarks[0].y)**2 )
            minLandmark = allLandmarks[0]
            for l in allLandmarks:
                dist = math.sqrt( (i.x - l.x)**2 + (i.y - l.y)**2 )
                if dist < min:
                    min = dist
                    minLandmark = l
            if min < ( 2 * 800 * (percentError/100)):
                #add the two together in the "pairs" list
                pairs.append([i, minLandmark])


#extended Kalman filter
def EKF(lms, position, sensors, screen, room):

    global pairs, currentLandmarks

    #update current state estimate using odometry data
    currentStateEst = [position[0], position[1],  0]

    #update the state by re-observing landmarks
    for i in pairs:
        # system state matrix
        X = [currentStateEst[0], currentStateEst[1], 0]

        # The covariance matrix
        P = []
        lmAngle = i[0].angle
        sensorBasedPos = []
        global prevSensorData
        global prevPos

        #find the robot's position based on the sensor data
        sensorBasedPos = DataPrep.getSensorBasedPos(sensors, prevSensorData, i[0], lmAngle)

        #covariance of robot state
        i_0 = [i[0].x, i[0].y, i[0].angle]
        i_1 = [i[1].x, i[1].y, i[1].angle]
        P.append(np.cov(currentStateEst, sensorBasedPos))
        P = np.array(P).reshape(2, 2)
        P = np.append(P, [[0], [0]], axis=1)
        P = np.append(P, [[0, 0, 0]], axis=0)

        #Jacobian Matrix
        H = []
        H.append((sensorBasedPos[0] - position[0]))
        H.append((sensorBasedPos[1] - position[1]))
        H.append(0)
        H.append((position[1] - sensorBasedPos[1]))
        H.append((position[0] - sensorBasedPos[0]))
        H.append(-1)
        H = np.array(H)
        H = np.resize(H, (2, 3))

        #Jacobian of the predictor model
        A = []
        A.append([1, 0, abs(prevPos[1] - position[1])])
        A.append([0, 1, abs(prevPos[0] - position[0])])
        A.append([0, 0, 1])

        #Slam specific jacobians
        J_xr = []
        J_xr.append([1, 0, abs(prevPos[1] - position[1])])
        J_xr.append([0, 1, abs(prevPos[0] - position[0])])

        J_z = []
        J_z.append([math.cos(abs(i[0].angle - i[1].angle)), -5*math.sin(abs(i[0].angle - i[1].angle))])
        J_z.append([math.sin(abs(i[0].angle - i[1].angle)), -5*math.cos(abs(i[0].angle - i[1].angle))])

        #The process noise
        W = np.array([abs(prevPos[0] - position[0]), abs(prevPos[1] - position[1]), 0])
        W = W.T
        C = 0.05
        Q = W * C * W.T

        #The measurement noise
        V = np.array([[1, 0], [0, 1]])
        R = [[sensors[int(lmAngle/90)] * (percentError/100), 0], [0, 1]]

        # Kalman gain
        P = np.asmatrix(P)
        H = np.asmatrix(H)
        V = np.asmatrix(V)
        R = np.asmatrix(R)
        X = np.asmatrix(X)
        K = P * H.T * np.asmatrix(H * P * H.T + V * R * V.T).I

        K = np.array(K).reshape(3, 2)

        currentStateEst[0] = prevPos[0] + K[0][1] * (sensorBasedPos[0] - prevPos[0])
        currentStateEst[1] = prevPos[1] + K[1][1] * (sensorBasedPos[1] - prevPos[1])

        #add the newly found coordinates to an array, adjust values according to room position
        #for example the coordinate (400, 400) in room[0][0] turns into (400, 2800)
        #this allows us to map all the landmarks and poses onto on graph
        DataPrep.SlamPosX.append(currentStateEst[0] + (800 * room[1]))
        DataPrep.SlamLX.append(i[0].x + (800 * room[1]))
        DataPrep.SlamPosY.append(currentStateEst[1] + (800 * abs(3 - room[0])))
        DataPrep.SlamLY.append(i[0].y + (800 * abs(3 - room[0])))

        # #see estimated robot position on screen
        # robotImage = pygame.image.load('venv/Images/rover.png')
        # screen.blit(robotImage, (currentStateEst[0], currentStateEst[1]))
        # pygame.display.update()
        # sleep(3)

    for l in lms:
        allLandmarks.append(l)

    prevPos = currentStateEst
    prevSensorData = sensors
    pairs = []
    currentLandmarks = []

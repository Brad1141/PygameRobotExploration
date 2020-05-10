import random

percentError = 1
position = [0, 0]

# change values according to percent error
# distance must be postive for this to work
def addErrors(sensors, rX, rY):

    #north
    sensors[0] = random.randint(int((1 - (percentError / 100)) * sensors[0]),
                               int((1 + (percentError / 100)) * sensors[0])) if sensors[0] > 0 else 0

    #south
    sensors[1] = random.randint(int((1 - (percentError / 100)) * sensors[1]),
                               int((1 + (percentError / 100)) * sensors[1])) if sensors[1] > 0 else 0
    
    #east
    sensors[2] = random.randint(int((1 - (percentError / 100)) * sensors[2]),
                               int((1 + (percentError / 100)) * sensors[2])) if sensors[2] > 0 else 0

    #west
    sensors[3] = random.randint(int((1 - (percentError / 100)) * sensors[3]),
                               int((1 + (percentError / 100)) * sensors[3])) if sensors[3] > 0 else 0

    #robot width
    position[0] = random.randint(int((1 - (percentError / 100)) * rX),
                               int((1 + (percentError / 100)) * rX)) if rX > 0 else 0

    #robot height
    position[1] = random.randint(int((1 - (percentError / 100)) * rY),
                               int((1 + (percentError / 100)) * rY)) if rY > 0 else 0
    
    return sensors, position

def setPercentError(self, newError):
    percentError = newError
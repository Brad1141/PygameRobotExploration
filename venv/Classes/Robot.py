import pygame

class Robot:

    def getSensorData(self, rX, rY, mX, mY):
        nDistance = 0
        sDistance = 0
        eDistance = 0
        wDistance = 0

        #north
        if rY > mY + 128 and mX < rX < mX + 128:
            #Note: remember that (rX,rY) and (mX,mY) gives us the top-left coordinate
            #However, we want the distance between the robot and the bottom of the moon obstacle
            #so we have to substract 128 (the moon.png is 128x128 pixels)
            nDistance = rY - mY - 128
        else:
            nDistance = rY

        #south
        if rY + 64 < mY and mX < rX < mX + 128:
            sDistance = mY - rY - 64
        else:
            sDistance = 800 - rY - 64

        #east
        if rX < mX and mY < rY < mY + 128:
            eDistance = mX - 128 - rX + 64
        else:
            eDistance = 800 - rX - 64

        #west
        if rX > mX and mY < rY < mY + 128:
            wDistance = rX - mX - 128
        else:
            wDistance = rX

        sensors = [eDistance, nDistance, wDistance, sDistance]
        return sensors


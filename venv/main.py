import pygame
from Classes import Room
from Classes import Robot
from Classes import SLAM
from Classes import DataPrep

screen = pygame.display.set_mode((800, 800))
running = True
numOfRooms = 16;

# Starting coordinates
rX = 0
rY = 400

speed = 5;
robotImage = pygame.image.load('venv/Images/rover.png')

#create 2d array of 16 rooms (4x4)
rooms = [[Room.Room() for j in range(4)] for i in range(4)]

rRow = 0;
rCol = 0;
rooms[rRow][rCol].fillRoom(screen, robotImage, rX, rY)

currentRoom = rooms[rRow][rCol]

sensors = (736, 400, 0, 336)

while running:
    # pause the program for 5 miliseconds so that it doesn't run to fast
    pygame.time.wait(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    moonRect = pygame.Rect((currentRoom.moonWidth, currentRoom.moonHeight), (128, 128))

    if keys[pygame.K_LEFT] and pygame.Rect((rX - speed, rY), (64, 64)).colliderect(moonRect) == 0 \
            and (sensors[2] - speed > 0 or rCol - 1 > -1):
        rX = rX - speed
    elif keys[pygame.K_RIGHT] and pygame.Rect((rX + speed, rY), (64, 64)).colliderect(moonRect) == 0 \
            and (sensors[0] > speed or rCol + 1 < 4):
        rX = rX + speed
    elif keys[pygame.K_UP] and pygame.Rect((rX, rY - speed), (64, 64)).colliderect(moonRect) == 0 \
            and (sensors[1] - speed > 0 or rRow - 1 > -1):
        rY = rY - speed
    elif keys[pygame.K_DOWN] and pygame.Rect((rX, rY + speed), (64, 64)).colliderect(moonRect) == 0 \
            and (sensors[3] > speed or rRow + 1 < 4):
        rY = rY + speed

    #keep track of the old row and column values
    #(this will help us if we need to flip the robot
    prevRow, prevCol = rRow, rCol

    #get the new row and column values
    rRow, rCol = currentRoom.changeRoom(rRow, rCol, rX, rY)
    currentRoom = rooms[rRow][rCol]

    #flip the robot on its X-axis
    #(for example if our robot moves to the right
    #we want to bring it back to the left when the room changes)
    if prevCol != rCol:
        rX = abs(rX - 750)
    #flip the robot on its Y-axis
    elif prevRow != rRow:
        rY = abs(rY - 750)

    # call the fillRoom function to add the robot to the screen
    rooms[rRow][rCol].fillRoom(screen, robotImage, rX, rY)

    #call the sensor data
    mX = rooms[rRow][rCol].moonWidth
    mY = rooms[rRow][rCol].moonHeight
    sensors = Robot.Robot().getSensorData(rX, rY, mX, mY)

    sensors, positions = DataPrep.addErrors(sensors, rX, rY)

    positions = [rX, rY]

    #SLAM!
    roomCoord = [rRow, rCol]
    SLAM.demoSlam(sensors, positions, screen, roomCoord)

    # update the screen
    pygame.display.update()

#print out the graph
DataPrep.printCoords()

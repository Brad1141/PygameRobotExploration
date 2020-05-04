import pygame
import sys
from Classes import Room

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

#main.py
#tells us which room to go to next (if that room exist)
def changeRoom(currentRow, currentCol):
    #go to room on the right
    if rX > 750 and currentCol + 1 < 4:
        currentCol = currentCol + 1
    #go to room on the left
    elif rX < 0 and currentCol - 1 > -1:
        currentCol = currentCol - 1
    #go to room below
    elif rY > 750 and currentRow + 1 < 4:
        currentRow = currentRow + 1
    #go to room above
    elif rY < 0 and currentRow - 1 > -1:
        currentRow = currentRow - 1

    return currentRow, currentCol


while running:
    # pause the program for 5 miliseconds so that it doesn't run to fast
    pygame.time.wait(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # if the up, down, left, or right keys are pressed
    # we want to change the position accordingly
    if keys[pygame.K_LEFT]:
        rX = rX - speed
    elif keys[pygame.K_RIGHT]:
        rX = rX + speed
    elif keys[pygame.K_UP]:
        rY = rY - speed
    elif keys[pygame.K_DOWN]:
        rY = rY + speed

    #main.py
    #keep track of the old row and column values
    #(this will help us if we need to flip the robot
    prevRow, prevCol = rRow, rCol

    #get the new row and column values
    rRow, rCol = changeRoom(rRow, rCol)

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
    # update the screen
    pygame.display.update()



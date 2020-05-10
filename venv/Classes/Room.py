import random
import pygame

class Room:
    def __init__(self):
        self.moonHeight = random.randint(200, 600)
        self.moonWidth = random.randint(200, 600)
        self.r, self.g, self.b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        moonFileLocation = 'venv/Images/moon.png'
        self.moon = pygame.image.load(moonFileLocation)

    # pass in the screen, image of the robot, and the coordinates that the robot should be at
    def fillRoom(self, screen, image, newX, newY):
        # add the background and moon for this room
        screen.fill((self.r, self.g, self.b))
        #ERROR in last post, width and height should be swapped
        screen.blit(self.moon, (self.moonWidth, self.moonHeight))

        # add the robot
        screen.blit(image, (newX, newY))
        # update everything
        pygame.display.update()

    # tells us which room to go to next (if that room exist)
    def changeRoom(self, currentRow, currentCol, rX, rY):
        # go to room on the right
        if rX > 750 and currentCol + 1 < 4:
            currentCol = currentCol + 1
        # go to room on the left
        elif rX < 0 and currentCol - 1 > -1:
            currentCol = currentCol - 1
        # go to room below
        elif rY >= 750 and currentRow + 1 < 4:
            currentRow = currentRow + 1
        # go to room above
        elif rY <= 0 and currentRow - 1 > -1:
            currentRow = currentRow - 1

        return currentRow, currentCol









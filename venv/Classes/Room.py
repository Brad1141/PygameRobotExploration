import random
import pygame
class Room:
    def __init__(self):
        self.height = random.randint(200, 700)
        self.width = random.randint(200, 700)
        self.r, self.g, self.b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        moonFileLocation = 'venv/Classes/moon.png'
        self.moon = pygame.image.load(moonFileLocation)

    # pass in the screen, image of the robot, and the coordinates that the robot should be at
    def fillRoom(self, screen, image, newX, newY):
        # add the background and moon for this room
        screen.fill((self.r, self.g, self.b))
        screen.blit(self.moon, (self.height, self.width))

        # add the robot
        screen.blit(image, (newX, newY))
        # update everything
        pygame.display.update()



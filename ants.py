import random
import time
import pygame

pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)


class Ant:
    def __init__(self):
        self.cords = (200, 200)


ants = Ant()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(ants.cords[0], ants.cords[1], 20, 20))
    pygame.display.flip()

    time.sleep(0.2)

pygame.quit()

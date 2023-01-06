import random
import time
from collections import deque
import pygame

pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
player_cor = [200, 200]
apple_cor = [500, 500]
direction = [0, 20]
snakes_parts_cords = deque([[100, 100]])
goal = [500, 500]


def collide(obj1, obj2):
    if obj1[0] >= obj2[0] >= obj1[0] and obj1[1] >= obj2[1] >= obj1[1]:
        return True

def links_rechts():
    global player_cor, goal, direction
    if player_cor[0] < goal[0]:
        direction = [20, 0]
    if player_cor[0] > goal[0]:
        direction = [-20, 0]

def oben_unten():
    global player_cor, goal, direction
    if player_cor[1] < goal[1]:
        direction = [0, 20]
    if player_cor[1] > goal[1]:
        direction = [0, -20]



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snakes_parts_cords.append([player_cor[0] - direction[0], player_cor[1] - direction[1]])
            '''
            elif event.key == pygame.K_LEFT and direction != [20, 0]:
                direction = [-20, 0]
            elif event.key == pygame.K_UP and direction != [0, 20]:
                direction = [0, -20]
            elif event.key == pygame.K_DOWN and direction != [0, -20]:
                direction = [0, 20]'''
    screen.fill((0, 0, 0))

    player_cor[0] += direction[0]
    player_cor[1] += direction[1]

    # snakes parts update
    if len(snakes_parts_cords) > 1:
        snakes_parts_cords.rotate(1)
    snakes_parts_cords[0][0] = player_cor[0]
    snakes_parts_cords[0][1] = player_cor[1]

    # collide
    if collide(player_cor, apple_cor):
        apple_cor[0] = random.randint(0, width / 20) * 20
        apple_cor[1] = random.randint(0, height / 20) * 20
        snakes_parts_cords.append([player_cor[0] - direction[0], player_cor[1] - direction[1]])
    elif player_cor[0] < 0 or player_cor[0] > width or player_cor[1] < 0 or player_cor[1] > height:
        break
    for i in range(len(snakes_parts_cords)):
        if i != 0:
            if collide(player_cor, snakes_parts_cords[i]):
                break
    if collide(player_cor, goal):
        goal[0] = apple_cor[0]
        goal[1] = apple_cor[1]

    # Draw
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_cor[0], player_cor[1], 20, 20))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple_cor[0], apple_cor[1], 20, 20))
    for i in range(len(snakes_parts_cords)):
        if i != 0:
            pygame.draw.rect(screen, (0, 255, 0),
                             pygame.Rect(snakes_parts_cords[i][0], snakes_parts_cords[i][1], 20, 20))
    pygame.display.flip()

    # randomwalk
    a = random.randint(0, 1)

    if a == 0 and player_cor[0] != goal[0]:
        links_rechts()
    elif a == 1 and player_cor[1] == goal[1]:
        links_rechts()
    else:
        oben_unten()


    time.sleep(0.02)

pygame.quit()




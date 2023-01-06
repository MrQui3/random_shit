import pygame
import time

pygame.init()
height = 10
width = 10
x_factor = 60
y_factor = 60
screen = pygame.display.set_mode([width * x_factor, height * y_factor], pygame.RESIZABLE)
start_cords = (0, 8)
end_cords = (8, 0)
current = start_cords

not_closed = {}  # the set of nodes to be evaluated
closed = [start_cords]  # the set of nodes already evaluated
walls = [(2, 4), (3, 4), (4, 4), (5, 4), (5, 5), (5, 6)]


# G cost = distance from starting node
# H cost = distance from end node
# F cost = G cost + H cost
def calculate_G_cost(point):
    global start_cords
    return abs(point[0] - start_cords[0]) + abs(point[1] - start_cords[1])


def calculate_H_cost(point):
    global end_cords
    return abs(point[0] - end_cords[0]) + abs(point[1] - end_cords[1])


def add_neighbors_to_not_closed(point):
    global not_closed
    if (point[1]) != 0 and (point[0], point[1] - 1) not in closed and (point[0], point[1] - 1) not in not_closed and (point[0], point[1] - 1) not in walls:
        not_closed[(point[0], point[1] - 1)] = calculate_G_cost((point[0], point[1] - 1)) + calculate_H_cost(
            (point[0], point[1] - 1))
    if (point[0]) != width and (point[0] + 1, point[1]) not in closed and (point[0] + 1, point[1]) not in not_closed and (point[0] + 1, point[1]) not in walls:
        not_closed[(point[0] + 1, point[1])] = calculate_G_cost((point[0] + 1, point[1])) + calculate_H_cost(
            (point[0] + 1, point[1]))
    if (point[1]) != height and (point[0], point[1] + 1) not in closed and (point[0], point[1] + 1) not in not_closed and (point[0], point[1] + 1) not in walls:
        not_closed[(point[0], point[1] + 1)] = calculate_G_cost((point[0], point[1] + 1)) + calculate_H_cost(
            (point[0], point[1] + 1))
    if (point[0]) != 0 and (point[0] - 1, point[1]) not in closed and (point[0] - 1, point[1]) not in not_closed and (point[0] - 1, point[1]) not in walls:
        not_closed[(point[0] - 1, point[1])] = calculate_G_cost((point[0] - 1, point[1])) + calculate_H_cost(
            (point[0] - 1, point[1]))


add_neighbors_to_not_closed(current)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    current = min(not_closed, key=not_closed.get)
    not_closed.pop(current)
    closed.append(current)
    add_neighbors_to_not_closed(current)
    if current == end_cords:
        time.sleep(100)
        running = False

    # Draw closed
    for i in closed:
        pygame.draw.rect(screen, (255, 0, 0), ((i[0] * x_factor, i[1] * y_factor), (60, 60)))

    # Draw not_closed
    for i in not_closed:
        pygame.draw.rect(screen, (0, 255, 0), ((i[0] * x_factor, i[1] * y_factor), (60, 60)))

    # Draw Walls
    for i in walls:
        pygame.draw.rect(screen, (0, 0, 0), ((i[0] * x_factor, i[1] * y_factor), (60, 60)))

    # Draw start and end point
    pygame.draw.rect(screen, (0, 0, 255), ((start_cords[0] * x_factor, start_cords[1] * y_factor), (60, 60)))
    pygame.draw.rect(screen, (0, 0, 255), ((end_cords[0] * x_factor, end_cords[1] * y_factor), (60, 60)))

    # Draw rows and columns
    for i in range(width):
        pygame.draw.line(screen, (10, 10, 10), ((i + 1) * x_factor, 0), ((i + 1) * x_factor, height * y_factor), 2)
    for i in range(height):
        pygame.draw.line(screen, (10, 10, 10), (0, (i + 1) * y_factor), (width * x_factor, (i + 1) * y_factor), 2)

    pygame.display.flip()
    time.sleep(1)



pygame.quit()

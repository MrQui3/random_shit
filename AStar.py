import pygame
import time

pygame.init()
height = 20
width = 20
x_factor = 30
y_factor = 30
screen = pygame.display.set_mode([width * x_factor, height * y_factor], pygame.RESIZABLE)
start_cords = (10, 18)
end_cords = (8, 4)
current = start_cords

f_cost_not_closed = {}  # the set of nodes to be evaluated. 2d dictionary first number g cost, second f cost
g_cost_not_closed = {}  # the set of nodes to be evaluated. 2d dictionary first number g cost, second f cost
closed = [start_cords]  # the set of nodes already evaluated
walls = [(3, 6), (4, 6), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10)]


# G cost = distance from starting node
# H cost = distance from end node
# F cost = G cost + H cost
def calculate_G_cost(point):
    global current, g_cost_not_closed
    if current == start_cords:
        if ((point[0] == current[0] and point[1] - 1 == current[1]) or
                (point[0] == current[0] and point[1] + 1 == current[1]) or
                (point[1] == current[1] and point[0] - 1 == current[0]) or
                (point[1] == current[1] and point[0] + 1 == current[0])):
            return 10
        else:
            return 14

    else:
        if ((point[0] == current[0] and point[1] - 1 == current[1]) or
                (point[0] == current[0] and point[1] + 1 == current[1]) or
                (point[1] == current[1] and point[0] - 1 == current[0]) or
                (point[1] == current[1] and point[0] + 1 == current[0])):
            return g_cost_not_closed[current] + 10
        else:
            return g_cost_not_closed[current] + 14


def calculate_H_cost(point):
    global end_cords
    dx = abs(point[0] - end_cords[0])
    dy = abs(point[1] - end_cords[1])
    return 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)


def add_neighbors_to_not_closed(point):
    global f_cost_not_closed
    x = point[0]
    y = point[1]
    pn = [(x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1),
          (x + 1, y - 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    for t in pn:
        if (t[0] > -1 or t[1] > -1 or t[0] <= width or t[1] <= height) and t not in closed and t not in f_cost_not_closed and t not in walls:
            f_cost_not_closed[t] = calculate_G_cost(t) + calculate_H_cost(t)
            g_cost_not_closed[t] = calculate_G_cost(t)


add_neighbors_to_not_closed(current)
running = True
while running:

    current = min(f_cost_not_closed, key=f_cost_not_closed.get)
    add_neighbors_to_not_closed(current)
    f_cost_not_closed.pop(current)
    g_cost_not_closed.pop(current)
    closed.append(current)
    if current == end_cords:
        time.sleep(100)
        running = False

    # Pygame stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    # Draw closed
    for i in closed:
        pygame.draw.rect(screen, (255, 0, 0), ((i[0] * x_factor, i[1] * y_factor), (x_factor, y_factor)))

    # Draw not_closed
    for i in f_cost_not_closed:
        pygame.draw.rect(screen, (0, 255, 0), ((i[0] * x_factor, i[1] * y_factor), (x_factor, y_factor)))

    # Draw Walls
    for i in walls:
        pygame.draw.rect(screen, (0, 0, 0), ((i[0] * x_factor, i[1] * y_factor), (x_factor, y_factor)))

    # Draw start and end point
    pygame.draw.rect(screen, (0, 0, 255), ((start_cords[0] * x_factor, start_cords[1] * y_factor), (x_factor, y_factor)))
    pygame.draw.rect(screen, (0, 0, 255), ((end_cords[0] * x_factor, end_cords[1] * y_factor), (x_factor, y_factor)))

    # Draw rows and columns
    for i in range(width):
        pygame.draw.line(screen, (10, 10, 10), ((i + 1) * x_factor, 0), ((i + 1) * x_factor, height * y_factor), 2)
    for i in range(height):
        pygame.draw.line(screen, (10, 10, 10), (0, (i + 1) * y_factor), (width * x_factor, (i + 1) * y_factor), 2)

    pygame.display.flip()
    time.sleep(1)

pygame.quit()

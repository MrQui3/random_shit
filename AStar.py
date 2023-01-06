import pygame

pygame.init()
height = 10
width = 10
x_factor = 60
y_factor = 60
screen = pygame.display.set_mode([width * x_factor, height * y_factor], pygame.RESIZABLE)
start_cords = (4, 8)
end_cords = (3, 4)


# not_closed = []  # the set of nodes to be evaluated
# closed = [start_cords]  # the set of nodes already evaluated

# G cost = distance from starting node
# H cost = distance from end node
def calculate_G_cost(point):
    global start_cords
    return abs(point[0] - start_cords[0]) + abs(point[1] - start_cords[1])

def calculate_H_cost(point):
    global end_cords
    return abs(point[0] - end_cords[0]) + abs(point[1] - end_cords[1])


running = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    # Draw start and end point
    pygame.draw.rect(screen, (0, 0, 255), ((start_cords[0] * x_factor, start_cords[1] * y_factor), (60, 60)))
    pygame.draw.rect(screen, (0, 0, 255), ((end_cords[0] * x_factor, end_cords[1] * y_factor), (60, 60)))

    # Draw rows and columns
    for i in range(width):
        pygame.draw.line(screen, (0, 0, 0), ((i + 1) * x_factor, 0), ((i + 1) * x_factor, height * y_factor), 2)
    for i in range(height):
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * y_factor), (width * x_factor, (i + 1) * y_factor), 2)

    pygame.display.flip()

pygame.quit()

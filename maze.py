import random
import time
import pygame

pygame.init()

markedVisited = []
stack = []
at_the_moment = (0, 0)

stack_solving = []
markedVisited_solving = []
goal = 0
at_the_moment_solving = (0, 0)

width = 20
height = 20


class generate:

    def get_neighbors(self, x, y):
        neighbors = []
        if x > 0 and (x - 1, y) not in markedVisited:
            neighbors.append((x - 1, y))
        if x < width - 1 and (x + 1, y) not in markedVisited:
            neighbors.append((x + 1, y))
        if y > 0 and (x, y - 1) not in markedVisited:
            neighbors.append((x, y - 1))
        if y < height - 1 and (x, y + 1) not in markedVisited:
            neighbors.append((x, y + 1))

        return neighbors

    def jump(self):
        if len(stack) == 0:
            return
        neighbors = self.get_neighbors(stack[-1][0], stack[-1][1])
        if len(neighbors) <= 0:
            stack.pop(-1)
            self.jump()

    def generate_maze(self, at_the_moment):
        global goal
        try:
            markedVisited.append(at_the_moment)
            neighbors = self.get_neighbors(at_the_moment[0], at_the_moment[1])
            if len(neighbors) == 0:
                self.jump()
                at_the_moment = stack[-1]
                at_the_moment = (at_the_moment[0], at_the_moment[1], 0)
                markedVisited.append(at_the_moment)
                neighbors = self.get_neighbors(at_the_moment[0], at_the_moment[1])

            at_the_moment = neighbors[random.randint(0, len(neighbors) - 1)]
            if len(neighbors) > 1:
                stack.append(at_the_moment)
            return at_the_moment
        except:
            goal = (random.randint(round(width / 2), width - 1), random.randint(round(height / 2), height - 1))
            return 0, 0, 0, 0


class solving:

    def number_of_neighbors(self, x, y):
        if (x, y, 0) in markedVisited:
            return 2

        else:
            return 1

    def get_neighbors(self, x, y):
        neighbors = []
        positions = []
        a = markedVisited.index((x, y))

        if markedVisited[a] == markedVisited[-1]:
            return neighbors

        if len(markedVisited[a + 1]) != 3 and markedVisited[a + 1] not in markedVisited_solving:
            neighbors.append(markedVisited[a + 1])

        for i in range(len(markedVisited)):
            if (x, y, 0) == markedVisited[i] and markedVisited[i + 1] not in markedVisited_solving:
                neighbors.append(markedVisited[i + 1])
            if len(positions) == 2:
                break

        return neighbors

    def solve(self, at_the_moment):
        a = self.get_neighbors(at_the_moment[0], at_the_moment[1])

        if len(a) == 0:
            return 1, 1, 1, 1
        return a[random.randint(0, len(a) - 1)]


def start():
    global at_the_moment, at_the_moment_solving
    global markedVisited, markedVisited_solving
    global stack, stack_solving
    global goal

    markedVisited = []
    stack = []
    at_the_moment = (0, 0)

    stack_solving = []
    markedVisited_solving = []
    goal = 0
    at_the_moment_solving = (0, 0)

    markedVisited.append(at_the_moment)
    stack.append(at_the_moment)
    neighbors = generate().get_neighbors(at_the_moment[0], at_the_moment[1])

    at_the_moment = neighbors[random.randint(0, len(neighbors) - 1)]
    if len(neighbors) > 1:
        stack.append(at_the_moment)

    markedVisited_solving.append(at_the_moment_solving)
    stack_solving.append(at_the_moment_solving)


screen = pygame.display.set_mode([1000, 1000], pygame.RESIZABLE)

running = True
start()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    # Generating
    if at_the_moment != (0, 0, 0, 0):
        at_the_moment = generate().generate_maze(at_the_moment)



    # Solving

    else:
        if at_the_moment_solving != goal:
            at_the_moment_solving = solving().solve(stack_solving[-1])
            if at_the_moment_solving != (1, 1, 1, 1):
                stack_solving.append(at_the_moment_solving)
                markedVisited_solving.append(at_the_moment_solving)
            else:
                stack_solving.pop(-1)

        else:
            time.sleep(1)
            start()

    # Draw
    color = (10, 10, 30)
    # Changing surface color
    screen.fill(color)

    for i in range(len(markedVisited) - 1):
        if len(markedVisited[i + 1]) != 3:
            pygame.draw.line(screen, (0, 0, 255), [markedVisited[i][0] * 10 + 5, markedVisited[i][1] * 10 + 5],
                             [markedVisited[i + 1][0] * 10 + 5, markedVisited[i + 1][1] * 10 + 5], width=1)

    for i in range(len(stack_solving) - 1):
        pygame.draw.line(screen, (255, 0, 0), [stack_solving[i][0] * 10 + 5, stack_solving[i][1] * 10 + 5],
                         [stack_solving[i + 1][0] * 10 + 5, stack_solving[i + 1][1] * 10 + 5], width=1)

    pygame.draw.circle(screen, (255, 0, 0), [markedVisited[0][0] * 10 + 5, markedVisited[0][1] * 10 + 5], 2)

    if at_the_moment == (0, 0, 0, 0):
        pygame.draw.circle(screen, (0, 255, 0), [goal[0] * 10 + 5, goal[1] * 10 + 5], 2)

    pygame.display.flip()

pygame.quit()

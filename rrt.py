import pygame, random, math
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

showScreen = True
SIZE = (800, 800)

START = [400, 400]
GOAL = [700, 700]

nodes = []
connections = []

# CLASSES
class Connection:
    def __init__(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2

    def draw(self, screen):
        pygame.draw.line(screen, (0, 255, 255), [self.parent1.x, self.parent1.y], [
                         self.parent2.x, self.parent2.y], 2)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, [self.x, self.y], 5)


# FUNCTIONS
def createConnection():
    global nodes, connections

    nNode = Node(random.randrange(0, SIZE[0]), random.randrange(0, SIZE[1]))
    closestNode = nodes[0]
    minDistance = distance(closestNode.x, closestNode.y, nNode.x, nNode.y)
    
    for node in nodes[1:]:
        dist = distance(node.x, node.y, nNode.x, nNode.y)

        if dist < minDistance:
            closestNode = node
            minDistance = dist

    connections.append(Connection(closestNode, nNode))
    nodes.append(nNode)

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

#### SETUP

nodes.append(Node(START[0], START[1]))
for x in range(1000):
    createConnection()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
while showScreen:
    screen.fill(BLACK)

    # draw start, goal
    pygame.draw.circle(screen, (0, 255, 0), START, 8)
    pygame.draw.circle(screen, (255, 0, 255), GOAL, 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showScreen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                createConnection()

    # draw connections and nodes
    for connection in connections:
        connection.draw(screen)

    # for node in nodes[1:]:
    #     node.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

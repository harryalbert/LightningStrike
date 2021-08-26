import pygame
import random
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SIZE = (800, 800)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

showScreen = True

splitWidthRange = [40, 60]  # part of line from which line can be split
splitHeightRange = [-60, 60]  # distance from line that new line is cast
lineLengthRange = [80, 120]  # bscly size of angle to morph line at
newLineLengthRange = [20, 50] # length as percent of parent line length

splitChance = 0.8 #chance of a line to morph
newLineChance = 0.8 # chance of a new line coming off of an old line

class Strike:
    def __init__(self, intensity, x1, y1, x2, y2):
        self.intensity = intensity
        self.p1 = [x1, y1]
        self.p2 = [x2, y2]

        baseColor = 255 * intensity
        self.color = (baseColor, baseColor, baseColor)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.p1, self.p2)

def splitStrikes(strikes):
    newStrikes = []

    for strike in strikes:
        if random.random() > splitChance:
            newStrikes.append(strike)
            continue

        midPercent = random.randrange(
            splitWidthRange[0], splitWidthRange[1]) / 100.0

        # get slope of line
        slopeX = strike.p2[0] - strike.p1[0]
        slopeY = strike.p2[1] - strike.p1[1]
        fullLength = abs(slopeX) + abs(slopeY)

        # point of origin for new line
        midX = strike.p1[0] + slopeX * midPercent
        midY = strike.p1[1] + slopeY * midPercent

        # slope of perpendicular line
        invRise = -1 * slopeX / fullLength
        invRun = slopeY / fullLength

        newLength = random.randrange(lineLengthRange[0], lineLengthRange[1])
        newLength *= (fullLength / orgLength)
        if random.random() > 0.5:
            newLength *= -1

        npX = midX + invRun * newLength
        npY = midY + invRise * newLength

        newStrikes.append(Strike(strike.intensity, strike.p1[0], strike.p1[1], npX, npY))
        newStrikes.append(Strike(strike.intensity, npX, npY, strike.p2[0], strike.p2[1]))

        if random.random() < newLineChance:
            newLength = fullLength * (random.randrange(newLineLengthRange[0], newLineLengthRange[1]) / 100.0)
            npX2 = npX + (slopeX / fullLength) * newLength
            npY2 = npY + (slopeY / fullLength) * newLength
            newStrikes.append(Strike(strike.intensity * 0.7, npX, npY, npX2, npY2))

    return newStrikes


strikes = [Strike(1, 100, 100, 700, 700)]
orgLength = abs(strikes[0].p2[0] - strikes[0].p1[0]) + abs(strikes[0].p2[1] - strikes[0].p1[1])
while showScreen:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showScreen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                strikes = splitStrikes(strikes)

    for strike in strikes:
        strike.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

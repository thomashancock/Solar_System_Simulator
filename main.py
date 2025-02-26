import sys
import random
import math

# Setup logging
import logging

if __debug__:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

# Setup pygame
import pygame
import pygame.locals
pygame.init()
pygame.font.init()

fontComicSans = pygame.font.SysFont('Comic Sans MS', 30)

# Define colors
WHITE = (255,255,255)
GREY = (128,128,128)
BLACK = (0,0,0)
RED = (255,0,0)
ORANGE = (255, 165, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SADDLEBROWN = (139, 69, 19)
ROSYBROWN = (188, 143, 143)
CYAN = (0, 255, 255)

convertAU2km = 149.6E6

surfaceWidth = 720
surfaceHeight = 720

# Colour, Speed (mk/s), Radius (AU)
planetDict = {
    'mercury': [SADDLEBROWN, 47.87, 0.39*convertAU2km],
    'venus': [ROSYBROWN, 35.02, 0.723*convertAU2km],
    'earth': [GREEN, 29.78, 1.0*convertAU2km],
    'mars': [RED, 24.077, 1.524*convertAU2km],
    'jupiter': [ORANGE, 13.07, 5.203*convertAU2km],
    'saturn': [WHITE, 9.69, 9.539*convertAU2km],
    'uranus': [CYAN, 6.81, 19.18*convertAU2km],
    'neptune': [BLUE, 5.43, 30.06*convertAU2km]
}


def getMaxOrbitRadius(planetDict):
    maxOrbitRad = 0.0
    for _, val in planetDict.items():
        maxOrbitRad = val[2] if val[2] > maxOrbitRad else maxOrbitRad
    assert(maxOrbitRad > 0.0)
    return maxOrbitRad

maxOrbitRad = getMaxOrbitRadius(planetDict)


def coorToPixel(xCoor, yCoor):
    scaleFactor = surfaceHeight/(maxOrbitRad*2.2)
    offset = surfaceHeight/2.0
    xPos = int((xCoor * scaleFactor) + offset)
    if xPos < 0:
        xPos = 0
    yPos = int((yCoor * scaleFactor) + offset)
    if yPos < 0:
        yPos = 0
    return xPos, yPos


class OrbitalBody:
    """
    Body
    """

    def __init__(self, name, color, initPos, initVel):
        """
        Body Constructor
        """

        self.name = name

        # Constants
        self.G = 6.674 * 1E-20 # km^3 /kg /s^2
        self.mass = 1.989 * 1E30 # kg # Solar Mass

        # Draw options
        self.radius = 5
        self.pos = [x for x in initPos]
        self.vel = [x for x in initVel]
        self.acc = [0.0, 0.0]
        self.color = color

        logging.info("Created body {} with colour {}".format(name, color))

    def getName():
        return self.name

    def draw(self, surface):
        xPos, yPos = coorToPixel(self.pos[0], self.pos[1])
        pygame.draw.circle(surface, self.color, [xPos, yPos], self.radius, 0)

    def update(self, dT):
        # Update position using Euler Method
        # Acc: ax_{i} = -G * m * x_{i} / (r^3)
        # Vel: vx_{i+1} = vx_{i} + ax_{i}*dt
        # Pos: x_{i+1} = x_{i} + vx_{i+1}*dt

        orbitalRadius = math.sqrt(self.pos[0]**2 + self.pos[1]**2)
        for coor in range(2):
            self.acc[coor] = -1.0 * self.G * self.mass * self.pos[coor] / (orbitalRadius**3)
            self.vel[coor] = self.vel[coor] + self.acc[coor] * dT
            self.pos[coor] = self.pos[coor] + self.vel[coor] * dT


class World:
    '''
    World class
    Manages and runs the simulation
    '''
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))

        self.clock = pygame.time.Clock()
        self.dT = 24*(60.0**2) # 1 frame = 1 day
        self.elapsedTime = 0.0

        self.entities = []


    def addEntity(self, entity):
        '''
        Add an entity for the world to track
        '''
        self.entities.append(entity)


    def run(self):
        '''
        Runs the simulation
        '''
        while True:
            for event in pygame.event.get():
                # Detect Quit Action
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update objects
            self.surface.fill(BLACK)

            for entity in self.entities:
                entity.update(self.dT)
                entity.draw(self.surface)

            # Print elapsed time
            self.elapsedTime += self.dT
            textsurface = fontComicSans.render('{:0.2f} earth years'.format(self.elapsedTime/(self.dT*365.25)), False, WHITE)
            self.surface.blit(textsurface,(0,0))

            # Update display
            pygame.display.flip()

            pygame.display.set_caption("Simulation FPS: {0}".format(int(self.clock.get_fps())))

            self.clock.tick(60)


def main():
    '''
    Main function
    '''

    # Define world object
    world = World(surfaceWidth, surfaceHeight)

    # Popuate world with entities
    for key, val in planetDict.items():
        planet = OrbitalBody(key, val[0], [0.0, val[2]], [val[1], 0.0])
        world.addEntity(planet)

    # Run world
    world.run()


if __name__ == "__main__":
    main();

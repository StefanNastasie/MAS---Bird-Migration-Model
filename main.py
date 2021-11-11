import pygame, math, sys
from random import randint


pygame.init()

#set values for screen size

X = 900
Y = 600

#set color values for easier access

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)


#class i found on the internet, might help us change background

class Gradient():
    def __init__(self, palette, maximum):
        self.COLORS = palette
        self.N = len(self.COLORS)
        self.SECTION = maximum // (self.N - 1)

    def gradient(self, x):
        """
        Returns a smooth color profile with only a single input value.
        The color scheme is determined by the list 'self.COLORS'
        """
        i = x // self.SECTION
        fraction = (x % self.SECTION) / self.SECTION
        c1 = self.COLORS[i % self.N]
        c2 = self.COLORS[(i+1) % self.N]
        col = [0, 0, 0]
        for k in range(3):
            col[k] = (c2[k] - c1[k]) * fraction + c1[k]
        return col

#class for the parameter sliders

class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.name = name
        self.val = int(val)  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 550 # fixed y-location at the bottom of the screen
        self.surf = pygame.surface.Surface((100, 50)) # dimensions for the slider box
        self.hit = False  # attribute that registers mouse interaction

        self.txt_surf = font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, CYAN, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, CYAN, (10, 10), 4, 0)


    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = int((pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini)
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi

#Agent class

agent_image = pygame.image.load("arrow-pointer.png")


class Agent():
    def __init__(self, init_pos, number, speed):
        self.n = number
        self.originX, self.originY = init_pos
        self.posX, self.posY = init_pos
        self.speed = speed


    def find_partner(self, random_agent):
        self.partner = random_agent


    def moveTowards(self, entity):
        if abs(self.posX - entity.posX) > 5:
            self.posX += (entity.posX-self.posX)/50
        if abs(self.posY - entity.posY) > 5:
            self.posY += (entity.posY-self.posY)/20

    def death(self):
        pass
    #to be completed

    def reproduction(self):
        pass
    #to be completed

    #think of other methods to add?


class Temperature():

    def __init__(self, region, hemisphere, min_value, max_value, location):
        self.region = region #name of the temp region
        self.hemisphere = hemisphere #hemisphere bool
        self.min_value = min_value #min value that the temp can reach
        self.max_value = max_value #max value that the temp can reach
        self.location = location #location border on the screen

    #add methods





#some game properties

screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
pygame.display.set_caption("Bird Migration Model")
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)


#Game Loop

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    if running:
        screen.fill(BLACK)




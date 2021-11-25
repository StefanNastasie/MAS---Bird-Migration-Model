import pygame, math, sys, datetime
from random import randint
from pygame.locals import RLEACCEL, BLEND_RGBA_MULT
import matplotlib.pyplot as plt
import numpy as np

pygame.init()
pygame.font.init()

# set values for screen size

X = 900
Y = 600
screen = pygame.display.set_mode((X, Y))

# set color values for easier access

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
BBYBLUE = (202, 228, 241)


# class for the parameter sliders

class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.name = name
        self.val = int(val)  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = 780  # fixed x-location on the left of the screen
        self.ypos = pos  # y-position
        self.surf = pygame.surface.Surface((100, 50))  # dimensions for the slider box
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
        pos = (10 + int((self.val - self.mini) / (self.maxi - self.mini) * 80), 33)
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


# Agent class

bird = pygame.image.load("new-pointer.png").convert_alpha()

agents = pygame.sprite.Group()


# add all agents to a sprite group for easy iteration

class Agent(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self, agents)
        self.speed = [1, 1]
        self.time_alive = 0
        self.image = bird
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = init_pos[0]
        self.rect.y = init_pos[1]
        self.image.set_colorkey(BBYBLUE, RLEACCEL)
        self.cooldown = 0
        self.goal = [self.rect.x, self.rect.y]
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill(BLACK)
        self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.lives = 20
        self.region = ''

    def reproduction(self):
        if pygame.sprite.spritecollide(self, agents, False):
            if self.cooldown <= 0:
                if randint(0, 101) < Reproduction_rate.val:
                    Agent([self.rect.x, self.rect.y])
                    self.cooldown = 360
            else:
                self.cooldown -= 1

    def get_region(self):
        if self.rect.y > 480:
            self.region = South
        elif self.rect.y > 360:
            self.region = Temperate_south
        elif self.rect.y > 300:
            self.region = Tropical_south
        elif self.rect.y > 240:
            self.region = Tropical_north
        elif self.rect.y > 120:
            self.region = Temperate_north
        else:
            self.region = North

    def move(self):
        if abs(self.rect.x - self.goal[0]) <= 5 and abs(self.rect.y - self.goal[1]) <= 5:
            self.find_goal()
        if self.temperature < -5 or self.temperature > 40:
            if self.lives <= 20:
                self.find_goal()
        if (self.rect.x - self.goal[0]) > 5:
            self.rect.x -= self.speed[0]
        if (self.rect.x - self.goal[0]) < -5:
            self.rect.x += self.speed[0]
        if (self.rect.y - self.goal[1]) > 5:
            self.rect.y -= self.speed[1]
        if (self.rect.y - self.goal[1]) < -5:
            self.rect.y += self.speed[1]

    def update(self):
        self.get_region()
        self.temperature = self.region.displayed_temp
        self.check_death()
        self.move()
        self.time_alive += 1

    def check_death(self):
        if self.time_alive > Lifespan.val:
            self.kill()
        if self.temperature < -5 or self.temperature > 40:
            self.lives -= 1
        if self.temperature > 15 and self.temperature < 25 and self.lives < 15:
            self.lives += 1
        if self.lives <= 0:
            self.kill()

    def find_goal(self):
        x_goal = randint(100, 740)
        if self.temperature < -5:
            if self.rect.y < 300:
                y_goal = randint(120, 300)
            else:
                y_goal = randint(300, 480)
        elif self.temperature > 40:
            if self.rect.y < 300:
                y_goal = randint(120, 240)
            else:
                y_goal = randint(360, 480)
        else:
            if self.rect.y < 300:
                y_goal = randint(300, 600)
            else:
                y_goal = randint(0, 300)
        self.goal = [x_goal, y_goal]


class Region():

    def __init__(self, name, yleft, yright):
        self.name = name  # name of the temp region
        self.yleft = yleft
        self.uleft = (0, yleft)
        self.dright = (749, yright)  # coordinates for the region
        self.uright = (749, yleft)
        self.dleft = (0, yright)
        self.font = pygame.font.SysFont("Magenta", 15)  # font settings
        self.color = MAGENTA

    def temperature(self, current_date, climate_factor):
        if self.name == "North":
            month = current_date.month
            temp_values = seasons_north.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)
            # formula for determining the temperature influenced by the climate factor (same for every temp_region)

        if self.name == "Temperate_north":
            month = current_date.month
            temp_values = seasons_temperate_north.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)

        if self.name == "Tropical_north":
            month = current_date.month
            temp_values = seasons_tropical_north.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)

        if self.name == "Tropical_south":
            month = current_date.month
            temp_values = seasons_tropical_south.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)

        if self.name == "Temperate_south":
            month = current_date.month
            temp_values = seasons_temperate_south.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)

        if self.name == "South":
            month = current_date.month
            temp_values = seasons_south.values()
            temp_values_list = list(temp_values)
            temp_range = temp_values_list[month - 1]
            return randint(temp_range[0] - climate_factor, temp_range[1] + climate_factor)

    def draw_display(self):  # method for displaying the temperature and region name

        region_info = self.font.render(str(self.name), 1, self.color)
        self.displayed_temp = self.temperature(date, Climate_change_factor.val)
        temperature_info = self.font.render('Temperature:{}°C'.format(self.displayed_temp), 1, self.color)
        screen.blit(region_info, (5, self.yleft + 10))
        screen.blit(temperature_info, (5, self.yleft + 20))


class display_info():       # function for displaying slider info and date

    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.font = pygame.font.SysFont("Magenta", 16)
        self.color = MAGENTA

    def draw(self):
        current_pop = len(agents)
        if not run_simulation:
            current_pop = Pop.val
        date_info = self.font.render(str(date), 1, self.color)
        population_info = self.font.render('population:{}'.format(current_pop), 1, self.color)
        reproduction_info = self.font.render('reproduction rate:{}'.format(Reproduction_rate.val), 1, self.color)
        lifespan_info = self.font.render('lifespan:{} days'.format(Lifespan.val), 1, self.color)
        climate_info = self.font.render('climate change factor:{}°C'.format(Climate_change_factor.val), 1, self.color)
        screen.blit(date_info, (self.xpos, self.ypos + 25))
        screen.blit(population_info, (self.xpos, self.ypos))
        screen.blit(reproduction_info, (self.xpos - 25, self.ypos + 500))
        screen.blit(lifespan_info, (self.xpos - 25, self.ypos + 530))
        screen.blit(climate_info, (self.xpos - 25, self.ypos + 560))



start_img = pygame.image.load('play.png').convert_alpha()


class Button():     #class for the start button
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.circle = self.image.get_rect()
        self.circle.topleft = (x, y)
        self.clicked = False

    def draw(self):
        screen.blit(self.image, (self.circle.x, self.circle.y))

    def start_click(self):
        pos = pygame.mouse.get_pos()
        if self.circle.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return True


class Border():     # class for making screen borders
    def __init__(self, xleft, yleft, xright, yright, color):
        self.xleft = xleft
        self.yleft = yleft
        self.xright = xright
        self.yright = yright
        self.color = color

    def draw_dotted(self):
        draw_dashed_line(screen, self.color, (self.xleft, self.yleft), (self.xright, self.yright))

    def draw(self):
        pygame.draw.line(screen, self.color, (self.xleft, self.yleft), (self.xright, self.yright))


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):     # function for drawing dotted lines
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if x1 == x2:
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif y1 == y2:
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a ** 2 + b ** 2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in np.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in np.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)


#functions to make the graphs

def plot_population_graph():
    xaxis = np.array(days_passed)
    yaxis = np.array(population_list)

    plt.plot(xaxis, yaxis)
    plt.title('Population graph by days passed')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_north_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(north_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the northern region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_temperate_north_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(temperate_north_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the temperate_north region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_tropical_north_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(tropical_north_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the tropical_north region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_tropical_south_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(tropical_south_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the tropical_south region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_temperate_south_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(temperate_south_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the temperate_south region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()


def plot_south_density():
    xaxis = np.array(days_passed)
    yaxis = np.array(south_population)

    plt.plot(xaxis, yaxis)
    plt.title('Population density in the southern region')
    plt.ylabel('Population')
    plt.xlabel('Days passed')
    plt.show()

#function that calls all graphs

def graphs():
    plot_population_graph()
    plot_north_density()
    plot_temperate_north_density()
    plot_tropical_north_density()
    plot_tropical_south_density()
    plot_temperate_south_density()
    plot_south_density()


# some game properties

font = pygame.font.SysFont("Verdana", 8)
clock = pygame.time.Clock()
pygame.display.set_caption("Bird Migration Model")
icon = pygame.image.load('bird.png').convert_alpha()
pygame.display.set_icon(icon)
date = datetime.date(2022, 1, 1)
date_change = datetime.timedelta(days=1)
display = display_info(X - 120, 10)
start_button = Button(X - 120, 60, start_img, 0.1)

# region borders

border_1 = Border(100, 480, 760, 480, RED)
border_2 = Border(100, 360, 760, 360, RED)
border_3 = Border(100, 300, 760, 300, RED)
border_4 = Border(100, 240, 760, 240, RED)
border_5 = Border(100, 120, 760, 120, RED)

borders = [border_1, border_2, border_3, border_4, border_5]

# screen borders

sborder_1 = Border(750, 0, 750, 600, BLACK)
sborder_2 = Border(100, 0, 100, 600, BLACK)
sborder_3 = Border(0, 480, 100, 480, BLACK)
sborder_4 = Border(0, 360, 100, 360, BLACK)
sborder_5 = Border(0, 300, 100, 300, BLACK)
sborder_6 = Border(0, 240, 100, 240, BLACK)
sborder_7 = Border(0, 120, 100, 120, BLACK)

sborders = [sborder_1, sborder_2, sborder_3, sborder_4, sborder_5, sborder_6, sborder_7]

# regions

North = Region("North", 0, 120)
Temperate_north = Region("Temperate_north", 121, 240)
Tropical_north = Region("Tropical_north", 241, 300)
Tropical_south = Region("Tropical_south", 301, 360)
Temperate_south = Region("Temperate_south", 361, 480)
South = Region("South", 481, 600)

regions = [North, Temperate_north, Temperate_south, Tropical_north, Tropical_south, South]

# seasons dictionary with month as key and temperatures as min/max values in a tuple

seasons_north = {"January": (-12, -7), "February": (-13, -7), "March": (-11, -6), "April": (-7, 0), "May": (0, 6),
                 "June": (5, 12), "July": (7, 14), "August": (6, 12), "September": (3, 8), "October": (-2, 2),
                 "November": (-7, -3), "December": (-11, -6)}
seasons_temperate_north = {"January": (0, 5), "February": (0, 6), "March": (1, 10), "April": (5, 15), "May": (10, 19),
                           "June": (13, 23), "July": (16, 26), "August": (15, 24), "September": (12, 21),
                           "October": (8, 16), "November": (4, 10), "December": (0, 6)}
seasons_tropical_north = {"January": (19, 30), "February": (21, 32), "March": (23, 33), "April": (24, 35),
                          "May": (26, 36), "June": (26, 36), "July": (25, 35), "August": (25, 34),
                          "September": (25, 34), "October": (25, 34), "November": (22, 32), "December": (20, 30)}
seasons_tropical_south = {"January": (21, 30), "February": (21, 30), "March": (21, 30), "April": (21, 30),
                          "May": (19, 29), "June": (18, 28), "July": (17, 28), "August": (18, 29),
                          "September": (19, 30), "October": (20, 30), "November": (21, 30), "December": (21, 30)}
seasons_temperate_south = {"January": (12, 22), "February": (11, 22), "March": (10, 20), "April": (7, 18),
                           "May": (5, 14), "June": (3, 12), "July": (2, 12), "August": (3, 13), "September": (4, 15),
                           "October": (7, 17), "November": (8, 19), "December": (10, 21)}
seasons_south = {"January": (-2, 3), "February": (-3, 2), "March": (-8, -1), "April": (-12, -5), "May": (-15, -7),
                 "June": (-16, -8), "July": (-16, -8), "August": (-15, -7), "September": (-13, -6),
                 "October": (-11, -4), "November": (-6, 0), "December": (-3, 2)}

# sliders

Pop = Slider("Population", 2, 100, 2, 150)
Speed = Slider("Speed", 25, 50, 10, 220)
Reproduction_rate = Slider("Reproduction rate", 2, 7, 0, 290)
Lifespan = Slider("Lifespan", 20, 360, 20, 360)
Climate_change_factor = Slider("Climate factor", 0, 20, 0, 430)

sliders = [Pop, Speed, Reproduction_rate, Lifespan, Climate_change_factor]

# graph data for population
days_passed = []
population_list = []
days_counter = 0

# graph data for density
north_population = []
temperate_north_population = []
tropical_north_population = []
tropical_south_population = []
temperate_south_population = []
south_population = []

north_population_counter = 0
temperate_north_counter = 0
tropical_north_counter = 0
tropical_south_counter = 0
temperate_south_counter = 0
south_population_counter = 0

# Game Loop
running = True
run_simulation = False

while running:

    screen.fill(BBYBLUE)
    start_button.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            graphs()
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for slider in sliders:
                if slider.button_rect.collidepoint(pos):
                    slider.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for slider in sliders:
                slider.hit = False

    for slider in sliders:
        slider.draw()

    display.draw()
    pos = pygame.mouse.get_pos()

    for border in borders:
        border.draw_dotted()
    for sborder in sborders:
        sborder.draw()

    if not run_simulation:
        for slider in sliders:
            if slider.hit:
                slider.move()

    if start_button.start_click():
        run_simulation = True
        for i in range(Pop.val):
            Agent([randint(100, 750), randint(0, 600)])

    if run_simulation:
        for region in regions:
            region.draw_display()
        for agent in agents:
            agent.update()
            screen.blit(agent.image, agent.rect)
            if agent.alive():
                agents.remove(agent)
                agent.reproduction()
                agents.add(agent)
        date += date_change
        days_counter += 1
        days_passed.append(days_counter)
        for agent in agents:
            if agent.rect.y <= 120:
                north_population_counter += 1
            if 240 >= agent.rect.y > 120:
                temperate_north_counter += 1
            if 300 >= agent.rect.y > 240:
                tropical_north_counter += 1
            if 360 >= agent.rect.y > 300:
                tropical_south_counter += 1
            if 480 >= agent.rect.y > 360:
                temperate_south_counter += 1
            if 600 >= agent.rect.y > 480:
                south_population_counter += 1

        north_population.append(north_population_counter)
        temperate_north_population.append(temperate_north_counter)
        tropical_north_population.append(tropical_north_counter)
        tropical_south_population.append(tropical_south_counter)
        temperate_south_population.append(temperate_south_counter)
        south_population.append(south_population_counter)

        north_population_counter = 0
        temperate_north_counter = 0
        tropical_north_counter = 0
        tropical_south_counter = 0
        temperate_south_counter = 0
        south_population_counter = 0

        current_pop = len(agents)
        population_list.append(current_pop)

        if Speed.hit:
            Speed.move()

    clock.tick(Speed.val)
    pygame.display.flip()

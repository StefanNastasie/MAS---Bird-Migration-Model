import pygame, math, sys, datetime, numpy
from random import randint



pygame.init()
pygame.font.init()

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
BBYBLUE = (202,228,241)

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

agents = pygame.sprite.Group()
#add all agents to a sprite group for easy iteration

class Agent(pygame.sprite.Sprite):
    def __init__(self, init_pos, number, speed, color):
        pygame.sprite.Sprite.__init__(self, agents)
        self.n = number
        self.originX, self.originY = init_pos
        self.posX, self.posY = init_pos
        self.speed = speed
        self.time_alive = 0
        self.image = pygame.image.load("arrow-pointer.png")
        self.image.fill(color)
        self.partner = 0
        self.cooldown = 20

    def find_partner(self):
        if pygame.sprite.spritecollide(self, agents, False):
            if self.cooldown <= 0:
                if random.randint(0, 101) < 2:
                    self.partner = 1
            else:
                self.cooldown -= 1


    def update(self):
        entity = self.goal()
        if abs(self.posX - entity[0]) > 5:
            self.posX += (entity[0]-self.posX)/50
        if abs(self.posY - entity[1]) > 5:
            self.posY += (entity.posY-self.posY)/20
        self.time_alive += 1
        self.check_death()
        self.reproduction()

    def check_death(self):
        if self.time_alive > 180:
            if random.randint(0,101) < 5:
                self.kill()


    def reproduction(self):
        if self.partner != 0:
            Agent([self.posx, self.posy], new_number(agents), self.speed, self.color, 0)
            self.partner = 0
            self.cooldown = 20


    def goal(self):
        if self.summer():
            x_goal = self.posx + random.randint(-5, 6)
            y_goal = self.posy + random.randint(-5, 6)
            goal = [x_goal, y_goal]
            return goal
        if not self.summer():
            pass


    def summer(self):
        #returns true if temperature at current position is over a ceratin value
        pass

def new_number(agents):
    nums = []
    for i in agents:
        nums += i.number
    return (max(nums) + 1)

class Region():

    def __init__(self, name, hemisphere, min_value, max_value, yleft, yright):
        self.name = name #name of the temp region
        self.hemisphere = hemisphere #hemisphere bool
        self.min_value = min_value #min value that the temp can reach
        self.max_value = max_value #max value that the temp can reach
        #location border on the screen
        self.yleft = yleft
        self.uleft = (0,yleft)
        self.dright = (749,yright)
        self.uright = (X,yleft)
        self.dleft = (0,yright)
        self.font = pygame.font.SysFont("White", 15)
        self.color = WHITE

    def temperature(self,current_date):
        return temperature
    #add methods

    def draw_display(self):

        region_info = self.font.render(str(self.name), 1, self.color)
        temperature_info = self.font.render('Temperature:{}°C'.format(self.temperature(date)), 1, self.color)
        screen.blit(region_info, (self.yleft+10, X+20))
        screen.blit(temperature_info, (self.yleft+20, X+20))

class display_info():

    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.font = pygame.font.SysFont("Magenta", 20)
        self.color = MAGENTA

    def draw(self):

        date_info = self.font.render(str(date), 1, self.color)
        population_info = self.font.render('population:{}'.format(population_counter), 1, self.color)
        screen.blit(date_info, (self.xpos, self.ypos+25))
        screen.blit(population_info, (self.xpos, self.ypos))


start_img = pygame.image.load('play.png')

class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.circle = self.image.get_rect()
        self.circle.topleft = (x,y)
        self.clicked = False

    def draw(self):
        screen.blit(self.image,(self.circle.x,self.circle.y))

    def start_click(self):
        pos = pygame.mouse.get_pos()
        if self.circle.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return True

class Border():
    def __init__(self,xleft,yleft,xright,yright,color):
        self.xleft = xleft
        self.yleft = yleft
        self.xright = xright
        self.yright = yright
        self.color = color

    def draw_dotted(self):
        draw_dashed_line(screen,self.color,(self.xleft,self.yleft),(self.xright,self.yright))

    def draw(self):
        pygame.draw.line(screen,self.color,(self.xleft,self.yleft),(self.xright,self.yright))

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
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
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)




#some game properties

screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
pygame.display.set_caption("Bird Migration Model")
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)
population_counter = 10
date = datetime.date(2022,1,1)
date_change = datetime.timedelta(days=1)
display = display_info(X-120, 10)
start_button = Button(X-120, 60,start_img,0.1)
temperature = 10

#region borders

border_1 = Border(100,480,760,480,RED)
border_2 = Border(100,360,760,360,RED)
border_3 = Border(100,300,760,300,RED)
border_4 = Border(100,240,760,240,RED)
border_5 = Border(100,120,760,120,RED)

borders = [border_1,border_2,border_3,border_4,border_5]

#screen borders

sborder_1 = Border(750,0,750,600,BLACK)
sborder_2 = Border(100,0,100,600,BLACK)
sborder_3 = Border(0,480,100,480,BLACK)
sborder_4 = Border(0,360,100,360,BLACK)
sborder_5 = Border(0,300,100,300,BLACK)
sborder_6 = Border(0,240,100,240,BLACK)
sborder_7 = Border(0,120,100,120,BLACK)

sborders = [sborder_1,sborder_2,sborder_3,sborder_4,sborder_5,sborder_6,sborder_7]



#regions
North = Region("North",1,0,30,0,120)
Temperate1 = Region("Temperate",1,0,30,121,240)
Tropical1 = Region("Tropical",1,0,30,241,300)
Tropical2 = Region("Tropical",1,0,30,301,360)
Temperate2 = Region("Temperate",1,0,30,361,480)
South = Region("South",1,0,30,481,600)

regions = [North,Temperate1,Temperate2,Tropical1,Tropical2,South]

#Game Loop
running = True
run_simulation = False

while running:

    screen.fill(BBYBLUE)
    start_button.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit(0)

    display.draw()
    for border in borders:
        border.draw_dotted()
    for sborder in sborders:
        sborder.draw()
    for region in regions:
        region.draw_display()
    clock.tick(5)
    pygame.display.flip()
    if start_button.start_click():
        run_simulation = True

    if run_simulation:
        date += date_change


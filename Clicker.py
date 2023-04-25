import pygame

import sys


def between(begin, pos, end):
    return begin <= pos <= end


class Box:
    def __init__(self, x_coord, y_coord, width, height,
                 text, inactive_color, active_color=None):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.text = text
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self):
        mouse = pygame.mouse.get_pos()
        pygame.font.get_fonts()
        font = pygame.font.SysFont('arial', 24)
        img = font.render(self.text[0], True, BLUE)
        isInside = (between(self.x_coord, mouse[0],
                            self.x_coord + self.width) and
                    between(self.y_coord, mouse[1],
                            self.y_coord + self.height))
        color = ACTIVE_COLOR if isInside else INACTIVE_COLOR
        pygame.draw.rect(sc, color, (self.x_coord, self.y_coord,
                                     self.width, self.height))
        sc.blit(img, (self.x_coord, self.y_coord))
        pygame.display.update()

    def doIfPressed(self):
        pass


class Button(Box):
    def __init__(self, x_coord, y_coord, width, height,
                 text, inactive_color, func, active_color=None):
        Box.__init__(self, x_coord, y_coord, width, height,
                     text, inactive_color, active_color)
        self.func = func

    def doIfPressed(self):
        mouse = pygame.mouse.get_pos()
        if ((between(self.x_coord, mouse[0], self.x_coord + self.width) and
                between(self.y_coord, mouse[1], self.y_coord + self.height) and
                pygame.mouse.get_pressed()[0])):
            self.func()

pygame.font.init()

W = 700  # ширина экрана
H = 300  # высота экрана

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (10, 27, 255)
ACTIVE_COLOR = (100, 20, 140)
INACTIVE_COLOR = (12, 182, 30)

clicksNumber = 0
clicksPerSecond = 1
clicksForSpace = 1
cost = 10

lastTime = pygame.time.get_ticks()
currentTime = lastTime

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

textClick = ["0 clicks"]
autoTextClick = ["0 cps"]
autoTextButton = ["Boost: 10"]


def changeClicksNumber():
    global clicksForSpace
    global clicksNumber
    clicksNumber += clicksForSpace


def changeAutoClick():
    global clicksPerSecond
    global cost
    global clicksNumber
    if (clicksNumber >= cost):
        clicksNumber -= cost
        clicksPerSecond += 1
        cost *= 2

clicksBox = Box(W * 0.35, H * 0.1, W * 0.325, H * 0.1,
                textClick, INACTIVE_COLOR, ACTIVE_COLOR)
autoClicksBox = Box(W * 0.35, H * 0.5, W * 0.325, H * 0.1,
                    autoTextClick, INACTIVE_COLOR, ACTIVE_COLOR)
clicksButton = Button(W * 0.35, H * 0.3, W * 0.325, H * 0.1,
                      ["Click me"], INACTIVE_COLOR,
                      changeClicksNumber, ACTIVE_COLOR)
autoClicksButton = Button(W * 0.35, H * 0.7, W * 0.325, H * 0.1,
                          autoTextButton, INACTIVE_COLOR,
                          changeAutoClick, ACTIVE_COLOR)

boxes = [clicksBox, clicksButton, autoClicksBox, autoClicksButton]


def go():
    global currentTime
    global clicksNumber
    global lastTime
    currentTime = pygame.time.get_ticks()
    if (currentTime >= lastTime + 1000):
        lastTime = currentTime
        clicksNumber += clicksPerSecond

    textClick[0] = str(clicksNumber) + " clicks"
    autoTextClick[0] = str(clicksPerSecond) + " cps"
    autoTextButton[0] = "Boost: " + str(cost)

    for box in boxes:
        box.doIfPressed()


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                clicksNumber += clicksForSpace

    go()

    for box in boxes:
        box.draw()

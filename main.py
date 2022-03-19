import pygame
from pygame import Rect
from math import floor

from data.constants import *
from data.save_system import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Hud():
    def __init__(self) -> None:
        pass

    def text_display(self, text, color,x,y, size = TILE*4):
        font = pygame.font.Font("data/BebasNeue-Regular.ttf", size)
        font_render = font.render(str(text), True, color)
        window.blit(font_render,(int(x),int(y)))

    def money_count(self, amount):
        self.text_display(f'Money : {amount:,} $', WHITE, 10, 10)
        
    def draw_grid(self):
        for x in range(0, WIDTH, TILE):
            pygame.draw.line(window, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE):
            pygame.draw.line(window, WHITE, (0, y), (WIDTH, y))
    

class Button():
    def __init__(self, pos_x, pos_y, size_x, size_y) -> None:

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

        self.clicked = 0

        self.rect = Rect(pos_x, pos_y, size_x, size_y)

    def click(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.clicked = 1
                    return 1
        else:
            self.clicked = 0

    def render(self):
        if self.clicked:
            pygame.draw.rect(window, MBLUE, self.rect)
        else:
            pygame.draw.rect(window, LBLUE, self.rect)


class Generator():
    def __init__(self, size, upgrades = 0, is_generator = True) -> None:
        self.upgrades = upgrades
        self.is_generator = is_generator
        self.upgrade_growth = 1.07

        self.production_base = values[f"{size}"][0]
        self.productivity = values[f"{size}"][1]

        self.cost_base = values[f"{size}"][2]
        self.cost = self.cost_base * (self.upgrade_growth ** self.upgrades)

        self.production = (self.upgrades * self.productivity)


        if self.is_generator:
            self.speed = size * 60

        for _ in range(self.upgrades):
            self.load_upgrades()
            

    def load_upgrades(self):
        self.cost = self.cost_base * (self.upgrade_growth ** self.upgrades)
        self.production = round(self.production_base + self.productivity * (self.upgrades - 1))


    def upgrade(self, money):
        if money.amount >= self.cost:
            money.amount -= self.cost
            money.amount = round(money.amount, 2)
            self.upgrades += 1

            self.cost = self.cost_base * (self.upgrade_growth ** self.upgrades)
            self.production = floor(self.production_base + self.productivity * (self.upgrades - 1))


class Page(Hud, Button):
    gens = 1
    pages = []
    selfadder_pages = []

    def __init__(self, name, generator_upgrades=0, text="") -> None:

        self.name = name
        self.text = text

        self.pos_x = int(TILE)
        self.pos_y = int(HEIGHT/2)
        self.size_x = int(WIDTH - TILE*2)
        self.size_y = int(HEIGHT/2 - TILE)

        self.x = 0
        self.graphic_gametick = 0

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        self.button = Button(-1,-1,0,0)
        
        if len(self.pages) < 1:
            self.generator = Generator(len(self.pages)+1, 1 if generator_upgrades == 0 else generator_upgrades, False)
        else: 
            self.generator = Generator(len(self.pages)+1 , generator_upgrades)
            self.selfadder_pages.append(self)

        self.pages.append(self)
        self.gens += 1


    def render(self):
        pygame.draw.rect(window, BLUE, self.rect)
        if not self.generator.is_generator:
            pass
        else:
            if self.generator.production == 0:
                pass
            else:
                pygame.draw.rect(window, LBLUE, (int(self.size_x / 2), int(self.pos_y), int(((self.graphic_gametick/self.generator.speed)*self.size_x/2)), int(TILE*4)))


        self.text_display(f'{self.name}', BLACK, TILE*2, self.pos_y)
        self.text_display(f'{self.text}', ORANGE, WIDTH/2, self.pos_y, TILE*2)

        self.text_display(f'Adding by : {self.generator.production:,}', WHITE, TILE*2, self.pos_y + 5*TILE, TILE*3)
        self.text_display(f'Needed to upgrade : {round(self.generator.cost, 2):,} $', WHITE, TILE*2, self.pos_y + 8*TILE, TILE*3)
        self.text_display(f'Upgrade lvl : {self.generator.upgrades:,}', WHITE, TILE*2, self.pos_y + 11*TILE, TILE*3)

        self.button.render()

        if money.amount >= self.generator.cost:
            draw_rect_alpha(window, LGREEN, self.button.rect, 100)

    def upgrades(self, event, money):
        if self.button.click(event):
            self.generator.upgrade(money)

class Money():
    def __init__(self, amount) -> None:
        self.amount = float(amount)

    def add(self, generator):
        self.amount += generator.production
        self.amount = round(self.amount, 2)

    def self_add(self):
        for page in Page.selfadder_pages:  

            if gametick % page.generator.speed == 0:
                money.add(page.generator)
                page.graphic_gametick = 0

            page.graphic_gametick += 1                


def page_dots(pages, page_pos):
    for i, page in enumerate(pages):
        coordinates = (TILE + (TILE*i + TILE)+i, HEIGHT - TILE*2) #Circle Center x, y

        if money.amount >= page.generator.cost:
            draw_circle_alpha(window, WHITE, coordinates, int(TILE/2), 128)
        
        elif i == page_pos:
            pygame.draw.circle(window, LBLUE, coordinates, int(TILE/2))
        
        else:
            pygame.draw.circle(window, MBLUE, coordinates, int(TILE/2))

def window_render():
    window.fill(DARK)
    buttonClicker.render()
    hud.money_count(money.amount)
    Page.pages[page_pos].render() 
    page_dots(Page.pages, page_pos)
    

def draw_rect_alpha(surface, color, rect, alpha):
    color_alpha = (color[0], color[1], color[2], alpha)
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color_alpha, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius, alpha):
    color_alpha = (color[0], color[1], color[2], alpha)
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color_alpha, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def scroll(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                return 1
            elif event.button == 5:
                return 2

def quit(keys):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
        else: return 1
    if keys[pygame.K_ESCAPE]:
        return 0
    else: return 1
    
def save_data():
    for i, page in enumerate(Page.pages):
        data[f"{i}"] = page.generator.upgrades
    data["money"] = money.amount
    data["time"] = gametick



pygame.init()
pygame.mixer.init()
pygame.display.set_caption('IdleG')
clock = pygame.time.Clock()

hud = Hud()

buttonClicker = Button(WIDTH - TILE*17, TILE, TILE*16, TILE*16)
buttonClickUpgrade = Button(-1,-1,0,0)


data = load_file()

money = Money(data["money"])

pick = Page("Clicker", data[f"{len(Page.pages)+1}"])

cats = Page("Cats", data[f"{len(Page.pages)+1}"])

iron = Page("Iron Mine", data[f"{len(Page.pages)+1}"])
silver = Page("Silver Mine", data[f"{len(Page.pages)+1}"])
gold = Page("Gold Ore", data[f"{len(Page.pages)+1}"])


page_pos = 0

running = True
gametick = data["time"]

while running:
    clock.tick(TICK)
    gametick += 1
    
    for page in Page.pages:
        if page != page_pos:
            page.button.rect = Rect(-1,-1,0,0)

    Page.pages[page_pos].button.rect = Rect(UPGRADE_BUTTON_RECT)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_m]:
        money.amount += 10000
    if keys[pygame.K_n]:
        money.amount -= 10000

    for event in pygame.event.get():
        if buttonClicker.click(event):
            money.add(pick.generator)

        for page in Page.pages:
            page.upgrades(event, money)

        if scroll(event) == 2:
            page_pos += 1
            if page_pos == len(Page.pages):
                page_pos = 0
        elif scroll(event) == 1:
            if page_pos == 0:
                page_pos = len(Page.pages)
            page_pos -= 1

    else:
        pass

    money.self_add()

    running = quit(keys)

    window_render()

        # DEBUG TOOLS
    # hud.text_display(f'page:{page_n}', WHITE, TILE*8, TILE*5) # PAGE NUMBER
    # hud.text_display(f'{gametick}', GREEN, TILE*24, TILE*5)   # TICK
    # hud.draw_grid()                                           # GRID
    
    pygame.display.flip()


save_data()
save_file(data)
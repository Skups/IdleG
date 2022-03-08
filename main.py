from pickle import FALSE, TRUE
import pygame
from pygame import Rect
from itertools import count

from constants import *
from save_system import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Hud():
    def __init__(self) -> None:
        pass

    def text_display(self, text, color,x,y, size = TILE*4):
        font = pygame.font.Font("BebasNeue-Regular.ttf", size)
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


class Adder():
    def __init__(self, size, upgrades = 0) -> None:
        self.size = size
        self.addition = self.size
        self.upgrades = upgrades

        self.upgrade_size = 0.2
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10
        self.upgrade_cost_rate = 1.3
        

        for _ in range(self.upgrades):
            self.load_upgrades()

    def load_upgrades(self):
        self.addition += self.upgrade_size
        self.addition = round(self.addition, 2)
        self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
        self.upgrade_cost = round(self.upgrade_cost, 2)
        self.upgrade_size = self.upgrade_size * self.upgrade_size_rate

    def upgrade(self, money):
        if money.amount >= self.upgrade_cost:
            money.amount -= self.upgrade_cost
            money.amount = round(money.amount, 2)

            self.addition += self.upgrade_size
            self.addition = round(self.addition, 2)
            self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
            self.upgrade_cost = round(self.upgrade_cost, 2)
            self.upgrade_size = self.upgrade_size * self.upgrade_size_rate
            self.upgrades += 1



class SelfAdder():
    def __init__(self, size, upgrades = 0) -> None:
        self.size = size
        self.addition = 0
        self.upgrades = upgrades

        self.upgrade_size = 5 ** self.size 
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10 ** (self.size + 1)
        self.upgrade_cost_rate = 1.3
        
        self.speed = self.size * 60

        for _ in range(self.upgrades):
            self.load_upgrades()

    def load_upgrades(self):
        self.addition += self.upgrade_size
        self.addition = round(self.addition, 2)
        self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
        self.upgrade_cost = round(self.upgrade_cost, 2)
        self.upgrade_size = self.upgrade_size * self.upgrade_size_rate
        # self.speed = self.speed - self.upgrades


    def upgrade(self, money):
        if money.amount >= self.upgrade_cost:
            money.amount -= self.upgrade_cost
            money.amount = round(money.amount, 2)
        
            self.addition += self.upgrade_size
            self.addition = round(self.addition, 2)
            self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
            self.upgrade_cost = round(self.upgrade_cost, 2)
            self.upgrade_size = self.upgrade_size * self.upgrade_size_rate
            # self.speed = self.speed - self.upgrades
            self.upgrades += 1




class Page(Hud, Button):
    page_amount = count(0)
    pages = []
    selfadder_pages = []

    def __init__(self, name, adder_upgrades=0, text="") -> None:

        self.name = name
        self.text = text
        self.page_amount = next(self.page_amount)

        self.pos_x = int(TILE)
        self.pos_y = int(HEIGHT/2)
        self.size_x = int(WIDTH - TILE*2)
        self.size_y = int(HEIGHT/2 - TILE)

        self.x = 0
        self.graphic_gametick = 0

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        self.button = Button(-1,-1,0,0)
        
        if self.page_amount < 1:
            self.adder = Adder(1, adder_upgrades)
        else: 
            self.adder = SelfAdder(int(self.page_amount), adder_upgrades)
            self.selfadder_pages.append(self)

        self.pages.append(self)


    def render(self):
        pygame.draw.rect(window, BLUE, self.rect)
        if isinstance(self.adder, Adder):
            pass
        else:
            if self.adder.addition == 0:
                pass
            else:
                pygame.draw.rect(window, LBLUE, (int(self.size_x / 2), int(self.pos_y), int(((self.graphic_gametick/self.adder.speed)*self.size_x/2)), int(TILE*4)))


        self.text_display(f'{self.name}', BLACK, TILE*2, self.pos_y)
        self.text_display(f'{self.text}', ORANGE, WIDTH/2, self.pos_y, TILE*2)

        self.text_display(f'Adding by : {self.adder.addition:,}', WHITE, TILE*2, self.pos_y + 5*TILE)
        self.text_display(f'Next upgrade: {round(self.adder.addition + self.adder.upgrade_size, 2):,}', WHITE, TILE*2, self.pos_y + 9*TILE)
        self.text_display(f'Needed to upgrade : {self.adder.upgrade_cost:,} $', WHITE, TILE*2, self.pos_y + 13*TILE)
        self.text_display(f'Upgrade lvl : {self.adder.upgrades:,}', WHITE, TILE*2, self.pos_y + 17*TILE)

        self.button.render()

        if money.amount >= self.adder.upgrade_cost:
            draw_rect_alpha(window, LGREEN, self.button.rect, 100)

    def upgrades(self, event, money):
        if self.button.click(event):
            self.adder.upgrade(money)

class Money():
    def __init__(self, amount) -> None:
        self.amount = float(amount)

    def add(self, adder):
        self.amount += adder.addition
        self.amount = round(self.amount, 2)

    def self_add(self):
        for selfadder in Page.selfadder_pages:  

            if gametick % selfadder.adder.speed == 0:
                money.add(selfadder.adder)
                selfadder.graphic_gametick = 0

            selfadder.graphic_gametick += 1                


def page_dots(pages, page_pos):
    for i in range(len(pages)):
        coordinates = (TILE + (TILE*i + TILE)+i, HEIGHT - TILE*2) #Circle Center x, y
        if i == page_pos:
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
        data[f"{i}"] = page.adder.upgrades
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

pick = Page("Clicker", data[f"{len(Page.pages)}"])
coal = Page("Coal Mine", data[f"{len(Page.pages)}"])
iron = Page("Iron Mine", data[f"{len(Page.pages)}"])
silver = Page("Silver Mine", data[f"{len(Page.pages)}"])
gold = Page("Gold Ore", data[f"{len(Page.pages)}"])
diamond = Page("Diamonds", data[f"{len(Page.pages)}"])


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
            money.add(pick.adder)

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
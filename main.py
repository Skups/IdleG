import pygame
from pygame import Rect
from itertools import count
from constants import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Utilities():
    def __init__(self) -> None:
        pass

    def round(self, num):
        num = round(num, 2)

class Control():
    def __init__(self) -> None:
        pass

class Hud():
    def __init__(self, win) -> None:
        self.win = win

    def text_display(self, text, color,x,y, size = TILE*4):
        font = pygame.font.Font("BebasNeue-Regular.ttf", size)
        font_render = font.render(str(text), True, color)
        window.blit(font_render,(x,y))

    def money_count(self, amount):
        self.text_display(f'Money : {amount} $', WHITE, 10, 10)
        
    def draw_grid(self):
        for x in range(0, WIDTH, TILE):
            pygame.draw.line(window, COL1, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE):
            pygame.draw.line(window, COL1, (0, y), (WIDTH, y))
    

class Button():
    def __init__(self, pos_x, pos_y, size_x, size_y) -> None:

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

        self.rect = Rect(pos_x, pos_y, size_x, size_y)

    def click(self,event):
        button = self.rect
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button.collidepoint(event.pos):
                    return 1

    def render(self):
        pygame.draw.rect(window, WHITE, self.rect)


class Adder(Utilities):
    def __init__(self, size) -> None:
        self.size = size
        self.addition = self.size
        self.upgrades = 0

        self.upgrade_size = 0.2
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10
        self.upgrade_cost_rate = 1.3
    
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

        else:
            pass

class SelfAdder():
    def __init__(self, size) -> None:
        self.size = size
        self.addition = 0
        self.upgrades = 0

        self.upgrade_size = 5 ** self.size 
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10 ** (self.size + 1)
        self.upgrade_cost_rate = 1.3
        
        self.speed = self.size * 60

    
    def upgrade(self, money):
        if money.amount >= self.upgrade_cost:
            money.amount -= self.upgrade_cost
            money.amount = round(money.amount, 2)
            
            self.addition += self.upgrade_size
            self.addition = round(self.addition, 2)
            self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
            self.upgrade_cost = round(self.upgrade_cost, 2)
            self.upgrade_size = self.upgrade_size * self.upgrade_size_rate
            self.speed = self.speed - self.upgrades
            self.upgrades += 1

        else:
            pass



class Page(Hud, Button):
    page_amount = count(0)
    pages = []
    selfadder_pages = []

    def __init__(self, name, text="") -> None:

        self.name = name
        self.text = text
        self.page_amount = next(self.page_amount)

        self.pos_x = TILE
        self.pos_y = HEIGHT/2
        self.size_x = WIDTH - TILE*2
        self.size_y = HEIGHT/2 - TILE

        self.x = 0

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        self.button = Button(-1,-1,0,0)
        
        if self.page_amount < 1:
            self.adder = Adder(1)
        else: 
            self.adder = SelfAdder(int(self.page_amount))
            self.selfadder_pages.append(self)

        self.pages.append(self)


    def render(self):
        pygame.draw.rect(window, COL4, self.rect)
        if isinstance(self.adder, Adder):
            pass
        else:
            if self.adder.addition == 0:
                pass
            else:
                if gametick % self.adder.speed == 0:
                    self.x = gametick // self.adder.speed
                    print(self.x)
                graphic_gametick = gametick - (self.x * self.adder.speed)
                # else:
                #     graphic_gametick = gametick
                pygame.draw.rect(window, COL6, (self.pos_x, self.pos_y, ((graphic_gametick/self.adder.speed)*self.size_x), self.size_y))


        self.text_display(f'{self.name}', COL2, TILE*2, self.pos_y)
        self.text_display(f'{self.text}', COL6, WIDTH/2, self.pos_y, TILE*2)

        self.text_display(f'Adding by :{self.adder.addition}', WHITE, TILE*2, self.pos_y + 5*TILE)
        self.text_display(f'Needed to upgrade : {self.adder.upgrade_cost}', WHITE, TILE*2, self.pos_y + 9*TILE)
        self.text_display(f'Upgrade lvl : {self.adder.upgrades}', WHITE, TILE*2, self.pos_y + 13*TILE)

        if money.amount >= self.adder.upgrade_cost:
            pygame.draw.rect(window, GREEN, self.button.rect)
        else:
            pygame.draw.rect(window, WHITE, self.button.rect)

    def upgrades(self, event, money):
        if self.button.click(event):
            self.adder.upgrade(money)

class Money(Utilities):
    def __init__(self, amount) -> None:
        self.amount = float(amount)

    def add(self, adder):
        self.amount += adder.addition
        self.amount = round(self.amount, 2)

def page_dots(pages, page_pos):
    for i in range(len(pages)):
        coordinates = (TILE + (TILE*i + TILE)+i, HEIGHT - TILE*2) #Circle Center x, y
        if i == page_pos:
            pygame.draw.circle(window, COL3, coordinates, int(TILE/1.5))
        else:
            pygame.draw.circle(window, COL5, coordinates, int(TILE/2))



def window_render():
    window.fill(COL3)
    buttonClicker.render()
    hud.money_count(money.amount)

    Page.pages[page_pos].render() 
    page_dots(Page.pages, page_pos)
    

def scroll(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                return 1
            elif event.button == 5:
                return 2

def quit(keys):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        else: return True
    if keys[pygame.K_ESCAPE]:
        return False
    else: return True



pygame.init()
pygame.mixer.init()


pygame.display.set_caption('IdleG')
clock = pygame.time.Clock()

hud = Hud(window)

money = Money(0)
buttonClicker = Button(WIDTH - TILE*17, TILE, TILE*16, TILE*16)
buttonClickUpgrade = Button(-1,-1,0,0)


pick = Page("Clicker", "click click click...")
coal = Page("Coal Mine", "mining coal since the 1700s")
iron = Page("Iron Mine")
silver = Page("Silver Mine")
gold = Page("Gold Ore")

page_pos = 0

running = True
gametick = 0

while running:
    clock.tick(TICK)
    gametick += 1
    if gametick == 360:
        gametick = 0

    
    for page in Page.pages:
        if page != page_pos:
            page.button.rect = Rect(-1,-1,0,0)

    Page.pages[page_pos].button.rect = Rect(UPGRADE_BUTTON_RECT)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_m]:
        money.amount += 100 

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

    for selfadder in Page.selfadder_pages:

        if gametick % selfadder.adder.speed == 0:
            money.add(selfadder.adder)

    running = quit(keys)


    window_render()

        # DEBUG TOOLS
    # hud.text_display(f'page:{page_n}', WHITE, TILE*8, TILE*5) # PAGE NUMBER
    # hud.text_display(f'{gametick}', GREEN, TILE*24, TILE*5)   # TICK
    # hud.draw_grid()                                           # GRID
  
  
    pygame.display.flip()
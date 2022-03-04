from ast import While
from email.header import Header
from turtle import width
import pygame
from pygame import Rect

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

    def text_display(self, text, color,x,y):
        font = pygame.font.SysFont('Trebuchet MS', TILE*4)
        font_render = font.render(str(text), True, color)
        window.blit(font_render,(x,y))

    def money_count(self, amount):
        # if purchasable:
        #     self.text_display(f'Money : {amount}', GREEN, 10, 10)
        # else:
        self.text_display(f'Money : {amount} $', WHITE, 10, 10)
        
    def adders(self, size, upgrade_cost, upgrades):
        self.text_display(f'Adding by :{size}', WHITE, 10, 40)
        self.text_display(f'Needed to upgrade : {upgrade_cost}', WHITE, 10, 60)
        self.text_display(f'Upgrade lvl : {upgrades}', WHITE, 10, 80)
    
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

class Page(Hud, Button):
    def __init__(self, name, text, button, adder) -> None:

        self.name = name
        self.text = text

        self.pos_x = TILE
        self.pos_y = HEIGHT/2
        self.size_x = WIDTH - TILE*2
        self.size_y = HEIGHT/2 - TILE

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

        self.button = button
        self.adder = adder

    def render(self, size, upgrade_cost, upgrades, button):
        pygame.draw.rect(window, GREY, self.rect)

        self.text_display(f'{self.name}', BLACK, TILE*2, self.pos_y)

        self.text_display(f'Adding by :{size}', WHITE, TILE*2, self.pos_y + 5*TILE)
        self.text_display(f'Needed to upgrade : {upgrade_cost}', WHITE, TILE*2, self.pos_y + 9*TILE)
        self.text_display(f'Upgrade lvl : {upgrades}', WHITE, TILE*2, self.pos_y + 13*TILE)

        pygame.draw.rect(window, WHITE, button.rect)


class Money(Utilities):
    def __init__(self, amount) -> None:
        self.amount = float(amount)

    def add(self, adder):
        self.amount += adder.size
        self.amount = round(self.amount, 2)


class Adder(Utilities):
    def __init__(self, size) -> None:
        self.size = size
        self.upgrades = 0

        self.upgrade_size = 0.2
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10
        self.upgrade_cost_rate = 1.3
    

    def upgrade(self, money):
        if money.amount >= self.upgrade_cost:
            money.amount -= self.upgrade_cost
            money.amount = round(money.amount, 2)
            
            self.size += self.upgrade_size
            self.size = round(self.size, 2)
            self.upgrade_cost = self.upgrade_cost * self.upgrade_cost_rate
            self.upgrade_cost = round(self.upgrade_cost, 2)
            self.upgrade_size = self.upgrade_size * self.upgrade_size_rate
            self.upgrades += 1
        else:
            pass

class SelfAdder(Adder):
    def __init__(self, size) -> None:
        self.size = size
        self.upgrades = 0

        self.upgrade_size = 0.2
        self.upgrade_size_rate = 1.2

        self.upgrade_cost = 10
        self.upgrade_cost_rate = 1.3
        

        self.speed = 1
        self.speedcalc = 5 * (TICK / (self.speed)) 




def window_render():
    window.fill(BLACK)
    buttonClicker.render()
    hud.money_count(money.amount)



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

adder = Adder(1)
selfAdder1 = SelfAdder(1)
selfAdder2 = SelfAdder(2)
money = Money(0)
hud = Hud(window)

buttonClicker = Button(WIDTH - TILE*9, TILE, TILE*8, TILE*8)
buttonClickUpgrade = Button(TILE*49, TILE*38, TILE*8, TILE*4)
buttonUpgrade1 = Button(TILE*49, TILE*38, TILE*8, TILE*4)
buttonUpgrade2 = Button(TILE*49, TILE*38, TILE*8, TILE*4)

pick = Page("Clicker", "click click click...", buttonClickUpgrade, adder)
coal = Page("Coal Mine", "mining coal since the 1700s", buttonUpgrade1, selfAdder1)
iron = Page("Iron Mine", "iron ore pouring out all the time", buttonUpgrade2, selfAdder2)

pages = [pick, coal, iron]

running = True
gametick = 0

page_n = 0


while running:
    clock.tick(TICK)
    gametick += 1

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        
        if buttonClicker.click(event):
            money.add(adder)

        elif coal.click(event):
            adder.upgrade(money)

        elif buttonUpgrade2.click(event):
            selfAdder1.upgrade(money)


        elif keys[pygame.K_RIGHT]:
            page_n += 1
            if page_n == len(pages):
                page_n = 0
        elif keys[pygame.K_LEFT]:
            if page_n == 0:
                page_n = len(pages)
            page_n -= 1

    else:
        pass

    if gametick / selfAdder1.speedcalc == 0:
        money.add(selfAdder1)

    

    running = quit(keys)


    window_render()
    pages[page_n].render(pages[page_n].adder.size, pages[page_n].adder.upgrade_cost, pages[page_n].adder.upgrades, pages[page_n].button) 
    hud.text_display(f'page:{page_n}', WHITE, TILE*8, TILE*5)
    pygame.display.flip()
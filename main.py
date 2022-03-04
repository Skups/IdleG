import pygame
from pygame import Rect

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
        font = pygame.font.SysFont('Trebuchet MS', 24)
        font_render = font.render(str(text), True, color)
        self.win.blit(font_render,(x,y))

    def money_count(self, amount):
        self.text_display(f'Money : {amount}', WHITE, 10, 10)
        
    def adders(self, size, upgrade_cost, upgrades):
        self.text_display(f'Adding by :{size}', WHITE, 10, 40)
        self.text_display(f'Needed to upgrade : {upgrade_cost}', WHITE, 10, 60)
        self.text_display(f'Upgrade lvl : {upgrades}', WHITE, 10, 80)

class Button(Hud):
    def __init__(self, pos_x, pos_y, size, Hud) -> None:
        super().__init__(Hud.win)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size

        self.rect = Rect(pos_y, pos_x, size, size)

    def click(self,event):
        button = self.rect
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if event.type == 1:
                if button.collidepoint(event.pos):
                    return 1

    def render(self):
        pygame.draw.rect(self.win, WHITE, self.rect)

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
        super().__init__(size)
        self.speed = 1

    def tick(self):
        return self.speed


def window_render():
    window.fill(BLACK)

    button1.render()
    button2.render()

    hud.money_count(money.amount)
    hud.adders(adder.size, adder.upgrade_cost, adder.upgrades)
    pygame.display.flip()

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

window = pygame.display.set_mode((480, 360))
pygame.display.set_caption('IdleG')
clock = pygame.time.Clock()

adder = Adder(1)
# adder1 = SelfAdder(1)
money = Money(0)
hud = Hud(window)

button1 = Button(10, 220, 20, hud)
button2 = Button(40, 220, 10, hud)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



running = True

while running:
    clock.tick(60)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        

        if button1.click(event):
            money.add(adder)
        elif keys[pygame.K_a]:
            adder.upgrade(money)
        elif button2.click(event):
            adder.upgrade(money)
    # elif keys[pygame.K_1]:
    #     adder1.upgrade(money)
    else:
        pass

    

    running = quit(keys)

    window_render()

from pygame import Color
TILE = 8*2
WIDTH = 480*2
HEIGHT = 360*2

UPGRADE_BUTTON_RECT = (WIDTH-TILE*10, HEIGHT-TILE*6, TILE*8, TILE*4)
NULL_BUTTON_RECT = (-1,-1,0,0)

BLACK = (0, 0, 0)
WHITE = Color("#ffeecc")    #WHITE
DARK = Color("#46425e")     #DARK
BLUE = Color("#15788c")     #BLUE
MBLUE = Color("#0c96a5")    #MIDDLE BLUE
LBLUE = Color("#00b9be")    #LIGHT BLUE
ORANGE = Color("#ffb0a3")   #ORANGE
RED = Color("#ff6973")      #RED
LGREEN = Color("#a3ffd7")   #LIGHT GREEN
GREEN = Color("#73ff69")    #GREEN

TICK = 60

        #prod_base, prod, cost_base

values = {
    "1": (1, 1.67, 3.738),
    "2": (60, 20, 60),
    "3": (540, 90, 720),
    "4": (4320, 360, 8640),
    "5": (51840, 2160, 103680),
}


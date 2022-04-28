# Game Settings
import random
import os

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
maps_Folder = os.path.join(assets_Folder, "maps")
audio_Folder = os.path.join(assets_Folder, "audio")

# screen size
WIDTH = 1024 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 480 # 16 * 30 or 32 * 15 or 64 * 7.5

#tile properties
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# game title
TITLE = "Runner" #Sets title
FONT_NAME = 'arial'

# Player Size
PLAYER_HEIGHT = HEIGHT / 15
PLAYER_WIDTH = PLAYER_HEIGHT

#player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -.1
PLAYER_GRAV = 0.8
PLAYER_JUMP = 16
PLAYER_SPEED = 300

#platform properties
PLATFORM_SPEED = 5

#Bullet Properties
BULLET_SPEED = 15
BARREL_OFFSET = 22
FIRE_RATE = 150

#cards
CARD_LIST = ['card1.txt', 'card2.txt', 'card3.txt', 'card4.txt', 'card5.txt', 'card6.txt']

# clock speed
FPS = 60 #sets frames per second (clock tick)

# difficulty
diff = "Normal" #sets difficulty


# Colors (R,G,B)
BLACK = (0, 0, 0)
GRAY = (50,50,50)
LIGHTGRAY = (100,100,100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 155, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255, 0)
skyBlue = (135,206,235)
darkBlue = (86, 105, 184)
cfBlue = (100, 149, 237)
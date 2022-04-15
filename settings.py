# Game Settings
import random
import os

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")

#High score file
HS_FILE = "highscore.txt"

#Spritesheet file
SPRITESHEET = "pass"


# game title
TITLE = "Runner" #Sets title
FONT_NAME = 'arial'

# screen size
WIDTH = 1042 #sets width of screen
HEIGHT = 480 #sets height of screen

# Player Size
PLAYER_HEIGHT = HEIGHT / 15
PLAYER_WIDTH = PLAYER_HEIGHT

#player properties
PLAYER_ACC = 1.25
PLAYER_FRICTION = -.075
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game Properties


# clock speed
FPS = 60 #sets frames per second (clock tick)

# difficulty
diff = "Normal" #sets difficulty
PLATFORM_SPEED = 8
PLATFORM_LIST = ((WIDTH+150, HEIGHT / 2, 250, 20),
                 (WIDTH +450, HEIGHT / 4, 200, 20),
                 (WIDTH +450, HEIGHT * (3 / 4), 200, 20),
                 (WIDTH + 800, HEIGHT * (5/8), 300, 20),
                 (WIDTH + 1200, HEIGHT * (3/8), 250, 20))


# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255, 0)
skyBlue = (135,206,235)
darkBlue = (86, 105, 184)
cfBlue = (100, 149, 237)
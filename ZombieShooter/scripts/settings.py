import os.path
import pygame as pg
from scripts.tile_map import *
from random import *
vec = pg.math.Vector2


# define colors, colors work in a (RGB) format.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PINK = (255,0,255)
ORANGE = (255,127,0)
DARK_GRAY = (40,40,40)
LIGHT_GRAY = (100,100,100)
GRAY_BLUE = (92,192,194)
BROWN = (106,55,5)

colors = (WHITE,BLUE,BLACK,RED,GREEN,YELLOW,TEAL,PINK,ORANGE)



#Game Title
TITLE = "CHANGE ME THIS IS WRONG!"



# Window Settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
DEFAULT_COLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


# camera settings
fps = 60

# file locations
#gets location of file on computer
game_folder = os.path.dirname(__file__)
game_folder = game_folder.replace("\scripts","")
sprites_folder = os.path.join(game_folder,"sprites")
playerSprites = os.path.join(sprites_folder,"playerSprites")
enemySprites = os.path.join(sprites_folder,"enemySprites")
map_folder = os.path.join(game_folder,"maps")
map_sprites_folder = os.path.join(sprites_folder,"mapSprites")
item_sprites_folder = os.path.join(sprites_folder, 'ItemSprites')
snd_folder = os.path.join(game_folder,'snd_fx')
snd_fx_folder = os.path.join(snd_folder,'effects')
music_folder = os.path.join(snd_folder,'music')
pain_folder = os.path.join(snd_fx_folder,'pain')
TITLE_FONT = os.path.join(sprites_folder, 'ZOMBIE.TTF')
HUD_FONT = os.path.join(sprites_folder, 'Impacted2.0.ttf')




#Player Settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 380
PLAYER_ROT_SPEED = 300
PLAYER_IMG = os.path.join(playerSprites, "manBlue_gun.png")
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(30,10)
PLAYER_SPLAT_IMG = os.path.join(playerSprites,'splat red.png')

#Weapon Settings
BULLET_IMG = os.path.join(playerSprites,"bullet.png")
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed':500,
                     'bullet_lifetime':1000,
                     'rate':250,
                     'kickback':200,
                     'spread':5,
                     'damage':10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed':400,
                     'bullet_lifetime':500,
                     'rate':1200,
                     'kickback':500,
                     'spread':25,
                     'damage':5,
                     'bullet_size': 'sm',
                     'bullet_count':18}

# Enemy Settings
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_SPEED = [150,175,150,200,250]
MOB_IMG = os.path.join(enemySprites,'zombie1_hold.png')
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400
ZOMBIE_SPLAT_IMG = os.path.join(enemySprites, 'splat green.png')

#Map Settings
MAP1 = os.path.join(map_folder, 'map1.txt')
MAP2 = os.path.join(map_folder, 'map2.txt')
WALL_IMG = os.path.join(map_sprites_folder,'tile_358.png')
TILEDMAP = os.path.join(map_folder, 'Tiled1.tmx')


#Effects
MUZZLE_FLASHES = [os.path.join(playerSprites,'whitePuff15.png'),
                  os.path.join(playerSprites,'whitePuff16.png'),
                  os.path.join(playerSprites,'whitePuff17.png'),
                  os.path.join(playerSprites,'whitePuff18.png')]
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0,255,45)]

#layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items

HEALTH_PACK = os.path.join(item_sprites_folder, 'health_pack.png')
HEALTH_PACK_AMOUNT = 50
SHOTGUN_IMG = os.path.join(playerSprites, 'obj_shotgun.png')

ITEM_IMAGES = {'Health':HEALTH_PACK,
               'Shotgun':SHOTGUN_IMG}
BOB_RANGE = 15
BOB_SPEED = 0.5

#sounds
BG_MUSIC = os.path.join(music_folder,'espionage.wav')
PLAYER_HIT_SOUNDS = [os.path.join(pain_folder,'8.wav'),
                     os.path.join(pain_folder,'9.wav'),
                     os.path.join(pain_folder,'10.wav'),
                     os.path.join(pain_folder,'11.wav')]
ZOMBIE_MOAN_SOUNDS = [os.path.join(snd_fx_folder,'brains2.wav'),
                      os.path.join(snd_fx_folder,'brains3.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-1.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-2.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-3.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-5.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-6.wav'),
                      os.path.join(snd_fx_folder,'zombie-roar-7.wav')]
ZOMBIE_HIT_SOUNDS = [os.path.join(snd_fx_folder, 'splat-15.wav')]
WEAPON_SOUNDS = {'pistol':[os.path.join(snd_fx_folder,"sfx_weapon_singleshot2.wav")],
                 'shotgun':[os.path.join(snd_fx_folder,'shotgun.wav')]}
EFFECTS_SOUNDS = {'level_start': os.path.join(snd_fx_folder,'level_start.wav'),
                  'health_up': os.path.join(snd_fx_folder,'health_pack.wav'),
                  'gun_pickup': os.path.join(snd_fx_folder,'gun_pickup.wav')}




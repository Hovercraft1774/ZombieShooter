from scripts.settings import *
import pygame as pg
import pytmx
WIDTH = 1024   # isn't reading width/height even though settings is formated right
HEIGHT = 768

def collide_hit_rect(one,two): #adds the hit rect to normal collides
    return one.hit_rect.colliderect(two.rect)

class Map: #loads a text map
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width*TILESIZE
        self.height = self.tile_height*TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        #scroll only to wall
        x = min(0,x) #left wall
        y = min(0,y) #top wall
        x = max(-(self.width-WIDTH),x) #right wall
        y = max(-(self.height-HEIGHT),y) #bottom wall
        self.camera = pg.Rect(x,y,self.width,self.height)

from scripts.settings import *
from scripts.tile_map import *
vec = pg.math.Vector2
from itertools import chain
import pytweening as tween


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):#must be a sprite inherited otherwise it won't fit in groups

    def __init__(self,game,x,y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites,game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game  # adds reference to the game
        # self.PLAYER_IMG = pg.transform.flip(self.PLAYER_IMG, True, True) #this flips the image along the x,y axis
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.damaged = False


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED,0).rotate(-self.rot)#goes straight, but in the way we are rotated
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2,0).rotate(-self.rot)#half speed going back
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'],WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()#stops overlapping sound
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA*2)

    def add_health(self,amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def update(self):
        self.get_keys()
        self.rot = (self.rot+self.rot_speed*self.game.dt)% 360 #if rotate 360 change angle back to one. no integer overload
        self.image = pg.transform.rotate(self.game.player_img,self.rot)
        if self.damaged:
            #alpha determines how transparent an image is
            try:#cycles through transparencies to get flashing damaged effect
                self.image.fill((255,255,255,next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.wall_group,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.wall_group,'y')
        self.rect.center = self.hit_rect.center


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir,damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullet_group
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos) #get a new vector otherwise it moves the player too
        self.rect.center = pos
        # spread = uniform(-GUN_SPREAD,GUN_SPREAD)
        self.vel = dir*WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9,1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.wall_group):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.wall_group.add(self)

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups = game.wall_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        size = randint(20,50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Item(pg.sprite.Sprite):
    def __init__(self,game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items_group
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1


    def update(self):
        #bobbing motion
        offset = BOB_RANGE * (self.tween(self.step/BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1














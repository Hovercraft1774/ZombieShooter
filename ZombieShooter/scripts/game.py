import random

from scripts.settings import *
from scripts.player import *
from scripts.enemy import *
from scripts.tile_map import *
from scripts.settings import *







def draw_player_health(surf,x,y,pct):
    if pct< 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game(object):

    def __init__(self):
        self.playing = True
        pg.mixer.pre_init(44100,-16,1,2048) #helps with sound lag
        pg.init()
        pg.mixer.init() #if using online editor, take this out
        # creates a screen for the game
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE) #Title of the screen window
        # creates time
        self.clock = pg.time.Clock()
        self.defaultColor = DEFAULT_COLOR
        pg.key.set_repeat(200,200)
        self.load_data()


    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def load_data(self):
        self.title_font = TITLE_FONT
        self.hud_font = HUD_FONT
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,190)) #goes up to 255, dims the screen aka transparency
        self.player_img = pg.image.load(PLAYER_IMG).convert_alpha() #convert alpha also does colorkey background
        self.wall_img = pg.image.load(WALL_IMG)
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        self.mob_img = pg.image.load(MOB_IMG).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(BULLET_IMG).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10,10))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(img).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(ITEM_IMAGES[item]).convert_alpha()
        #Sound Loading
        pg.mixer.music.load(BG_MUSIC)
        pg.mixer.music.set_volume(0.5)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            s = pg.mixer.Sound(EFFECTS_SOUNDS[type])
            s.set_volume(0.2)
            self.effects_sounds[type] = s
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(snd)
                s.set_volume(0.1)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        self.load_sound(ZOMBIE_MOAN_SOUNDS,self.zombie_moan_sounds,0.1)
        self.player_hit_sounds = []
        self.load_sound(PLAYER_HIT_SOUNDS,self.player_hit_sounds,0.3)
        self.zombie_hit_sounds = []
        self.load_sound(ZOMBIE_HIT_SOUNDS,self.zombie_hit_sounds,0.2)
        self.zombie_splat = pg.image.load(ZOMBIE_SPLAT_IMG).convert_alpha()
        self.zombie_splat = pg.transform.scale(self.zombie_splat, (TILESIZE,TILESIZE))

    def load_sound(self,list,group,volume):
        for snd in list:
            s = pg.mixer.Sound(snd)
            s.set_volume(volume)
            group.append(s)




    def new(self):
        self.map = TiledMap(TILEDMAP)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # create Sprite Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mob_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.items_group = pg.sprite.Group()

        # create player player objects


        #create walls
        # for row, tiles in enumerate(self.map.data): #enumerate gives both the index value and the item
        #     for col,tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self,col,row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row, PLAYER_IMG)
        #         if tile == 'M':
        #             Mob(self, col, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x+ tile_object.width/2,
                             tile_object.y + tile_object.height/2)
            if tile_object.name == 'Player':
                self.player = Player(self,obj_center.x,obj_center.y)
            if tile_object.name == 'Wall':
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name == 'ZombieSpawn':
                Mob(self,obj_center.x,obj_center.y)
            if tile_object.name == "Bush":
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name in ['Health', 'Shotgun']:
                Item(self,obj_center, tile_object.name)

        self.camera = Camera(self.map.width,self.map.height)
        self.draw_debug = False
        self.effects_sounds['level_start'].play()
        self.paused = False



    def gameLoop(self):
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(fps)/1000
            #tick clock
            self.clock.tick(fps)

            #check events
            self.check_Events()

            #update all
            if not self.paused:
                self.update()

            #draw
            self.draw()


    def check_Events(self):
        if len(self.mob_group) ==0:
            self.playing = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_F3:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_k:
                    for mob in self.mob_group:
                        mob.kill()

    #player hits item
        hits = pg.sprite.spritecollide(self.player,self.items_group, False)
        for hit in hits:
            if hit.type == 'Health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'Shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'

    #mob hits player
        hits = pg.sprite.spritecollide(self.player,self.mob_group, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
    #bullet hits mob
        hits = pg.sprite.groupcollide(self.mob_group, self.bullet_group, False, True)#bullet hit mobs
        for mob in hits: #hits checks each mob hit, then does a dictionary of bullets that hit
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0,0)


    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # bullets hit mobs


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (x,0), (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (0,y), (WIDTH,y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                print(sprite)
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.wall_group:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text("Zombies: {}".format(len(self.mob_group)), self.hud_font, 30, WHITE, WIDTH-10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align='center')



        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        pg.display.flip()

    def start_Screen(self):
        pass
    def end_Screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH/2, HEIGHT/2, align='center')
        self.draw_text("Press any key to quit", self.title_font, 75, WHITE, WIDTH/2, HEIGHT*3/4, align='center')
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()#stops key events from holding from game
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                    exit()
                if event.type == pg.KEYUP:
                    waiting = False



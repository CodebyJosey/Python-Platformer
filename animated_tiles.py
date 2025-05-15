import pygame as pg
from sprites import import_folder, import_coins, import_wheel, import_enemies, import_flag
from player import Player
import random
from settings import tile_size


class Coin(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.imports()
        self.index = 0
        self.animation_speed = random.choice([0.04, 0.05, 0.06, 0.07, 0.08])

        self.type = random.choice(['gold', 'silver', 'bluediamond', 'greendiamond', 'reddiamond', 'redpotion', 'goldenskull'])

        self.image = self.animations[self.type][self.index]
        self.rect = self.image.get_rect(topleft = pos)

        self.status = self.type

    def imports(self):
        character_path = 'C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/coins/'
        self.animations = {'gold': [], 'silver': [], 'bluediamond': [], 'greendiamond': [], 'reddiamond': [], 'redpotion': [], 'goldenskull': []} 

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_coins(full_path)

    def animatie(self):
        animation = self.animations[self.type]

        self.index += self.animation_speed

        if self.index >= len(animation):
            self.index = 0

        image = animation[int(self.index)]
        self.image = image

    def update(self, x_shift):
        self.animatie()
        self.rect.x += x_shift

class Wheel(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.imports()
        self.index = 0
        self.animation_speed = 0.15

        self.image = self.animations['random'][self.index]
        self.rect = self.image.get_rect(topleft = pos)

        self.status = 'random'

    def imports(self):
        character_path = 'C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/wheel'
        self.animations = {'random': []}

        for animation in self.animations.keys():
            full_path = character_path
            self.animations[animation] = import_wheel(full_path)

    def animatie(self):
        animation = self.animations['random']

        self.index += self.animation_speed

        if self.index >= len(animation):
            self.index = 0

        image = animation[int(self.index)]
        self.image = image

    def update(self, x_shift):
        self.animatie()
        self.rect.x += x_shift

class Flag(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.imports()
        self.index = 0
        self.animation_speed = 0.15

        self.image = self.animations['flag'][self.index]
        self.rect = self.image.get_rect(topleft = pos)

        self.status = 'flag'

    def imports(self):
        character_path = 'C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/flag'
        self.animations = {'flag': []}

        for animation in self.animations.keys():
            full_path = character_path
            self.animations[animation] = import_flag(full_path)

    def animatie(self):
        animation = self.animations['flag']

        self.index += self.animation_speed

        if self.index >= len(animation):
            self.index = 0

        image = animation[int(self.index)]
        self.image = image

    def update(self, x_shift):
        self.animatie()
        self.rect.x += x_shift

class MovingPlatforms(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.speed = 1.375
        self.direction = 1
        self.start = pos[0]
        self.range = 50
        self.type = type

        if self.type == 'grass':
            self.image = pg.transform.scale(pg.image.load('C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/Grass.png'), (tile_size, tile_size))
        elif self.type == 'dirt':
            self.image = pg.transform.scale(pg.image.load('C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/Dirt.png'), (tile_size, tile_size))
        else:
            raise ValueError(f"{self.type} is onbekend!")
        
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += self.direction * self.speed + x_shift
        self.start += x_shift

        if self.direction == 1 and self.rect.x >= self.start + self.range:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.start - self.range:
            self.direction = 1

class Enemies(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.imports()

        # Animations
        self.index = 0
        self.animation_speed = 0.1

        # Default status
        self.status = 'run'

        # Movement
        self.speed = random.choice([1.05, 1.1, 1.15, 1.2, 1.35, 1.5, 1.65, 1.8, 1.95, 2.1])
        self.direction = 1
        self.start = pos[0]
        self.range = 2 * tile_size
        self.double = False

        # Image & rect
        self.image = self.animations[self.status][self.index]
        flipped_image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=pos)

        # Health 
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_width = self.rect.width
        self.health_bar_height = 5

    def imports(self):
        self.type = random.choice(['toothy', 'pinky', 'crab'])
        character_path = f'C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/enemys/{self.type}/'
        self.animations = {'run': [], 'hit': [], 'die': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_enemies(full_path)

            if self.animations[animation] is None:
                raise ValueError(f"Error: Animatie '{animation}' voor enemy '{self.type}' niet kunnen laden")

    def animatie(self):
        self.animation = self.animations[self.status]
        self.index += self.animation_speed

        if self.status == 'die':
            self.index = 0
        if self.index >= len(self.animation):
            if self.status == 'die':
                self.kill()
            else:
                self.index = 0

        image = self.animation[int(self.index)]
        if self.direction == -1:
            self.image = image
        else:
            flipped_image = pg.transform.flip(image, True, False)
            self.image = flipped_image

    def update(self, x_shift):
        self.animatie()
        self.rect.x += self.direction * self.speed + x_shift
        self.start += x_shift

        if self.double == True:
            self.range = 120

        if self.direction == 1 and self.rect.x >= self.start + self.range:
            self.direction = -1
            if not self.double:
                self.double = True
        elif self.direction == -1 and self.rect.x <= self.start - self.range:
            self.direction = 1
            if not self.double:
                self.double = True
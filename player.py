import pygame as pg
import sys, random
from sprites import import_folder, jump_sound
from health import *

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        # Initialisatie
        super().__init__()
        self.imports()

        # Animation
        self.index, self.animation_speed = 0, 0.15

        # Op het scherm
        self.image = self.animations['idle'][self.index]
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.direction, self.speed = pg.math.Vector2(0, 0), 0.1
        
        # Jump
        self.gravity, self.jump_speed, self.max_jump_count, self.jump_count, self.jump_cooldown, self.jump_cooldown_duration, self.last_jump_time = 0.42, -12, 3, 0, False, 0.45, 0.0

        # Status
        self.status = 'idle'
        self.rechts = True

        # Health
        self.health = 100

        # Sounds
        self.sound_played = True

    def imports(self):
        self.character = random.choice(["1", "2", "3"])
        character_path = f'C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/character{self.character}/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'die': [], 'shoot': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animatie(self):
        animation = self.animations[self.status]
        self.index += self.animation_speed

        if self.index >= len(animation):
            if self.status == 'die':
                pg.quit()
                sys.exit()
            if self.status == 'shoot':
                self.index = 0
                self.get_status()
            else:
                self.index = 0

        image = animation[int(self.index)]
        if not self.rechts:
            image = pg.transform.flip(image, True, False)
        self.image = image

    def movement(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.status != 'die':
                self.direction.x = 1
                self.rechts = True
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            if self.status != 'die':
                self.direction.x = -1
                self.rechts = False
        else:
            self.direction.x = 0

        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            if self.status != 'die':
                if self.sound_played:
                    self.sound_played = False
                if not self.sound_played:
                    # jump_sound.play()
                    self.sound_played = True
                self.jump()

        if keys[pg.K_s]:
            if self.status != 'die':
                self.status = 'shoot'

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            if health_bar.hp <= 0:
                self.status = 'die'
            else:
                if self.direction.x != 0:
                    self.status = 'run'
                elif pg.key.get_pressed()[pg.K_s]:
                    self.status = 'shoot'
                else:
                    self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        current_time = pg.time.get_ticks() / 1000

        if self.jump_count < self.max_jump_count:
            if not self.jump_cooldown:
                self.direction.y = self.jump_speed
                self.jump_count += 1
                self.last_jump_time = current_time
                self.jump_cooldown = True
                #jump_sound.play()

        if self.jump_cooldown and current_time - self.last_jump_time >= self.jump_cooldown_duration:
            self.jump_cooldown = False
            self.jump_count = 0

    def shoot(self):
        if pg.key.get_pressed()[pg.K_s]:
            self.status = 'shoot', self.animatie()

    def update(self):
        self.movement(), self.get_status(), self.animatie(), self.shoot()
import pygame as pg
import sys, time
from tiles import *
from settings import tile_size, WIDTH
from player import Player
from health import *
from animated_tiles import Coin, Wheel, Flag, Enemies, MovingPlatforms
from sprites import coin_collect, coin_decrease, import_wheel

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.collision_cooldown = 0
        self.coins = 0

        self.win = False

        self.sound_played = True

    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        self.wheel = pg.sprite.Group()
        self.flag = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.diamond = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        self.platform = pg.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'G':
                    tile = Tile('grass')
                    tile.create_tile((x, y), tile_size, 'grass')
                    self.tiles.add(tile)
                elif cell == 'D':
                    tile = Tile('dirt')
                    tile.create_tile((x, y), tile_size, 'dirt')
                    self.tiles.add(tile)
                elif cell == 'B':
                    tile = Tile('border')
                    tile.create_tile((x,y), tile_size, 'border')
                    self.tiles.add(tile)
                elif cell == 'K':
                    tile = Tile('killingborder')
                    tile.create_tile((x, y), tile_size, 'killingborder')
                    self.tiles.add(tile)
                elif cell == 'S':
                    tile = Tile('spikes')
                    tile.create_tile((x,y), tile_size, 'spikes')
                    self.tiles.add(tile)
                elif cell == 'V':
                    tile = Tile('barrel')
                    tile.create_tile((x, y), tile_size, 'barrel')
                    self.tiles.add(tile)
                elif cell == '1':
                    player = Player((x, y))
                    self.player.add(player)
                elif cell == 'C':
                    coin = Coin((x, y))
                    self.coin.add(coin)
                elif cell == 'W':
                    wheel = Wheel((x, y))
                    self.wheel.add(wheel)
                elif cell == 'F':
                    flag = Flag((x, y))
                    self.flag.add(flag)
                elif cell == 'L':
                    enemy = Enemies((x, y))
                    self.enemies.add(enemy)
                elif cell == 'A':
                    platform = MovingPlatforms((x, y), 'grass')
                    self.platform.add(platform)
                elif cell == 'Y':
                    platform = MovingPlatforms((x, y), 'dirt')
                    self.platform.add(platform)

    def scroll_systeem(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else: 
            self.world_shift = 0
            player.speed = 8

    def horizontale_movement_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        coin = self.coin.sprites

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, MovingPlatforms):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                if isinstance(sprite, Tile) and sprite.tile_type == 'spikes':
                    health_bar.hp -= 0.5
                    self.collision_cooldown = 60
                elif isinstance(sprite, Tile) and sprite.tile_type == 'killingborder':
                    pg.quit()
                    sys.exit()
                else:
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

        for sprite in self.platform.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, MovingPlatforms):
                        if player.direction.x < 0:
                            player.rect.left = sprite.rect.right
                        elif player.direction.x > 0:
                            player.rect.right = sprite.rect.left

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if enemy.status != 'die':
                    if isinstance(enemy, Enemies):
                        health_bar.hp = 0

        for sprite in self.flag.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, Flag):
                    self.win = True
                    health_bar.hp = health_bar.max_hp

        for sprite in self.coin.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, Coin):
                    if sprite.type == 'redpotion':
                        health_bar.hp += 15
                    self.sound_played = False
                    choice = random.choice([1, 2])
                    if choice == 1:
                        self.coins += random.randint(1, 3)
                    elif choice == 2:
                        amount = random.randint(1, 3)
                        if self.coins - amount <= 0:
                            self.coins += amount
                        else:
                            self.coins -= amount
                    if self.sound_played == False:
                        if choice == 1:
                            coin_collect.play()
                        elif choice == 2:
                            if self.coins - amount <= 0:
                                coin_collect.play()
                            else:
                                coin_decrease.play()
                        self.sound_played = True
                    self.coin.remove(sprite)

                else:
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

    def verticale_movement_collisions(self):
        player = self.player.sprite
        player.apply_gravity()
        coin = self.coin.sprites
        diamond = self.diamond.sprites
        enemies = self.enemies.sprites

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, Tile) and sprite.tile_type == 'spikes':
                    health_bar.hp -= 0.5
                    self.collision_cooldown = 60
                elif isinstance(sprite, Tile) and sprite.tile_type == 'killingborder':
                    pg.quit()
                    sys.exit()
                else:
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

        for sprite in self.platform.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, MovingPlatforms):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if enemy.status != 'die':
                    if isinstance(enemy, Enemies):
                        health_bar.hp = 0

        for sprite in self.flag.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, Flag):
                    self.win = True
                    health_bar.hp = health_bar.max_hp

        for sprite in self.coin.sprites():
            if sprite.rect.colliderect(player.rect):
                if isinstance(sprite, Coin):
                    if sprite.type == 'redpotion':
                        health_bar.hp += 15
                    self.sound_played = False
                    choice = random.choice([1, 2])
                    if choice == 1:
                        self.coins += random.randint(1, 3)
                    elif choice == 2:
                        amount = random.randint(1, 3)
                        if self.coins - amount <= 0:
                            self.coins += amount
                        else:
                            self.coins -= amount
                    if self.sound_played == False:
                        if choice == 1:
                            coin_collect.play()
                        elif choice == 2:
                            if self.coins - amount <= 0:
                                coin_collect.play()
                            else:
                                coin_decrease.play()
                        self.sound_played = True
                    self.coin.remove(sprite)
                else:
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0                
    def run(self):
        # Level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # Coin
        self.coin.update(self.world_shift)
        self.coin.draw(self.display_surface)

        # Wheel
        self.wheel.update(self.world_shift)
        self.wheel.draw(self.display_surface)

        # Flag
        self.flag.update(self.world_shift)
        self.flag.draw(self.display_surface)

        # Enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)

        # Platforms
        self.platform.update(self.world_shift)
        self.platform.draw(self.display_surface)

        # Player
        self.player.update()

        self.scroll_systeem()
        self.horizontale_movement_collisions()
        self.verticale_movement_collisions()
        self.player.draw(self.display_surface)

        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1 
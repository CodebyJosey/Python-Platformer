import pygame as pg
import sys, random, time
from settings import *
from tiles import Tile
from level import Level
from sprites import *
from player import Player
from health import *

pg.init()

screen, clock, FPS = pg.display.set_mode((WIDTH, HEIGHT)), pg.time.Clock(), 60
level = Level(level_map, screen)

pg.display.set_icon(logo)

big_cloud_image, small_cloud1_image, small_cloud2_image, small_cloud3_image = pg.transform.scale_by(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/clouds/Big Clouds.png").convert_alpha(), 1.25), pg.transform.scale_by(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/clouds/Small Cloud 1.png").convert_alpha(), 2), pg.transform.scale_by(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/clouds/Small Cloud 2.png").convert_alpha(), 2), pg.transform.scale_by(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/clouds/Small Cloud 3.png").convert_alpha(), 2)
cloud_images = [big_cloud_image, small_cloud1_image, small_cloud2_image, small_cloud3_image]

class Cloud:
    def __init__(self, x, y, speed, image):
        self.x, self.y, self.speed = x, y, speed
        self.image = image
        self.size = image.get_size()

    def move(self):
        self.x += self.speed

        if self.x > WIDTH:
            self.x = -self.size[0]

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))

class Text:
    def __init__(self, x, y, text, size, color):
        self.x = x
        self.y = y
        self.text = text
        self.font = pg.font.SysFont("behnschrift", size)
        self.color = color
        self.surface = self.font.render(text, True, color)

        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def check_collision(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

play_text = Text((WIDTH / 2), (HEIGHT / 4), "Play", 40, "white")
cloud_list = [Cloud(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2), random.uniform(0.1, 0.8), random.choice(cloud_images)) for _ in range(random.randint(3, 5))]

def main():
    
    pg.display.set_caption('Pixel Platformer - Main Menu') 

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if play_text.check_collision(mouse_pos):
                    game()

        play_text.draw(screen)

        pg.display.update()
        clock.tick(FPS)

def game():
    pg.display.set_caption('Pixel Platformer - Game')
    run = True

    while run:
        coin_txt = pg.font.SysFont("behnschrift", 45).render(f"{level.coins}", True, "white")
        coin_txt_r = coin_txt.get_rect(topleft=(90, coin_rect.y + 10))

        time = pg.font.SysFont("behnschrift", 45).render(f"{round((pg.time.get_ticks() / 1000), 1)}", True, "white")
        time_r = time.get_rect(topleft=(90, 150))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

        for cloud in cloud_list:
            cloud.move()

        screen.fill("white")
        screen.blit(background, (0, 0))

        for cloud in cloud_list:
            cloud.draw(screen)

        health_bar.draw(screen)
        screen.blit(health, health_rect), screen.blit(coin_txt, coin_txt_r), screen.blit(coin, coin_rect), screen.blit(clock_icon, clock_rect), screen.blit(time, time_r)

        if level.win == True:
            pass
            
        level.run()

        pg.display.update()
        clock.tick(FPS)

game()


# CODE VOOR COIN SYSTEEM MET SHOP

def get_current_coins():
  with open('coins.txt', 'r') as file:
    current_coins = int(file.read()) 
  return current_coins

def update_current_level(coins):
  with open('level.txt', 'w') as file:
    file.write(str(coins))
current_coins = get_current_coins()

print(current_coins)
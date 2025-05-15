from os import walk
import pygame as pg
from settings import WIDTH, HEIGHT, tile_size

pg.init()

logo = pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/logo.png")

background = pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/background.png")
background = pg.transform.scale(background, (WIDTH, HEIGHT))

coin = pg.transform.scale(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/map/coins/gold/01.png"), (45, 45))
coin_rect = coin.get_rect(topleft=(33, 82))

clock_icon = pg.transform.scale(pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/clock.png"), (40, 40))
clock_rect = clock_icon.get_rect(topleft=(36, 142))

health = pg.image.load("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/heart.png")
health = pg.transform.scale(health, (35, 35))
health_rect = health.get_rect(topleft = (36, 42))

coin_collect = pg.mixer.Sound("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/coin_collect.mp3")
coin_decrease = pg.mixer.Sound("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/coin_decrease.mp3")
jump_sound = pg.mixer.Sound("C:/Users/josey/Privé/Programmeren/Portfolio/Platformer/Animations/graphics/assets/jump_sound.mp3")

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            image_surf = pg.transform.scale_by(image_surf, 0.0825)
            surface_list.append(image_surf)

        return surface_list
    
def import_coins(path):
    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            image_surf = pg.transform.scale(image_surf, (tile_size * 0.9, tile_size * 0.9))
            surface_list.append(image_surf)

        return surface_list
    
def import_enemies(path):
    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            image_surf = pg.transform.scale_by(image_surf, (1.875))
            surface_list.append(image_surf)

        return surface_list
    
def import_wheel(path):
    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            image_surf = pg.transform.scale(image_surf, (tile_size, tile_size))
            surface_list.append(image_surf)

        return surface_list
    
def import_flag(path):
    surface_list = []

    for _,__,img_files in walk(path):

        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            image_surf = pg.transform.scale_by(image_surf, (1.15))
            surface_list.append(image_surf)

        return surface_list
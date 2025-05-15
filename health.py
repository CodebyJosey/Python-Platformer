import pygame as pg

class Health:
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        border_width = 2  # Breedte van de rand

        pg.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))

        filled_width = self.w * ratio
        pg.draw.rect(surface, "green", (self.x, self.y, filled_width, self.h))

        # Teken de rand rondom de groene balk
        pg.draw.rect(surface, "black", (self.x, self.y, self.w, self.h), border_width)

health_bar = Health(90, 42, 200, 30, 100)
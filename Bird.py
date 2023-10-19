import pygame
import random

from config import *

class Bird:
    """
    Este es el jugador, se puede elegir uno random o no.
    """

    def __init__(self,x,y,w,h,color,flap,human=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.color = color
        
        self.speed = 0
        self.flap = flap
        
        self.score = 0
        self.state = "live"
        self.human = human

    def jump(self):
        self.speed = self.flap

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)

    def update(self):
        # Sólo cae
        self.speed += GRAVITY
        self.y += self.speed

        # Si no es humano salta
        if not self.human:
            if random.random()<0.09:
                self.jump()
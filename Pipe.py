import random
import pygame 

from config import *


class Pipe:
    """
    El juego tiene sólo una tubería, que se mueve hacia la izquierda y reinicia su posición.
    """

    def __init__(self,x,y,w,h,color,speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.speed = speed

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)
        pygame.draw.rect(screen, self.color, [self.x, self.y+self.h+150, self.w, SCREEN_HEIGHT], 0)

    def update(self):
        self.x -= self.speed

        if self.x < -self.w:
            self.x = SCREEN_WIDTH
            self.h = random.randint(150, 350)
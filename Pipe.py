import os
import random
import pygame 

from config import *

def get_pipe_assets(rotate,width,height):
    colors = ["green","red"]
    color = "green"

    scaled_sprite = pygame.transform.scale(pygame.image.load(os.path.join("assets/sprites", f"pipe-{color}.png")),(width,height))
    sprite = pygame.transform.rotate(scaled_sprite, 180 if rotate else 0)
    return sprite



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
        screen.blit(get_pipe_assets(True,self.w, self.h), (self.x,self.y, self.w, self.h))
        screen.blit(get_pipe_assets(False,self.w, SCREEN_HEIGHT/1.5), (self.x, self.y+self.h+150, self.w, SCREEN_HEIGHT))

    def update(self):
        self.x -= self.speed

        if self.x < -self.w:
            self.x = SCREEN_WIDTH
            self.h = random.randint(150, 350)

    def getCenter(self,screen):
        center = (int(self.x + (self.w/2)), int(self.y + (self.h+75)))
        return center
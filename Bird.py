import pygame
import random
import scipy.spatial.distance as distances

from config import *
from BrainV2 import *

structure = [6,4,1]

class Bird:
    """
    Este es el jugador, se puede elegir uno random o no.
    """

    def __init__(self,x,y,w,h,color,flap,human=False,brain="random"):
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

        self.brain = Brain(structure, []) if brain == "random" else Brain(structure, brain)

    def jump(self):
        self.speed = self.flap

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)

    def update(self, enviroment):
        # Sólo cae
        self.speed += GRAVITY
        self.y += self.speed

        # Si no es humano salta
        if not self.human:
            action = self.brain.predict(enviroment)
            if action > 0.5:
                self.jump()

    def measure(self, screen, pipe):
        bird_center = (int(self.x + (self.w/2)), int(self.y + (self.h/2)))
        
        # Measure the euclidean distance between center of bird - center pipe
        pipe_center = pipe.getCenter(screen)
        
        distance = distances.euclidean(bird_center, pipe_center)
        return (bird_center, pipe_center, distance)
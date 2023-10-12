import sys
import pygame
import random

from utils import *
from config import *

pygame.init()


# Inicialización de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Reloj
clock = pygame.time.Clock()

# Fuentes
font = pygame.font.Font(None, 36)

# Variables del juego
GRAVITY = 1


def show_score(score):
    score_text = font.render("Puntaje: " + str(score), True, (0,0,0))
    screen.blit(score_text, (10, 10))


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

    def update(self,gravity):
        self.speed += gravity
        self.y += self.speed

    def get_move(self):
        if random.random()<0.09:
            self.jump()



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


def gen_players(N):
    players = []

    for i in range(N):
        players.append(Bird(
            x=50,
            y=SCREEN_HEIGHT // 2,
            w=50,
            h=30,
            color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
            flap=-12,
            human=False            
        ))

    return players


players = gen_players(20)
players.append(Bird(
            x=50,
            y=SCREEN_HEIGHT // 2,
            w=50,
            h=30,
            color=(0,0,0),
            flap=-12,
            human=True            
        )   
)

live_players = len(players)

pipe = Pipe(
    x=SCREEN_WIDTH,
    y=0,
    w=50,
    h=random.randint(150, 350),
    color=(0,255,0),
    speed=5
)

mean_score = 0

# Bucle principal del juego
running = True


def restart():
    global pipe,players,live_players

    pipe.x = SCREEN_WIDTH
    players = gen_players(20)
    players.append(Bird(
                x=50,
                y=SCREEN_HEIGHT // 2,
                w=50,
                h=30,
                color=(0,0,0),
                flap=-12,
                human=True            
            )   
    )

    live_players = len(players)




def main():
    global live_players

    while live_players>0:
        # Events and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for player in players:
                    if player.human and player.state == "live":
                        player.jump()

        # Si el jugador no es humano
        for player in players:
            if player.state=="live":
                if not player.human:
                    player.get_move()

        # Player Moving
        for player in players:
            if player.state == "live":
                player.update(GRAVITY)

        # Pipe Moving
        pipe.update()

        # EL escenario y el jugador deben colisionar en todo momento, si no lo hacen, el jugador ha salido de los límites.
        for player in players:
            if player.state=="live":
                if not colission([0,0,SCREEN_WIDTH,SCREEN_HEIGHT],[player.x,player.y,player.w,player.h]):
                    player.state = "dead"
                    live_players-=1

        # Si el jugador toca una tubería, se muere.
        for player in players:
            if player.state=="live":
                if check_pipe_collisions(player,pipe):
                    player.state = "dead"
                    live_players-=1

        # Si el jugador está entre una tubería y no la toca gana puntos.
        for player in players:
            if player.state=="live":
                if pipe.x < player.x + 50 and not check_pipe_collisions(player,pipe):
                    player.score += 1

        # Fondo
        screen.fill((255, 255, 255))

        # Jugador
        for player in players:
            if player.state=="live":
                player.draw(screen)

        # Tuberías
        pipe.draw(screen)

        # Information
        # for player in players:
        #     mean_score+= player.score/len(players)
        
        show_score(live_players)

        if live_players == 0:
            restart()

        # Update screen
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()

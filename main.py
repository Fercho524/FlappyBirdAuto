import os
import sys
import pygame
import random

pygame.init()

from utils import *
from config import *

from Bird import Bird
from Pipe import Pipe
from GA import *

poblation = 100

def show_score(score,live_players):
    info = f"Global Score : {int(SCORE)} Live Players : {live_players}"
    score_text = FONT.render(info, True, WHITE)
    SCREEN.blit(score_text, (10, 10))


def gen_players(N):
    players = []

    for i in range(N):
        players.append(Bird(
            x=50,
            y=SCREEN_HEIGHT // 2,
            w=50,
            h=30,
            color=random.randint(0,2),
            flap=-12,
            human=False            
        ))

    return players


PLAYERS = gen_players(poblation)
# Generamos el jugador humano
"""PLAYERS.append(Bird(
            x=50,
            y=SCREEN_HEIGHT // 2,
            w=50,
            h=30,
            color=(0,0,0),
            flap=-12,
            human=True            
        )   
)"""

live_players = len(PLAYERS)

pipe = Pipe(
    x=SCREEN_WIDTH,
    y=0,
    w=50,
    h=random.randint(150, 350),
    color=(0,255,0),
    speed=5
)

SCORE = 0


def restart():
    global pipe,PLAYERS,live_players,SCORE

    SCORE = 0
    pipe.x = SCREEN_WIDTH
    pipe.speed = 5
    for player in PLAYERS:
        player.state="live"
        player.score=0

    live_players = len(PLAYERS)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for player in PLAYERS:
                if player.human and player.state == "live":
                    player.jump()


def check_bounds():
    global live_players

    # EL escenario y el jugador deben colisionar en todo momento, si no lo hacen, el jugador ha salido de los límites.
    for player in PLAYERS:
        if player.state=="live":
            if not colission([0,0,SCREEN_WIDTH,SCREEN_HEIGHT],[player.x,player.y,player.w,player.h]):
                player.state = "dead"
                live_players-=1


def check_player_pipe_colissions():
    global live_players

    for player in PLAYERS:
        if player.state=="live":
            if check_pipe_collisions(player,pipe):
                player.state = "dead"
                live_players-=1


sky = pygame.transform.scale(pygame.image.load(os.path.join("assets/sprites", f"background-day.png")),(SCREEN_WIDTH,SCREEN_HEIGHT))

def draw_background(screen):
    screen.blit(sky, (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_players(screen):
    for player in PLAYERS:
        if player.state=="live":
            player.draw(screen)


def check_player_score():
    global SCORE

    for player in PLAYERS:
        if player.state=="live":
            #if pipe.x < player.x + 50 and not check_pipe_collisions(player,pipe):
            if not check_pipe_collisions(player,pipe):
                #SCORE += 1
                player.score += 1
                SCORE+=1/len(PLAYERS)

                
def update_players(sc, pipe):
    for player in PLAYERS:
        if player.state == "live":
            center_bird, center_pipe, distance = player.measure(sc, pipe)
            player.update([center_bird[0], center_bird[1], center_pipe[0],center_pipe[1], distance, pipe.speed])

def main():
    global live_players,SCORE, PLAYERS
    history = []
    while live_players>0:
        # Eventos de cierre y control manual
        handle_events()

        # Player Moving, si el jugador no es humano planifica su movimiento
        #measure_distances(SCREEN, pipe)
        update_players(SCREEN, pipe)

        # Pipe Moving
        pipe.update()

        # Verifica que los jugadores estén dentro del escenario
        check_bounds()

        # Si el jugador toca una tubería, se muere.
        check_player_pipe_colissions()

        # Si el jugador está entre una tubería y no la toca gana puntos.
        check_player_score()

        # Fondo
        draw_background(SCREEN)

        # Jugador
        draw_players(SCREEN)

        # Tuberías
        pipe.draw(SCREEN)


        # Incremento de velocidad
        if SCORE % 100 == 0 and SCORE >= 100:
            pipe.speed+= SPEED_INC

        # Despliegue de información
        show_score(SCORE,live_players)

        # Reinicio cuando todos mueren
        if live_players == 0:            
            # Revisamos los mejores individuos de la generacion
            PLAYERS,history = evolve(PLAYERS,history)
            restart()

        # Update screen
        pygame.display.update()
        CLOCK.tick(30)


if __name__ == "__main__":
    main()
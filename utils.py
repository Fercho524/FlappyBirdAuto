from config import *

def colission(rect1, rect2):
    """
    Sólo verifica si 2 rectángulos se superponen o no
    """
    x1, y1, ancho1, alto1 = rect1
    x2, y2, ancho2, alto2 = rect2

    # Verificar si los rectángulos se superponen en el eje X
    colision_x = (x1 < x2 + ancho2) and (x1 + ancho1 > x2)

    # Verificar si los rectángulos se superponen en el eje Y
    colision_y = (y1 < y2 + alto2) and (y1 + alto1 > y2)

    # Si hay colisión en ambos ejes, entonces hay una colisión total
    if colision_x and colision_y:
        return True
    else:
        return False
    
def check_pipe_collisions(bird,pipe):
    """
    Verifica que un pájaro no toque la tubería de arriba o la de abajo.
    """
    return colission([bird.x,bird.y,bird.w,bird.h],[pipe.x, pipe.y, pipe.w, pipe.h]) or colission([bird.x,bird.y,bird.w,bird.h],[pipe.x, pipe.y+pipe.h+150, pipe.w, SCREEN_HEIGHT])

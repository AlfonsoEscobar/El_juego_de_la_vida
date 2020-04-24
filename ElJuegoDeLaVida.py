import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la ventana del juego
width, height = 600, 600

#creamos la ventana
screen = pygame.display.set_mode((height, width))


# Color del fondo del juego
bg = 25, 25, 25

# Pintamos el fondo con el color
screen.fill(bg)

# Cantidad de celdas en cada eje
nxC, nyC = 50, 50

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas vivas = 1. Muertas  = 0
# Inicializando con ceros
gameState = np.zeros((nxC, nyC))



# Automatas
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control del juego
pause = True

# Contrala la finalizacion del juego
endGame = False

#bucle de ejecucion
while not endGame:

    newGameState = np.copy(gameState)

    # Se vuelve a colorear la pantalla
    screen.fill(bg)

    # Se duerme para que no vaya tan rapido
    time.sleep(0.1)

    # Capturamos cualquier evento de pulsacion
    ev = pygame.event.get()
    
    for event in ev:

        # Si cierran la ventana finalizo el juego
        if event.type == pygame.QUIT:
            endGame = True

        # Si se toca una tecla se pausa o reanuda el juego
        if event.type == pygame.KEYDOWN:
            pause = not pause

        # Deteccion del click del mouse
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = 1

    # Se recorre cada una de las celdas generadas
    for y in range(0, nxC):
        for x in range(0, nyC):
            
            if not pause:

                # Calculamos los vecinos de todas las celadas
                # y si llegamos al borde volvemos por el otro lado
                n_neight =  gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x)     % nxC, (y - 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x - 1) % nxC, (y)     % nyC] + \
                            gameState[(x + 1) % nxC, (y)     % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                            gameState[(x)     % nxC, (y + 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1) % nyC]


                # Regla nº1: Una celula muerta con exactamente 3 vecinas vivas, "revive" 
                if gameState[x, y] == 0 and n_neight == 3:
                    newGameState[x, y] = 1


                # Regla nº 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas, "muere"
                elif gameState[x, y] == 1 and (n_neight < 2 or n_neight > 3):
                    newGameState[x, y] = 0

                # Creamos las celdas
            poly = [((x)     * dimCW,  y      * dimCH),
                    ((x + 1) * dimCW,  y      * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x)     * dimCW, (y + 1) * dimCH)]

            # Dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pause:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla.
    pygame.display.flip()



    


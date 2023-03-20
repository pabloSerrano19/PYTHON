import pygame
import random
import time
import asyncio

async def main():
    # run pygame
    pygame.init()
    pygame.mixer.init()
    sonido_fondo = pygame.mixer.Sound("C418-Wet-Hands-Minecraft-Volume-Alpha.wav")

    # display screen size an the title  
    size = (500, 500)
    screen = pygame.display.set_mode(size)


    # maque block grid 
    grid_size = (10,10)
    grid = [[0 for x in range(grid_size[0])] for y in range(grid_size[1])]
    mines = 10

    # display random mines  
    for i in range(mines):
        x = random.randint(0, grid_size[0]-1)
        y = random.randint(0, grid_size[1]-1)
        grid[x][y] = 1

    # game over variable 
    game_over = False

    #make grid of revealed
    revealed = [[False for x in range(grid_size[0])] for y in range(grid_size[1])]

    # make grid of flagged  
    flagged = [[False for x in range(grid_size[0])] for y in range(grid_size[1])]

    # text font 
    font = pygame.font.Font(None, 30)
    fontb = pygame.font.Font(None, 50)

    def reveal_empty_cells(x, y):
        # check if is reveled  
        if (x < 0 or x >= grid_size[0] or y < 0 or y >= grid_size[1] or revealed[x][y]):
            return
        
        revealed[x][y] = True
        
        # check mines around 
        mines_around = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= x+i < grid_size[0]) and (0 <= y+j < grid_size[1]) and grid[x+i][y+j] == 1:
                    mines_around += 1
        if mines_around == 0:
            # reveal empty cells 
            for i in range(-1, 2):
                for j in range(-1, 2):
                    reveal_empty_cells(x+i, y+j)

    def minesAround(mines_around):
        # print the numbers of mine around  
        if mines_around == 0:
            Img= pygame.image.load ("cuadrado.png")
            screen.blit(Img, (x*50, y*50))
        elif mines_around == 1:
            Img= pygame.image.load ("Tiles.png")
            screen.blit(Img, (x*50, y*50))

        elif mines_around ==2:
            Img= pygame.image.load ("Tiles2.png")
            screen.blit(Img, (x*50, y*50))

        elif mines_around==3:
            Img= pygame.image.load ("Tiles3.png")
            screen.blit(Img, (x*50, y*50))  
        elif mines_around==4:
            Img= pygame.image.load ("Tiles4.png")
            screen.blit(Img, (x*50, y*50))
    # game loop  
    running = True

    start_time = time.time()

    while running:
        pygame.mixer.Sound.play(sonido_fondo,-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get the x and y for the click of the mouse 
                pos = pygame.mouse.get_pos()
                x = pos[0] // 50                            
                y = pos[1] // 50
                print(x,y)
                if event.button == 1:
                    # check if mine is pressed 
                    if grid[x][y] == 1:
                        game_over = True
                        pygame.mixer.Sound.stop
                    elif not flagged[x][y]:
                        reveal_empty_cells(x, y)
                elif event.button == 3:
                    flagged[x][y] = not flagged[x][y]
        
        time_left = 120 - (time.time() - start_time)
        time_left = int(time_left)
        if time_left < 0:
            game_over=True
        texto_tiempo=time_left
        pygame.display.set_caption("BUSCAMINAS--> Tiempo Restante "+ str(texto_tiempo)+ " Segundos")
        
        # print the block and the mines in screen
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if game_over and grid[x][y] == 1:
                    pygame.draw.rect(screen, (255,0,0), (x*50, y*50, 50, 50))
                    Img= pygame.image.load ("bomba.png")
                    screen.blit(Img, (x*50, y*50))
                    
                elif not game_over and revealed[x][y]:
                    # check mines around the revealed  
                    mines_around = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (0 <= x+i < grid_size[0]) and (0 <= y+j < grid_size[1]) and grid[x+i][y+j] == 1:
                                mines_around += 1
                    
                    minesAround(mines_around)
                        
                else:
                    # pintar los cuadrados para los no revelados
                    Img= pygame.image.load ("vacia.png")
                    screen.blit(Img, (x*50, y*50))
                    
                    if flagged[x][y]:
                        Img= pygame.image.load ("bandera.png")
                        screen.blit(Img, (x*50, y*50))
    
        #comprobar si se ha perdido 
        if game_over:
            
            pygame.display.flip()
            time.sleep(1)
            pygame.draw.rect(screen, (200,200,200), (0, 0, 500, 500))
            Img= pygame.image.load ("over.png")
            screen.blit(Img, (0, 0))
            pygame.display.flip()
            time.sleep(2)
            running=False
        else:
            #chequear que todos los none-mines esten revelados 
            non_mine_cells = grid_size[0] * grid_size[1] - mines
            cells_revealed = 0
            for x in range(grid_size[0]):
                for y in range(grid_size[1]):
                    if revealed[x][y]:
                        cells_revealed += 1
            if cells_revealed == non_mine_cells:
                pygame.display.flip()
                pygame.draw.rect(screen, (255,255,255), (0, 0, 500, 500))
                text = fontb.render("You Win!", 1, (0, 255, 0))
                screen.blit(text, (170, 200))
                Img= pygame.image.load ("goku_10.gif")
                screen.blit(Img, (0, 0))
                pygame.display.flip()
                time.sleep(2)
                running = False
        pygame.display.flip()

        await asyncio.sleep(0)
    # limpiar y salirse
    
asyncio.run(main())    


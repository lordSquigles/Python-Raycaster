# my headers
import Map
import Player
import render
import texture

# python libraries
import pygame
import pygame.time
import pygame.locals
import numpy as np

# my constants
DEG = np.pi / 180.0 # set a constant for 1 deg
#screenW = 1440 # screen dimensions
#screenH = 1080

screenW = 400 # screen dimensions multiplied by 4. I use this small resolution because python can't handle much higher.
screenH = 300

def handleInputs(player, map, dt):
    for event in pygame.event.get(): # poll pygame for inputs
        if event.type == pygame.QUIT: # quit the program
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN: # key was pressed
            match event.key: # handle movements
                case pygame.K_UP:
                    player.up = 1 # looking up or down
                case pygame.K_DOWN: 
                    player.up = -1
                case pygame.K_w:
                    player.forwards = 1 # moving forwards or backwards
                case pygame.K_s: 
                    player.forwards = -1
                case pygame.K_a:
                    player.sideways = 1 # moving side-to-side
                case pygame.K_d: 
                    player.sideways = -1
                case pygame.K_RIGHT: # turning
                    player.turn = 1
                case pygame.K_LEFT: 
                    player.turn = -1
                case pygame.K_SLASH:
                    player.stats = True if player.stats == False else False
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP:
                    player.up = 0
                case pygame.K_DOWN:
                    player.up = 0
                case pygame.K_w:
                    player.forwards = 0
                case pygame.K_s: 
                    player.forwards = 0
                case pygame.K_a:
                    player.sideways = 0
                case pygame.K_d: 
                    player.sideways = 0
                case pygame.K_RIGHT:
                    player.turn = 0
                case pygame.K_LEFT:
                    player.turn = 0
    dx = player.forwards * np.cos(player.a) * 0.008 * dt + player.sideways * np.cos(player.a - np.pi / 2) * 0.008 * dt # move our player forwards in the dir they are facing 
    dy = player.forwards * np.sin(player.a) * 0.008 * dt + player.sideways * np.sin(player.a - np.pi / 2) * 0.008 * dt

    player.horizon += player.up * 0.25 * dt # vertical look, see: y-shearing
    player.a += player.turn * DEG * dt * 0.13 # turning, increment the player's angle
                                                                                     
    # this collision detection occasionally looks a little buggy; it works very well and is 8 lines, so I do not care
    if dx > 0: # are we moving in the pos x dir?
        try:
            if map.array[int(player.x + dx + 0.5) + int(player.y) * map.w] == 0: player.x += dx # if our dx would place us in a map unit, do not inc x 
        except:
            return(1)
    else: # neg x dir
        try:
            if map.array[int(player.x + dx - 0.5) + int(player.y) * map.w] == 0: player.x += dx # dec x
        except:
            return(1)
    if dy > 0: # are we moving in the pos y dir?
        try:
            if map.array[int(player.x) + int(player.y + dy + 0.5) * map.w] == 0: player.y += dy # do not inc y if it would put us in a wall
        except:
            return(1)
    else: # neg x dir
        try:
            if map.array[int(player.x) + int(player.y + dy - 0.5) * map.w] == 0: player.y += dy # dec y
        except:
            return(1)

def main():
    pxMult = 800 / screenW # our pixel multiplier will allow us to scale-up the screen after rendering at a smaller resolution
    pygame.init() # init pygame
    window = pygame.display.set_mode((screenW * pxMult, screenH * pxMult)) # set up display with defined width and height

    for level in range(3):
        player = Player.Player(2, 2, np.pi / 2.0, screenH, screenW) # create player object
        try: map = Map.Map(r"Levels/" + str(level) + ".csv", screenH) # load our map
        except:
            print('There is no "next level,"; exiting...')
            break
        wallTex = texture.Texture(pygame.image.load(r'Textures/converted2.png')) # load our wall textures
        floorTex = texture.Texture(pygame.image.load(r'Textures/floors.png')) # load our floor textures

        font = pygame.font.Font("freesansbold.ttf", 14) # for typing on screen
        print("Level", level)
        levelText = font.render("Level " + str(level) + " ", True, (0, 255, 0))
        levelBox = levelText.get_rect()
        levelBox.right = screenW * pxMult

        prev = 0 # get the initial time

        while True: # game loop
            now = pygame.time.get_ticks() # get the current time
            dt = now - prev # delta time from subtracting last time
            prev = now # set last time to this one

            if handleInputs(player, map, dt) == 1: # keybinds
                break

            window.fill((0, 120, 80))
            pygame.draw.rect(window, (0, 80, 120), [0, 0, screenW * pxMult, player.horizon * pxMult])

            render.drawFloors(window, player, floorTex, screenH, screenW, pxMult)
            #render.render(player, map, window, wallTex, screenW, screenH, pxMult)
            timeLeft = 60 * (level + 1) - now / 1000

            time = font.render(" Timer: " + str(timeLeft)[:5], True, (0, 255, 0))
            if timeLeft < 0: break
            window.blit(time, (screenW * pxMult / 2 - 50, 0))
            if player.stats:
                fps = font.render(" fps: " + str(1000 / dt)[:3], True, (0, 255, 0)) # 1 frame has passed over dt, we need how many frames over 1 sec (1000 ms)
                location = font.render(" X: " + str(player.x)[:5] + ", Y: " + str(player.y)[:5] + ", \u03B8: " + str(player.a)[:6], True, (0, 255, 0)) # 1 frame has passed over dt, we need how many frames over 1 sec (1000 ms)
                #looking = font.render("Looking at: (" + str(player.la[0]) + ", " + str(player.la[1]) + ")")
                window.blit(levelText, levelBox)
                window.blit(fps, (0, 0))
                window.blit(location, (0, 15))

            pygame.display.update()
    pygame.quit()
    return
main()

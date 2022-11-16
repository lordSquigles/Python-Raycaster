# my headers
import level
import character
import render

# python libraries
import pygame
import pygame.time
import pygame.locals
import math

# my constants
DEG = math.pi / 180.0 # set a constant for 1 deg
screenW = 1440 # screen dimensions
screenH = 1080

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
    dx = player.forwards * math.cos(player.a) * 0.01 * dt + player.sideways * math.cos(player.a - math.pi / 2) * 0.01 * dt # move our player forwards in the dir they are facing 
    dy = player.forwards * math.sin(player.a) * 0.01 * dt + player.sideways * math.sin(player.a - math.pi / 2) * 0.01 * dt

    player.horizon += player.up * dt # vertical look, see: y-shearing
    player.a += player.turn * DEG * dt * 0.1 # turning, increment the player's angle
                                                                                     
    player.a %= 2 * math.pi # normalize our angle for collisions
    if player.a < 0: player.a += 2 * math.pi

    # this collision detection occasionally looks a little buggy; it works very well and is 8 lines, so I do not care
    if dx > 0: # are we moving in the pos x dir?
        if map.array[int(player.y)][int(player.x + dx + 0.5)] == 0: player.x += dx # if our dx would place us in a map unit, do not inc x
    else: # neg x dir
        if map.array[int(player.y)][int(player.x + dx - 0.5)] == 0: player.x += dx # dec x
    if dy > 0: # are we moving in the pos y dir?
        if map.array[int(player.y + dy + 0.5)][int(player.x + dx)] == 0: player.y += dy # do not inc y if it would put us in a wall
    else: # neg x dir
        if map.array[int(player.y + dy - 0.5)][int(player.x + dx)] == 0: player.y += dy # dec y
    #if map.array[int(player.y + dy)][round(player.x + dx)] == 0: player.x += dx # collision detection
    #if map.array[round(player.y + dy)][int(player.x + dx)] == 0: player.y += dy

def main():
    pygame.init() # init pygame
    window = pygame.display.set_mode((screenW, screenH)) # set up display with defined width and height

    player = character.Player(8, 8, math.pi / 2.0, screenH / 2) # create player object
    map = level.Map(r"map.csv", screenH)

    font = pygame.font.Font("freesansbold.ttf", 14) # for typing on screen

    prev = 0 # get the initial time

    # lets make some constants to save conputation time
    constants = {}
    constants['fovInc'] = player.fov / screenW
    constants['fovHalf'] = player.fov / 2
    constants['screenW'] = screenW
    constants['screenH'] = screenH

    while True: # game loop
        now = pygame.time.get_ticks() # get the current time
        dt = now - prev # delta time from subtracting last time
        prev = now # set last time to this one

        handleInputs(player, map,dt) # keybinds

        window.fill((255, 255, 255))

        #render.drawMap(player, map, window)

        render.render(player, map, window, constants)

        if player.stats:
            fps = font.render(" fps: " + str(1000 / dt)[:3], True, (0, 255, 0), (0, 0, 0)) # 1 frame has passed over dt, we need how many frames over 1 sec (1000 ms)
            location = font.render(" X: " + str(player.x)[:5] + ", Y: " + str(player.y)[:5] + ", \u03B8: " + str(player.a)[:6], True, (0, 255, 0), (0, 0, 0)) # 1 frame has passed over dt, we need how many frames over 1 sec (1000 ms)
            #looking = font.render("Looking at: (" + str(player.la[0]) + ", " + str(player.la[1]) + ")")
            window.blit(fps, (0, 0))
            window.blit(location, (0, 15))

        pygame.display.update()
    input()
    return
main()

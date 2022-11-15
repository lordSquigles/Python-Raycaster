import pygame
import pygame.locals
import math
import os

DEG = math.pi / 180.0 # set a constant for 1 deg

class Player: # create our player class
    x = 0
    y = 0
    a = 0 # the angle the player is facing
    fov = math.pi / 3
    forwards = 0
    sideways = 0
    def __init__(self, x, y, a):
        self.x = x
        self.y = y
        self.a = a 
    

screenW = 1000 # screen dimensions
screenH = 500

class Map:
    array = []
    w = 0
    h = 0
    tileSize = 0
    def __init__(self, file):
        mf = open(file, "r")
        mapFile = mf.read().split("\n")
        mapFile.pop(-1)

        for i in mapFile:
            self.array.append([int(j) for j in i.replace(" ", "").split(",")])

        self.w = len(self.array) # width of 1st element
        self.h = len(self.array[0])# number of elements

        self.tileSize = screenH / len(self.array)

def clear(): return os.system('clear') # debugging stuff

def handleInputs(player):
    for event in pygame.event.get(): # poll pygame for inputs
        if event.type == pygame.QUIT: # quit the program
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN: # key was pressed
            match event.key: # handle movements
                case pygame.K_UP:
                    player.forwards = 1
                case pygame.K_DOWN: 
                    player.forwards = -1
                case pygame.K_LEFT: 
                    player.sideways = -1
                case pygame.K_RIGHT: 
                    player.sideways = 1
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP:
                    player.forwards = 0
                case pygame.K_DOWN:
                    player.forwards = 0
                case pygame.K_LEFT:
                    player.sideways = 0
                case pygame.K_RIGHT:
                    player.sideways = 0
    player.x += player.forwards * math.cos(player.a) * 0.1
    player.y += player.forwards * math.sin(player.a) * 0.1
    player.a += player.sideways * DEG

def render(player, map, window):
    for x in range(screenW // 2):

        # my implementation of lodev's DDA algorithm ()

        angle = player.a - player.fov / 4 + x * player.fov / screenW
        #angle = player.a

        rayDirX = math.cos(angle) # get the unit vector for our angle
        rayDirY = math.sin(angle)
        #pygame.draw.line(window, (0, 255, 255), [player.x * map.tileSize, player.y * map.tileSize], [(player.x + 16 * rayDirX) * map.tileSize, (player.y + 16 * rayDirY)* map.tileSize])

        deltaDistX = (1 + (rayDirY / rayDirX) ** 2) ** 0.5 # calc the amount to increment sideDistX and sideDistY by
        deltaDistY = (1 + (rayDirX / rayDirY) ** 2) ** 0.5
        
        mapX = int(player.x) # set the initial map square
        mapY = int(player.y)

        sideDistX = 0.0 # the x and y side distances of our ray
        sideDistY = 0.0

        stepX = 0 # the direction(s) our ray is walking in the map array
        stepY = 0

        if rayDirX < 0:
            stepX = -1 # set the direction I am stepping in one axis
            sideDistX = (player.x - float(mapX)) * deltaDistX # manually calc dist from nearest left cell
        else:
            stepX = 1
            sideDistX = (float(mapX + 1.0) - player.x) * deltaDistX

        if rayDirY < 0:
            stepY = -1
            sideDistY = (player.y - float(mapY)) * deltaDistY
        else:
            stepY = 1
            sideDistY = (float(mapY + 1) - player.y) * deltaDistY

        hit = False # for breaking the loop
        dist = 0 # distance to calc from
        while hit != True:
            if sideDistX < sideDistY: # we increment based on the smallest sideDist so far
                sideDistX += deltaDistX # step along our ray (float precision walk)
                mapX += stepX # step through our map (approximate integer walk)
                dist = sideDistX # set our distance to the smallest of the two
                side = 0 # tell us if we hit a NS or EW wall
                #pygame.draw.circle(window, (0, 0, 255), [mapX * map.tileSize, mapY * map.tileSize], 5)
            else:
                sideDistY += deltaDistY
                mapY += stepY
                dist = sideDistY
                side = 1
                #pygame.draw.circle(window, (0, 0, 255), [mapX * map.tileSize, mapY * map.tileSize], 5)

            #print(mapX, ",", mapY)
            if mapX >= 0 and mapX < map.w and mapY >= 0 and mapY < map.h: # make sure that we are within our map
                if map.array[mapY][mapX] > 0: # did we hit a wall?
                    hit = True # Yes!

        if hit:
            dist -= deltaDistX if side == 0 else deltaDistY # subtract our extra step

            intersectionX = player.x + rayDirX * dist # calculate our intersection point (based on javid9x's implementation of DDA algorithm)
            intersectionY = player.y + rayDirY * dist

            pygame.draw.line(window, (0, 255, 0), [player.x * map.tileSize, player.y * map.tileSize], [intersectionX * map.tileSize, intersectionY * map.tileSize])

            height = min(screenH, int(screenH / float(dist * math.cos(angle - player.a)))) # cos gives the perp dist from "camera plane," instead of euclidean distance from player
            color = (255, 0, 0) if side == 1 else (200, 0, 0)
            pygame.draw.line(window, color, [screenW // 2 + x, screenH // 2 - height / 2], [screenW // 2 + x, screenH // 2 + height / 2])
            #pygame.draw.circle(window, (255, 255, 0), [intersectionX * map.tileSize, intersectionY * map.tileSize], 4)
            #pygame.draw.rect(window, (0, 255, 0), [(mapX) * map.tileSize, (mapY) * map.tileSize, map.tileSize - 1, map.tileSize - 1])

        # The following algorithm is called "ray marching." It is easier to read, but much slower

        #c = 0 #
        #while c <= 10:
        #    x = player.x + c * math.cos(angle)
        #    y = player.y + c * math.sin(angle)

        #    #if x < 0 or y < 0 or x > map.w or y > map.h: # If ray is out of range
        #    #    break
        #    #print(int(round(x)), ",", int(round(y)))
        #    if map.array[int(round(x)) - 1][int(round(y)) - 1] == 1:
        #        #print("Hit")
        #        dist = c * math.cos(angle - player.a) # correct the fisheye effect
        #        #dist = ((x - player.x)**2 + (y - player.y)**2)**0.5
        #        height = min(screenH, int(screenH / dist))
        #        pygame.draw.line(window, (255, 0, 0), [i, screenH / 2 - height / 2], [i, screenH / 2 + height / 2], 5)
        #        break
        #    c += 0.05 # march our ray

def drawMap(player, map, window):
    j = 0
    while j < len(map.array): # draw our map
        i = 0
        while i < len(map.array[j]):
            color = (255, 0, 0) if map.array[j][i] == 0 else (0, 0, 255) # change color on walls
            pygame.draw.rect(window, color, [i * map.tileSize, j * map.tileSize, map.tileSize - 1, map.tileSize - 1])
            i += 1
        j += 1
    pygame.draw.circle(window, (0, 255, 0), [player.x * map.tileSize, player.y * map.tileSize], 5) # draw player
    pygame.draw.line(window, (0, 255, 0), [player.x * map.tileSize, player.y * map.tileSize], [(player.x + 2 * math.cos(player.a)) * map.tileSize, (player.y + 2 * math.sin(player.a)) * map.tileSize ])

def main():
    pygame.init() # init pygame
    window = pygame.display.set_mode((screenW, screenH)) # set up display with defined width and height
    player = Player(8, 8, math.pi / 2.0 + 0.01) # create player object
    map = Map(r"map.csv")
    while True: # game loop
        handleInputs(player)
        window.fill((255, 255, 255))
        drawMap(player, map, window)
        render(player, map, window)
        #clear()
        #print("X:", player.x, "Y:", player.y, "A:", player.a)
        pygame.display.update()
    input()
    return
main()

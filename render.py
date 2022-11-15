import math
import pygame

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

def render(player, map, window, constants): # my implementation of lodev's DDA algorithm ()
    for x in range(0, constants['screenW'], 4): # I will draw slices in quantity equal to 1/4 of the screenW but 4px wide

        angle = player.a - constants['fovHalf'] + x * constants['fovInc']

        rayDirX = math.cos(angle) # get the unit vector for our angle
        rayDirY = math.sin(angle)

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
        while hit == False:
            if sideDistX < sideDistY: # we increment based on the smallest sideDist so far
                sideDistX += deltaDistX # step along our ray (float precision walk)
                mapX += stepX # step through our map (approximate integer walk)
                dist = sideDistX # set our distance to the smallest of the two
                side = 0 # tell us if we hit a NS or EW wall
            else:
                sideDistY += deltaDistY
                mapY += stepY
                dist = sideDistY
                side = 1

            if mapX >= 0 and mapX < map.w and mapY >= 0 and mapY < map.h: # make sure that we are within our map
                if map.array[mapY][mapX] > 0: # did we hit a wall?
                    hit = True # Yes!
            else: break
        if hit:
            dist -= deltaDistX if side == 0 else deltaDistY # subtract our extra step

            intersectionX = player.x + rayDirX * dist # calculate our intersection point (based on javid9x's implementation of DDA algorithm)
            intersectionY = player.y + rayDirY * dist

            height = int(constants['screenH'] / float(dist * math.cos(angle - player.a))) # cos gives the perp dist from "camera plane," instead of euclidean distance from player
            color = (255, 0, 0) if side == 1 else (220, 0, 0) # do some shading depending on whether we hit a NS or EW wall
            pygame.draw.line(window, color, [x, max(0, player.horizon - height / 2)], [x, min(constants['screenH'], player.horizon + height / 2)], 4) # draw our vertical slice
            for i in range(4):
                for j in range(height):
                    window.set_at(x, max(0, player.horizon - height / 2))
            #pygame.draw.line(window, (0, 255, 0), [player.x * map.tileSize, player.y * map.tileSize], [intersectionX * map.tileSize, intersectionY * map.tileSize])
            #pygame.draw.circle(window, (255, 255, 0), [intersectionX * map.tileSize, intersectionY * map.tileSize], 4)
            #pygame.draw.rect(window, (0, 255, 0), [(mapX) * map.tileSize, (mapY) * map.tileSize, map.tileSize - 1, map.tileSize - 1])
        pygame.draw.line(window, (255, 255, 255, 20), [constants['screenW'] / 2 - 8, constants['screenH'] / 2], [constants['screenW'] / 2 + 8, constants['screenH'] / 2], 2)# draw crosshair
        pygame.draw.line(window, (255, 255, 255, 20), [constants['screenW'] / 2, constants['screenH'] / 2 - 8], [constants['screenW'] / 2, constants['screenH'] / 2 + 8], 2)# draw crosshair

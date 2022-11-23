import pygame
import numpy as np

def render(player, map, window, wallTex, screenW, screenH, pxMult): # my implementation of lodev's DDA algorithm (https://lodev.org/cgtutor/raycasting.html)
    for x in range(0, screenW, 1): # I will draw slices in quantity equal to 1/4 of the screenW but 4px wide

        angle = player.a - player.fovHalf + x * player.fovInc
        #angle = player.a

        rayDirX = np.cos(angle) # get the unit vector for our angle
        rayDirY = np.sin(angle)

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
        texNum = 0
        while hit == False: # march our ray based on previous calculations
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
                texNum = int(map.array[mapX + mapY * map.w]) # get the number in the square to determine which texture we are using
                if texNum > 0: # did we hit a wall?
                    texNum = min(texNum - 1, wallTex.num - 1) # we want to start at 0 in our texture array, not 1 whole texture in; I use min to make a default for missing textures; Eg, texNum = 23, but there are 6 textures
                    hit = True # Yes!
            else: break
        if hit: # we hit a wall!
            dist -= deltaDistX if side == 0 else deltaDistY # subtract our extra step

            intersectionX = player.x + rayDirX * dist # calculate our intersection point (based on javid9x's implementation of DDA algorithm)
            intersectionY = player.y + rayDirY * dist

            height = int(screenH / float(dist * np.cos(angle - player.a))) # cos gives the perp dist from "camera plane," instead of euclidean distance from player (see lodev's example)
            #color = (255, 0, 0) if side == 1 else (220, 0, 0) # do some shading depending on whether we hit a NS or EW wall
            #pygame.draw.line(window, color, [x, max(0, player.horizon - height / 2)], [x, min(screenH, player.horizon + height / 2)], 4) # draw our vertical slice # how we used to do things

            # I got the following idea from ssloy's tinyracaster project (https://github.com/ssloy/tinyraycaster)
            textureX = (intersectionX - int(intersectionX)) * wallTex.h if side == 1 else (intersectionY - int(intersectionY)) * wallTex.h # determing where horizontally to sample from on our texture

            # The following part of the texture-mapping algorithm is all original!
            pxHeight = height / wallTex.h # check if height is larger than wallText.h. If so, draw rectangles that scale with this height instead of wasting time sampling the same pixels

            if pxHeight < 1:
                for j in range(height):
                    #window.set_at((x, int(player.horizon - height / 2) + j), int(wallTex.array[int(textureX) + int(j * (wallTex.h / height)) * wallTex.w]))
                    pygame.draw.rect(window, int(wallTex.array[(int(textureX) + texNum * wallTex.h) + int(j * (wallTex.h / height)) * wallTex.w]), [x * pxMult, (int(player.horizon - height / 2) + j) * pxMult, pxMult, pxMult]) # draw my slice
                #for j in range(int(height / 2)):
                #    pygame.draw.rect(window, int(wallTex.array[int(textureX) + int(j * (wallTex.h / height) * 2) * wallTex.w]), [x, int(player.horizon - height / 2) + j * 2, 2, 2]) # draw my slice
            else:
                for j in range(wallTex.h): # This bit, I do so that I do not waste my time sampling the same px again and again (like in ssloy's tinyraycaster)
                #for j in range(0, height, int(pxHeight)):
                    # adding 1 here concedes some redundancy but fixes a more jarring graphical bug
                    #pygame.draw.rect(window, int(wallTex.array[1]), [x * pxMult, (int(player.horizon - height / 2) + j * pxHeight) * pxMult, pxMult, pxMult * pxHeight + 1])
                    #pygame.draw.rect(window, int(wallTex.array[int(textureX) + texNum * wallTex.h + j * wallTex.w]), [x * pxMult, (int(player.horizon - height / 2) + j * pxHeight) * pxMult, pxMult, pxMult * pxHeight + 1])
                    pygame.draw.rect(window, int(wallTex.array[int(textureX) + texNum * wallTex.h + j * wallTex.w]), [x * pxMult, (int(player.horizon - height / 2) + j * pxHeight) * pxMult, pxMult, pxMult * pxHeight + 1])

        pygame.draw.line(window, (255, 255, 255, 20), [screenW - 8, screenH], [screenW + 8, screenH], 2)# draw crosshair
        pygame.draw.line(window, (255, 255, 255, 20), [screenW, screenH - 8], [screenW, screenH + 8], 2)# draw crosshair

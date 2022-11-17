import pygame
import numpy as np

class Texture():
    h = 0
    w = 0
    array = np.empty(1, dtype=int)
    def __init__(self, image):
        pxArray = pygame.PixelArray(image)
        self.array = np.ndarray(shape=(image.get_height() * image.get_width()))
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                self.array[x + y * image.get_width()] = int(pxArray[x, y]) # much faster to make a pixel array than to deal with pygame's "Surface" crap
        self.h = int(image.get_height())
        self.w = int(image.get_width())

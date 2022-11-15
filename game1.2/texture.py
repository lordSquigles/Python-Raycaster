import pygame

class Texture():
    pixMap = []
    h = 0
    w = 0
    array = []
    def __init__(self, image):
        pxArray = pygame.PixelArray(image)
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                self.array.append(pxArray[x, y]) # musch faster to make a pixel array than to deal with pygame's "Surface" crap
        self.h = int(image.get_height())
        self.w = int(image.get_width())
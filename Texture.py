import pygame

class Texture():
    def __init__(self, file):
        image = pygame.image.load(file)
        array = pygame.PixelArray(image)


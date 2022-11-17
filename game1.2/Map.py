import numpy as np
class Map:
    array = np.zeros(1, dtype=int)
    list = []
    w = 0
    h = 0
    tileSize = 0
    def __init__(self, file, screenH):
        mf = open(file, "r")
        mapFile = mf.read().split("\n")
        mapFile.pop(-1)

        self.h = len(mapFile) # width of 1st element
        self.w = len(mapFile[0].split(",")) # number of elements

        self.array = np.zeros(self.w * self.h) # re-create our map array at the proper length

        for j in range(self.h):
            row = mapFile[j].replace(" ", "").split(",")
            for i in range(len(row)):
                self.array[i + j * len(mapFile)] = row[i]
            #self.list.append([int(j) for j in i.replace(" ", "").split(",")])

        self.tileSize = screenH / len(self.array)
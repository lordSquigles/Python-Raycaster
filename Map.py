class Map:
    array = []
    w = 0
    h = 0
    tileSize = 0
    def __init__(self, file, screenH):
        mf = open(file, "r")
        mapFile = mf.read().split("\n")
        mapFile.pop(-1)

        for i in mapFile:
            self.array.append([int(j) for j in i.replace(" ", "").split(",")])

        self.w = len(self.array) # width of 1st element
        self.h = len(self.array[0])# number of elements

        self.tileSize = screenH / len(self.array)

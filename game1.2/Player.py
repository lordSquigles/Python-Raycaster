class Player: # create our player class
    x = 0
    y = 0
    a = 0 # the angle the player is facing
    fov = 3.141592653589 / 3
    fovHalf = 3.141592653589 / 6
    fovInc = 0

    forwards = 0
    sideways = 0
    turn = 0
    up = 0

    horizon = 0
    la = []
    stats = False
    def __init__(self, x, y, a, h, w):
        self.x = x
        self.y = y
        self.a = a 
        self.horizon = h / 2
        self.fovInc = self.fov / w
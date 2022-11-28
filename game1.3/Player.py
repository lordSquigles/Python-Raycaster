class Player: # create our player class
    x = 0
    y = 0
    z = 0
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
        self.z = h / 2
        self.a = a 
        self.horizon = self.z
        self.fovInc = self.fov / w

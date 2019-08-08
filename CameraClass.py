class CameraClass:
    def __init__(self, win):
        self.position = 0, 0
        self.width, self.height = win.get_size()
        self.ui = []
        self.posIsGood = True

    def updatePos(self, player, levelSize):
        x = player.rigidBody.position.x - self.width/2
        y = player.rigidBody.position.y - self.height/2
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + self.width > levelSize[0]:
            x = levelSize[0] - self.width
        if y + self.height > levelSize[1]:
            y = levelSize[1] - self.height
        self.position = x, y


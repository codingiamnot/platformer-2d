from PlayerClass import PlayerClass
from PlatformClass import verifOnScreen
import pymunk


class Level:
    def __init__(self, levelTouple):
        self.space = pymunk.Space()
        self.space.gravity = 0, 700
        # levelTouple[0] contains a list of platforms sorted after the y axis
        self.platforms = levelTouple[0]
        # levelTouple[1] contains the position (top left corner) of the player spawn
        self.player = PlayerClass(levelTouple[1][0], levelTouple[1][1], self.space, True)
        # levelTouple[2] contains the point of death from falling
        self.maxiY = levelTouple[2]
        self.beginActivated = 0
        self.endActivated = -1
        self.size = None

    def loadNeededPlatforms(self, camera):
        while True:
            try:
                self.platforms[self.endActivated + 1]
            except:
                break
            if verifOnScreen(self.platforms[self.endActivated + 1], (camera.position[0], camera.position[0] + camera.width)):
                self.endActivated += 1
                self.space.add(self.platforms[self.endActivated].rigidBody, self.platforms[self.endActivated].poly)
            else:
                break

    def deleteUnusedPlatforms(self, camera):
        while not verifOnScreen(self.platforms[self.beginActivated], (camera.position[0], camera.position[0] + camera.width)):
            self.space.delete(self.platforms[self.beginActivated].rigidBody, self.platforms[self.beginActivated].poly)
            self.beginActivated += 1

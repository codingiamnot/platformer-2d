import pymunk
import pygame

# x and y from top corner


class PlatformClass:
    def __init__(self, x, y, width, height, img):
        self.addedToSpace = False
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(img, (width, height))
        self.rigidBody = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rigidBody.position = x + width/2, y + height/2
        self.poly = pymunk.Poly.create_box(self.rigidBody, size=(width, height))
        self.poly.id = "ground"
        self.position = x, y
        self.poly.friction = 0.3


def verifOnScreen(platform, interval):
    return platform.position[0] + platform.width > interval[0] or platform.position[0] < interval[1]

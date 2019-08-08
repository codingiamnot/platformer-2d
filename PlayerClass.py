import pygame
import pymunk
import time
import ImageProccesing

# x and y from top corner


class PlayerClass:
    def __init__(self, x, y, space, addToSpace):
        self.char = pygame.image.load('images/animations/standing.png')
        self.char = ImageProccesing.getMinRect(self.char)
        self.currentImage = self.char
        self.x = x
        self.y = y
        self.width = self.char.get_size()[0]
        self.height = self.char.get_size()[1]
        self.isOnGround = True
        self.rigidBody = pymunk.Body(1, pymunk.inf, pymunk.Body.DYNAMIC)
        self.rigidBody.position = x + self.width/2, y + self.height/2
        self.poly = pymunk.Poly.create_box(self.rigidBody, size=self.char.get_size())
        self.poly.id = "player"
        self.feetSensor = pymunk.Circle(self.rigidBody, self.width/2, (0, self.height/2))
        self.feetSensor.sensor = True
        self.feetSensor.id = "player"
        if addToSpace:
            space.add(self.rigidBody, self.poly, self.feetSensor)
        self.poly.friction = 1
        self.vel = 31.2
        self.maxVel = 90
        self.isJumping = False
        self.right = False
        self.left = False
        self.runCount = 0
        self.walkRight = [pygame.image.load('images/animations/R1.png'), pygame.image.load('images/animations/R2.png'),
                          pygame.image.load('images/animations/R3.png'), pygame.image.load('images/animations/R4.png'),
                          pygame.image.load('images/animations/R5.png'), pygame.image.load('images/animations/R6.png'),
                          pygame.image.load('images/animations/R7.png'), pygame.image.load('images/animations/R8.png'),
                          pygame.image.load('images/animations/R9.png')]
        for par in range(len(self.walkRight)):
            self.walkRight[par] = ImageProccesing.getMinRect(self.walkRight[par])
        self.walkLeft = [pygame.image.load('images/animations/L1.png'), pygame.image.load('images/animations/L2.png'),
                         pygame.image.load('images/animations/L3.png'), pygame.image.load('images/animations/L4.png'),
                         pygame.image.load('images/animations/L5.png'), pygame.image.load('images/animations/L6.png'),
                         pygame.image.load('images/animations/L7.png'), pygame.image.load('images/animations/L8.png'),
                         pygame.image.load('images/animations/L9.png')]
        for par in range(len(self.walkLeft)):
            self.walkLeft[par] = ImageProccesing.getMinRect(self.walkLeft[par])
        self.time = time.time()
        self.timeLastUpdate = 0
        self.neg = 0
        self.jumpForce = 500

    def drawPlayer(self, win, camera):
        self.time = time.time()
        if self.isJumping:
            if self.right and not self.left:
                self.currentImage = self.walkRight[1]
            elif not self.right and self.left:
                self.currentImage = self.walkLeft[1]
            else:
                self.currentImage = self.char
        else:
            if not self.left and not self.right:
                if self.runCount > 0:
                    self.currentImage = self.walkRight[0]
                else:
                    self.currentImage = self.walkLeft[0]
            elif not self.left and self.right:
                if self.runCount < 0:
                    self.runCount = 0
                self.runCount += 1
                if self.runCount >= 10:
                    self.runCount = 1
                if self.time - self.timeLastUpdate > 1/10:
                    self.timeLastUpdate = self.time
                    self.currentImage = self.walkRight[self.runCount - 1]
            else:
                if self.runCount > 0:
                    self.runCount = 0
                self.runCount -= 1
                if self.runCount <= -10:
                    self.runCount = -1
                if self.time - self.timeLastUpdate > 1/10:
                    self.timeLastUpdate = self.time
                    self.currentImage = self.walkLeft[-1 * self.runCount - 1]
        self.x = self.rigidBody.position.x - self.currentImage.get_size()[0]/2
        self.y = self.rigidBody.position.y - self.currentImage.get_size()[1]/2
        win.blit(self.currentImage, (self.x - camera.position[0], self.y - camera.position[1]))

    def Control(self, keys):
        if not self.isJumping and keys[pygame.K_UP] and self.isOnGround:
            self.isJumping = True
            if self.right and not self.left:
                self.neg = 1
            elif not self.right and self.left:
                self.neg = -1
            else:
                self.neg = 0
            self.rigidBody.apply_impulse_at_local_point((self.neg * self.jumpForce/4, -self.jumpForce), (0, 0))
        if keys[pygame.K_LEFT]:
            self.rigidBody.apply_impulse_at_local_point((-self.vel, 0), (0, 0))
            if self.rigidBody.velocity.x < -self.maxVel:
                self.rigidBody.apply_impulse_at_local_point((self.vel, 0), (0, 0))
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT]:
            self.rigidBody.apply_impulse_at_local_point((self.vel, 0), (0, 0))
            if self.rigidBody.velocity.x > self.maxVel:
                self.rigidBody.apply_impulse_at_local_point((-self.vel, 0), (0, 0))
            self.left = False
            self.right = True
        elif not self.isJumping:
            self.left = False
            self.right = False

    def Physics(self):
        if self.isJumping and self.isOnGround and self.rigidBody.velocity.y > 0:
            self.isJumping = False

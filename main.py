import pygame
import time
import pymunk.pygame_util
from CameraClass import CameraClass
from LevelClass import Level
from ImageProccesing import LoadLevel


pygame.init()

windowWidth = 800
windowHeight = 500

win = pygame.display.set_mode((windowWidth, windowHeight))
camera = CameraClass(win)

pymunk.pygame_util.positive_y_is_up = False


bg = pygame.image.load('images/bg.jpg')
platformImg = pygame.image.load('images\platform.png')

pygame.display.set_caption("Game")

levelImg = pygame.image.load("images\levels\levelTest7.png")
level = Level(LoadLevel(levelImg, platformImg))
print(level.platforms)
print(level.player)


debugImage = pygame.Surface(levelImg.get_size())
options = pymunk.pygame_util.DrawOptions(debugImage)

run = True

clock = pygame.time.Clock()
fps = 0
timeFrame = time.time()



def coll_begin(arbitrer, space, data):
    for shape in arbitrer.shapes:
        if shape.id == "player" and shape.sensor:
            level.player.isOnGround = True
    return True


def coll_pre(arbitrer, space, data):
    return True


def coll_post(arbitrer, space, data):
    pass


def coll_separate(arbitrer, space, data):
    for shape in arbitrer.shapes:
        if shape.id == "player" and shape.sensor:
            level.player.isOnGround = False


handler = level.space.add_default_collision_handler()
handler.begin = coll_begin
handler.pre_solve = coll_pre
handler.post_solve = coll_post
handler.separate = coll_separate


def draw(bg):
    clock.tick()
    camera.updatePos(level.player, levelImg.get_size())
    bg = pygame.transform.scale(bg, (windowWidth, windowHeight))
    win.blit(bg, (0, 0))
    for platform in level.platforms:
        win.blit(platform.img, (platform.position[0] - camera.position[0], platform.position[1] - camera.position[1]))
    level.player.drawPlayer(win, camera)
    pygame.display.update()


def debugDraw(bg):
    clock.tick()
    camera.updatePos(level.player, levelImg.get_size())
    bg = pygame.transform.scale(bg, (windowWidth, windowHeight))
    debugImage.blit(bg, camera.position)
    level.space.debug_draw(options)
    debugCameraRect = pygame.Rect(camera.position[0], camera.position[1], camera.width, camera.height)
    win.blit(debugImage.subsurface(debugCameraRect), (0, 0))
    for platform in level.platforms:
        win.blit(platform.img, (platform.position[0] - camera.position[0], platform.position[1] - camera.position[1]))
    level.player.drawPlayer(win, camera)
    pygame.display.update()


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            run = False
    keys = pygame.key.get_pressed()

    level.loadNeededPlatforms(camera)
    level.deleteUnusedPlatforms(camera)

    level.player.Control(keys)
    level.player.Physics()

    level.space.step(0.02)

    draw(bg)
    # debugDraw(bg)

    fps = clock.get_fps()

    if level.player.rigidBody.position[1] + level.player.height/2 > level.maxiY + 100:
        print("You died!")
        run = False


pygame.quit()

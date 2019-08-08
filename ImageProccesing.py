import pygame.surfarray
from PlatformClass import PlatformClass
import numpy


def getMinRect(img):
    a = pygame.surfarray.array_alpha(img)
    n = img.get_size()[0]
    m = img.get_size()[1]
    imini = n
    jmini = m
    imaxi = 0
    jmaxi = 0
    for i in range(n):
        for j in range(m):
            if a[i, j]:
                if i > imaxi:
                    imaxi = i
                if j > jmaxi:
                    jmaxi = j
                if i < imini:
                    imini = i
                if j < jmini:
                    jmini = j
    width = imaxi-imini
    height = jmaxi-jmini
    x = imini
    y = jmini
    anwRect = pygame.Rect(x, y, width, height)
    return img.subsurface(anwRect)


def fill(x, y, a, n, m, b):
    maxiW = 0
    maxiH = 0
    i = x
    j = y
    while a[i, j] == a[x, y] and i < n-1:
        i += 1
    maxiW = i - x
    i = x
    j = y
    while a[i, j] == a[x, y] and j < m-1:
        j += 1
    maxiH = j-y
    for i in range(maxiW):
        for j in range(maxiH):
            b[i + x, j + y] = 1
    return maxiW, maxiH


def LoadLevel(img, platformImg):
    # green ground, red player spawn
    alpha = pygame.surfarray.array_alpha(img)
    color = pygame.surfarray.array2d(img)
    n, m = img.get_size()
    maxi = 0
    b = numpy.zeros(shape=(n, m))
    platforms = []
    playerSpawn = 0
    for i in range(n):
        for j in range(m):
            if alpha[i, j] and b[i, j] == 0:
                x = i
                y = j
                size = fill(x, y, color, n, m, b)
                if color[i, j] == -16711936:
                    # -16711936 equals RGB(0,255,0)
                    anwPlatform = PlatformClass(x, y, size[0], size[1], platformImg)
                    if y + size[1] > maxi:
                        maxi = y + size[1]
                    platforms.append(anwPlatform)
                if color[i, j] == -16776961:
                    # -16776961 equals RGB(255,0,0)
                    playerSpawn = x, y
    return platforms, playerSpawn, maxi

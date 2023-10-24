import os
import pygame

path = '/home/slikful/Desktop/Stuff/Just a Game'

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("2D Game")

walkRight = [pygame.image.load(f'{path}/utils/sprites/R1.png'), pygame.image.load(f'{path}/utils/sprites/R2.png'), pygame.image.load(f'{path}/utils/sprites/R3.png'),
             pygame.image.load(f'{path}/utils/sprites/R4.png'), pygame.image.load(f'{path}/utils/sprites/R5.png'), pygame.image.load(f'{path}/utils/sprites/R6.png'),
             pygame.image.load(f'{path}/utils/sprites/R7.png'), pygame.image.load(f'{path}/utils/sprites/R8.png'), pygame.image.load(f'{path}/utils/sprites/R9.png')]

walkLeft = [pygame.image.load(f'{path}/utils/sprites/L1.png'), pygame.image.load(f'{path}/utils/sprites/L2.png'), pygame.image.load(f'{path}/utils/sprites/L3.png'),
            pygame.image.load(f'{path}/utils/sprites/L4.png'), pygame.image.load(f'{path}/utils/sprites/L5.png'), pygame.image.load(f'{path}/utils/sprites/L6.png'),
            pygame.image.load(f'{path}/utils/sprites/L7.png'), pygame.image.load(f'{path}/utils/sprites/L8.png'), pygame.image.load(f'{path}/utils/sprites/L9.png')]

bg = pygame.image.load(f'{path}/utils/images/bg.jpg')
char = pygame.image.load(f'{path}/utils/sprites/standing.png')

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.Standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.Standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class Enemy:
    enemy_walkingRight = [pygame.image.load(f'{path}/utils/sprites/R1E.png'), pygame.image.load(f'{path}/utils/sprites/R2E.png'), pygame.image.load(f'{path}/utils/sprites/R3E.png'),
                          pygame.image.load(f'{path}/utils/sprites/R4E.png'), pygame.image.load(f'{path}/utils/sprites/R5E.png'), pygame.image.load(f'{path}/utils/sprites/R6E.png'),
                          pygame.image.load(f'{path}/utils/sprites/R7E.png'), pygame.image.load(f'{path}/utils/sprites/R8E.png'), pygame.image.load(f'{path}/utils/sprites/R9E.png'),
                          pygame.image.load(f'{path}/utils/sprites/R10E.png'), pygame.image.load(f'{path}/utils/sprites/R11E.png')]

    ememy_walkingLeft = [pygame.image.load(f'{path}/utils/sprites/L1E.png'), pygame.image.load(f'{path}/utils/sprites/L2E.png'), pygame.image.load(f'{path}/utils/sprites/L3E.png'),
                         pygame.image.load(f'{path}/utils/sprites/L4E.png'), pygame.image.load(f'{path}/utils/sprites/L5E.png'), pygame.image.load(f'{path}/utils/sprites/L6E.png'),
                         pygame.image.load(f'{path}/utils/sprites/L7E.png'), pygame.image.load(f'{path}/utils/sprites/L8E.png'), pygame.image.load(f'{path}/utils/sprites/L9E.png'),
                         pygame.image.load(f'{path}/utils/sprites/L10E.png'), pygame.image.load(f'{path}/utils/sprites/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]


class Amunition:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    def draw_amunition(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw_amunition(win)

    pygame.display.update()


# mainloop
man = Player(200, 410, 64, 64)
bullets = []
run = True
while run:
    clock.tick(27)  # This is the amount of pictures/frames displayed per second...

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:  # check to see the position of the bullet...
            bullet.x += bullet.vel

        else:
            # Delete the bullet from the bullets list if it goes off screen...
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            direction = -1
        else:
            direction = 1

        if len(bullets) < 5:
            bullets.append(
                Amunition(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), direction))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.Standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.Standing = False
    else:
        man.Standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()


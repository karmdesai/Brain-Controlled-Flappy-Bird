# import the required libraries
import os
import time
import pygame
import random

# list of images - transform regular images to be 2 times the original size
birdImages = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdUp.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdMiddle.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdDown.png")))]

groundImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "theGround.png")))
sceneImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "backgroundScene.png")))
pipeImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "marioPipe.png")))

# set the window width and height
windowWidth = 500
windowHeight = 800

class Bird:
    # controls how much the bird will tilt
    maxRotation = 25
    # how much we're going to rotate on each frame
    rotationVelocity = 20
    # how long each bird animation will be shown
    animationTime = 5

    def __init__(self, x, y):
        # represents the starting position of the bird
        self.x = x
        self.y = y
        # represents how much an image is tilted
        self.tilt = 0
        # used to figure out the phsyics of the bird
        self.tickCount = 0
        self.velocity = 0
        self.height = self.y
        # used to keep track of what image we're using
        self.imageCount = 0
        self.currentImage = birdImages[0]

    def flap(self):
        # negative velocity represents moving up in PyGame
        self.velocity = -10.5
        # used to represent when we last flapped - reset to 0 when this is called
        self.tickCount = 0
        self.height = self.y

    # using frames to move our bird
    def move(self):
        # we moved once more since the last jump, so add 1
        self.tickCount += 1
        # this equation tells us how much we're moving up or down
        d = (self.velocity * self.tickCount) + (1.5 * (self.tickCount ** 2))

        # foolproofing logic - if we're moving down more than 16, make 'd' equal to 16
        if d >= 16:
            d = 16
        # fine-tuning movement
        if d < 0:
            d -= 2

        # change y position depending on how much we're moving ('d')
        self.y = self.y + d

        # controls what the bird looks like when going up
        # when the bird goes up, it'll go up slightly
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.maxRotation:
                self.tilt = self.maxRotation
        # controls what the bird looks like when going down
        # when the bird goes down, it'll go down a lot (90 degrees)
        elif self.tilt > -90:
            self.tilt -= self.rotationVelocity

    # used to animate the bird
    def draw(self, window):
        # keep track of how many times we've shown an image
        self.imageCount += 1

        # use animationTime and imageCount to create a 'flapping' animation
        if self.imageCount < self.animationTime:
            self.currentImage = birdImages[0]
        elif self.imageCount < (self.animationTime * 2):
            self.currentImage = birdImages[1]
        elif self.imageCount < (self.animationTime * 3):
            self.currentImage = birdImages[2]
        elif self.imageCount < (self.animationTime * 4):
            self.currentImage = birdImages[1]
        elif self.imageCount < ((self.animationTime * 4) + 1):
            self.currentImage = birdImages[0]
            # reset imageCount
            self.imageCount = 0

        # avoid the bird from 'flapping' if it's going downwards
        if self.tilt <= -80:
            self.currentImage = birdImages[1]
            self.imageCount = self.animationTime * 2

        # rotate the flappy bird image about the center
        rotatedImage = pygame.transform.rotate(self.currentImage, self.tilt)
        newRectangle = rotatedImage.get_rect(center = self.currentImage.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotatedImage, newRectangle.topleft)

    def getMask(self):
        return pygame.mask.from_surface(self.currentImage)

# used to draw a window
def displayWindow(window, bird):
    window.blit(sceneImage, (0, 0))
    bird.draw(window)
    # update the display
    pygame.display.update()

def main():
    # create a new instance of the 'Bird' class and a new window
    flappyBird = Bird(200, 200)
    newWindow = pygame.display.set_mode((windowWidth, windowHeight))
    # use the clock to set the 'frame rate'
    clock = pygame.time.Clock()

    # set gameRun to True (so the while loop runs)
    gameRun = True
    while gameRun:
        # have at most 30 ticks every second
        clock.tick(30)
        for event in pygame.event.get():
            # if the window is closed
            if event.type == pygame.QUIT:
                # the game should stop running
                gameRun = False
        # move the bird every time the while loop is executed
        flappyBird.move()
        displayWindow(newWindow, flappyBird)
    pygame.quit()
    quit()

main()
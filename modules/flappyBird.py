# import the required libraries
import os
import time
import pygame
import random

class Bird:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (50, 50)
    
    windowWidth = 375
    windowHeight = 600

    """ Set window location and initialize pyGame
    Also, set the screen size (when the bird is created)

    This is inefficient because we're calling it twice
    (once in the main loop and once here), but is somehow
    makes the game less choppy """

    pygame.init()
    pygame.display.set_mode((50, 50))
    newWindow = pygame.display.set_mode((windowWidth, windowHeight))
    
    # controls how much the bird will tilt
    maxRotation = 19
    # how much we're going to rotate on each frame
    rotationVelocity = 15
    # how long each bird animation will be shown
    animationTime = 5

    # list of images - transform regular images to be 1.5 times the original size
    birdImages = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdUp.png")).convert(), (51, 36)), 
                pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdMiddle.png")).convert(), (51, 36)),
                pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdDown.png")).convert(), (51, 36))]

    def __init__(self, x, y):
        # represents the starting position of the bird
        self.x = x
        self.y = y

        # represents how much an image is tilted
        self.tilt = 0

        # used to figure out the phsyics of the bird
        self.tickCount = 0
        self.velocity = 0
        self.height = y

        # used to keep track of what image we're using
        self.imageCount = 0
        self.currentImage = self.birdImages[0]

        # Initialize PyGame
        pygame.init()
        pygame.display.set_mode((50, 50))
        pygame.display.set_caption('Brain-Controlled Flappy Bird')

    def flap(self):
        # negative velocity represents moving up in PyGame
        self.velocity = -7.875

        # used to represent when we last flapped - reset to 0 when this is called
        self.tickCount = 0
        self.height = self.y

    # using frames to move our bird
    def move(self):
        # we moved once more since the last jump, so add 1
        self.tickCount += 1
        # this equation tells us how much we're moving up or down
        d = (self.velocity * self.tickCount) + (1.125 * (self.tickCount ** 2))

        # foolproofing logic - if we're moving down more than 12, make 'd' equal to 16
        if d >= 12:
            d = 12
        # fine-tuning movement
        if d < 0:
            d -= 1.5

        # change y position depending on how much we're moving ('d')
        self.y = self.y + d

        # controls what the bird looks like when going up
        # when the bird goes up, it'll go up slightly
        if d < 0 or self.y < self.height + 38:
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
            self.currentImage = self.birdImages[0]
        elif self.imageCount < (self.animationTime * 2):
            self.currentImage = self.birdImages[1]
        elif self.imageCount < (self.animationTime * 3):
            self.currentImage = self.birdImages[2]
        elif self.imageCount < (self.animationTime * 4):
            self.currentImage = self.birdImages[1]
        elif self.imageCount < ((self.animationTime * 4) + 1):
            self.currentImage = self.birdImages[0]
            # reset imageCount
            self.imageCount = 0

        # avoid the bird from 'flapping' if it's going downwards
        if self.tilt <= -80:
            self.currentImage = self.birdImages[1]
            self.imageCount = self.animationTime * 2

        # rotate the flappy bird image about the center
        rotatedImage = pygame.transform.rotate(self.currentImage, self.tilt)
        newRectangle = rotatedImage.get_rect(center = self.currentImage.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotatedImage, newRectangle.topleft)

    def getMask(self):
        # gets us the mask for the current image (used for collisions)
        return pygame.mask.from_surface(self.currentImage)

class Pipe:
    # the amount of space between two pipes
    pipeGap = 225
    # velocity (represents how fast the pipes will move)
    velocity = 4

    pipeImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "marioPipe.png")).convert(), (78, 480))

    # don't need a 'y' for pipe since height will be randomized
    def __init__(self, x):
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe will be
        self.top = 0
        self.bottom = 0

        # this version of the pipe image will be flipped (so it can be used at the top)
        self.pipeTop = pygame.transform.flip(self.pipeImage, False, True)
        self.pipeBottom = self.pipeImage

        # keep track of whether the bird passed the pipe or not
        self.pipePassed = False
        self.setHeight()

    # randomly sets the top, bottom, and height of a pipe
    def setHeight(self):
        self.height = random.randrange(38, 338)
        self.top = self.height - self.pipeTop.get_height()
        self.bottom = self.height + self.pipeGap

    def move(self):
        # just move the pipe more left every frame
        self.x -= self.velocity

    def draw(self, window):
        # draw the top of the pipe at (x, top)
        window.blit(self.pipeTop, (self.x, self.top))
        # draw the bottom of the pipe at (x, bottom)
        window.blit(self.pipeBottom, (self.x, self.bottom))

    # use masks (basically a 2D list of pixels) for collisions
    def collide(self, bird):
        # get the mask for the bird
        birdMask = bird.getMask()
        # get the mask for the top/bottom pipes
        topMask = pygame.mask.from_surface(self.pipeTop)
        bottomMask = pygame.mask.from_surface(self.pipeBottom)

        # calculate offsets - how far the masks are from each other
        # offset from the bird to the top mask
        topOffset = (self.x - bird.x, self.top - round(bird.y))
        # offset from the bird to the bottom mask
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y))

        # finds the point of overlap between the bird mask and the top pipe
        topPoint = birdMask.overlap(topMask, topOffset)
        # finds the point of overlap between the bird mask and the bottom pipe
        bottomPoint = birdMask.overlap(bottomMask, bottomOffset)

        # if these points have a value other than 'None'
        if topPoint or bottomPoint:
            # return True to symbolize collision
            return True

        # return False to symbolize non-collision
        return False

class Ground:
    # the velocity should be the same as the pipe
    velocity = 4
    groundImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "theGround.png")).convert(), (504, 168))
    groundWidth = groundImage.get_width()

    # 'x' doesn't need to be defined since it'll be moving to the left
    def __init__(self, y):
        self.y = y
        # two panels - used to create an infinite movement animation
        self.x1 = 0
        self.x2 = self.groundWidth

    def move(self):
        # move each panel to the left
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        # if the first panel has reached the end, move it behind the second
        if (self.x1 + self.groundWidth) < 0:
            self.x1 = self.x2 + self.groundWidth

        # if the second panel has reached the end, move it behind the first
        if (self.x2 + self.groundWidth) < 0:
            self.x2 = self.x1 + self.groundWidth

    def draw(self, window):
        # draw both the panels so we have a ground
        window.blit(self.groundImage, (self.x1, self.y))
        window.blit(self.groundImage, (self.x2, self.y))
# import the required libraries
import os
import time
import pygame
import random

# Set window location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (50, 50)

# Initialize PyGame
pygame.init()
pygame.display.set_mode((50, 50))
pygame.display.set_caption('Flappy Brain')

# list of images - transform regular images to be 1.5 times the original size
birdImages = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdUp.png")), (51, 36)), 
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdMiddle.png")), (51, 36)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "birdDown.png")), (51, 36))]

groundImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "theGround.png")), (504, 168))
sceneImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "backgroundScene.png")), (432, 768))
pipeImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "marioPipe.png")), (78, 480))

# set the window width and height
windowWidth = 375
windowHeight = 600

# fonts
statFont = pygame.font.SysFont("Didot", 75)

class Bird:
    # controls how much the bird will tilt
    maxRotation = 19
    # how much we're going to rotate on each frame
    rotationVelocity = 15
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
        # gets us the mask for the current image (used for collisions)
        return pygame.mask.from_surface(self.currentImage)

class Pipe:
    # the amount of space between two pipes
    pipeGap = 225
    # velocity (represents how fast the pipes will move)
    velocity = 4

    # don't need a 'y' for pipe since height will be randomized
    def __init__(self, x):
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe will be
        self.top = 0
        self.bottom = 0

        # this version of the pipe image will be flipped (so it can be used at the top)
        self.pipeTop = pygame.transform.flip(pipeImage, False, True)
        self.pipeBottom = pipeImage

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
        window.blit(groundImage, (self.x1, self.y))
        window.blit(groundImage, (self.x2, self.y))

# used to draw a window
def displayWindow(window, bird, pipes, ground, score):
    window.blit(sceneImage, (0, 0))

    # draw each pipe in the list of pipes
    for pipe in pipes:
        pipe.draw(window)

    # dispay the score
    text = statFont.render(str(score), 1, (255, 255, 255))
    window.blit(text, (windowWidth - 10 - text.get_width(), 10))

    # draw the bird and the ground
    ground.draw(window)
    bird.draw(window)

    # update the display
    pygame.display.update()

def main():
    userScore = 0

    # draw the ground and pipes
    pipes = [Pipe(525)]
    ground = Ground(547)

    # create a new instance of the 'Bird' class and a new window
    flappyBird = Bird(173, 262)
    newWindow = pygame.display.set_mode((windowWidth, windowHeight))
    # use the clock to set the 'frame rate'
    clock = pygame.time.Clock()

    # set gameRun to True (so the while loop runs)
    gameRun = True

    while gameRun:
        
        # have at most 30 ticks every second
        clock.tick(30)
        for event in pygame.event.get():
            try:
                # if the window is closed
                if event.type == pygame.QUIT:
                    # then stop the game
                    gameRun = False

                # if the 'q' is pressed
                if event.key == pygame.K_q:
                    # then stop the game
                    gameRun = False

                if event.type == pygame.KEYUP:
                    flappyBird.flap()

            except:
                pass
        
        # make it look like the bird is moving (it's actually the ground moving)
        ground.move()
        # get the Mario pipes moving and check for collision
        removePipes = []
        addPipe = False

        for pipe in pipes:

            # if the bird hits a pipe, restart the main loop
            if pipe.collide(flappyBird):
                time.sleep(0.75)
                main()

            # if the pipe is off the screen, remove it
            if (pipe.x + pipe.pipeTop.get_width()) < 0:
                removePipes.append(pipe)

            # when the bird passes a pipe, generate a new one
            if not pipe.pipePassed and (pipe.x < flappyBird.x):
                pipe.pipePassed = True
                addPipe = True

            pipe.move()

        # add a new pipe and increase score by 1
        if addPipe == True:
            userScore += 1
            pipes.append(Pipe(525))

        for oldPipe in removePipes:
            pipes.remove(oldPipe)

        # if the bird hits the ground, restart the main loop
        if (flappyBird.y + flappyBird.currentImage.get_height()) >= 547:
            time.sleep(1)
            main()

        # if the bird hits the top, restart the main loop
        elif (flappyBird.y) <= 0:
            time.sleep(1)
            main()

        # move the bird every time the while loop is executed
        flappyBird.move()
        displayWindow(newWindow, flappyBird, pipes, ground, userScore)

    pygame.quit()
    quit()

main()
# import the required libraries
import os
import sys
import time
import pygame
import random

# import custom modules that I created
from modules.customSocket import newSocket
from modules.flappyBird import Ground, Pipe, Bird

# set window location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (50, 50)

# background image
sceneImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "backgroundScene.png")).convert(), (432, 768))

# fonts
statFont = pygame.font.SysFont("Didot", 75)

# create a new instance of the 'newSocket' class
s = newSocket(sys.argv[1], int(sys.argv[2]))

# used to draw a window
def displayWindow(window, bird, pipes, ground, score):
    window.blit(sceneImage, (0, 0))

    # draw each pipe in the list of pipes
    for pipe in pipes:
        pipe.draw(window)

    # dispay the score
    text = statFont.render(str(score), 1, (255, 255, 255))
    window.blit(text, (bird.windowWidth - 10 - text.get_width(), 10))

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
    newBird = Bird(173, 262)
    newWindow = pygame.display.set_mode((newBird.windowWidth, newBird.windowHeight))
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

            except:
                pass
        
        # make it look like the bird is moving (it's actually the ground moving)
        ground.move()
        # get the Mario pipes moving and check for collision
        removePipes = []
        addPipe = False

        for pipe in pipes:

            # if the bird hits a pipe, restart the main loop
            if pipe.collide(newBird):
                time.sleep(0.75)
                main()

            # if the pipe is off the screen, remove it
            if (pipe.x + pipe.pipeTop.get_width()) < 0:
                removePipes.append(pipe)

            # when the bird passes a pipe, generate a new one
            if not pipe.pipePassed and (pipe.x < newBird.x):
                pipe.pipePassed = True
                addPipe = True

            pipe.move()
        
        output = s.eegWave()

        if output == 1:
            newBird.flap()

        # add a new pipe and increase score by 1
        if addPipe == True:
            userScore += 1
            pipes.append(Pipe(525))

        for oldPipe in removePipes:
            pipes.remove(oldPipe)

        # if the bird hits the ground, restart the main loop
        if (newBird.y + newBird.currentImage.get_height()) >= 547:
            time.sleep(1)
            main()

        # if the bird hits the top, restart the main loop
        elif (newBird.y) <= 0:
            time.sleep(1)
            main()

        # move the bird every time the while loop is executed
        newBird.move()
        displayWindow(newWindow, newBird, pipes, ground, userScore)

    pygame.quit()
    quit()

main()
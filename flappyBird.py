# import the required libraries
import os
import time
import pygame
import random

# set the window width and height
windowWidth = 600
windowHeight = 800

# list of images - transform regular images to be 2 times the original size
birdImages = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdUp.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdMiddle.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "birdDown.png")))]

groundImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "theGround.png")))
sceneImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "backgroundScene.png")))
pipeImage = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "images", "marioPipe.png")))
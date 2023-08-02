from random import random, Random

import pygame

# window attributes
screen_width = 700
screen_height = 500
background = (255, 255, 255)

# player class
class Player:
    def __init__(self):
        self.x = 10
        self.y = screen_height - 20
        self.delta_y = 0
        self.gravity = 1
        self.delta_x = 5
        self.color = (255, 0, 0)
        self.speed = 2

    def jump(self):
        if self.y == 440:
            self.delta_y = 18

    def move_forward(self):
        self.x += self.delta_x

    def update(self):

        self.x += self.speed
        if 0 < self.delta_y or self.y < screen_height:
            self.y -= self.delta_y
            self.delta_y -= self.gravity

        if self.y > 440:
            self.y = 440

        if self.x < 10:
            self.x = 10

        if self.x > screen_width:
            self.x = 10

# starting out the window
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Infinite Runner")
fps = 50
timer = pygame.time.Clock()

player = Player()  # Create the player instance
isRunning = True


while isRunning:
    timer.tick(fps)
    screen.fill(background)
    floor = pygame.draw.rect(screen, (0, 0, 0), [2, screen_height - 37.5, screen_width, 5])
    player_rect = pygame.draw.rect(screen, player.color, [player.x, player.y, 20, 20])


    # checking the events during the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    player.update()

    # updating the display
    pygame.display.flip()

pygame.quit()

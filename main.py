import time
import random

import pygame

# window attributes
screen_width = 700
screen_height = 500
background = (255, 255, 255)

obs_color = (255, 0, 0)

# player class
class Player:
    def __init__(self):
        self.x = 10
        self.y = screen_height - 20
        self.delta_y = 0
        self.gravity = 2
        self.delta_x = 5
        self.color = (255, 0, 0)
        self.speed = 2

    def jump(self):
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


def generate_random_list():
    first = random.randint(10, screen_width)
    time.sleep(2);
    second = random.randint(10, screen_width)
    time.sleep(2);
    third = random.randint(10, screen_width)
    return [first, second, third]

# starting out the window
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Infinite Runner")
fps = 50
timer = pygame.time.Clock()

player = Player()  # Create the player instance
isRunning = True

# obstacles
obstacle_set1 = [50, 100, 300, 400, 500]
obstacle_set2 = [150, 250, 315, 470, 650]
obstacle_set3 = [200, 256, 325, 576, 650]
obstacle_speed = 1
active = True

def select_difficulty():
    choice = random.randint(1,3)
    if (choice ==1):
        return obstacle_set1
    elif choice == 2:
        return  obstacle_set2
    return obstacle_set3

obstacles = obstacle_set1
# colors for obstacles
colors = [(0, 0, 0), (113, 171, 27), (255, 153, 255)]

while isRunning:
    timer.tick(fps)
    screen.fill(background)
    floor = pygame.draw.rect(screen, (0, 0, 0), [2, screen_height - 37.5, screen_width, 5])
    player_rect = pygame.draw.rect(screen, player.color, [player.x, player.y, 25, 25])


    # checking the events during the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                obstacles = select_difficulty() # generate a method to get random difficulty levels
                player.jump()

    for i in range(len(obstacles)):
        colorindex = random.randint(0,2)
        pygame.draw.rect(screen, colors[colorindex], [obstacles[i], screen_height - 62.5, 30, 30])

    for i in range(len(obstacles)):
        if active:
            obstacles[i] -= obstacle_speed

        if obstacles[i] < -10:
            obstacles[i] = random.randint(600, 700)


    player.update()


    # updating the display
    pygame.display.flip()

pygame.quit()

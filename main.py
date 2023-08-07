import time
import random

import cv2
import pygame

from detector import PalmDetector

# window attributes
screen_width = 700
screen_height = 500
background = (0, 0, 0 )

obs_color = (255, 0, 0)


# player class
class Player:
    def __init__(self):
        self.x = 10
        self.y = screen_height - 20
        self.delta_y = 0
        self.gravity = 3
        self.delta_x = 5
        self.color = (255, 0, 0)
        self.speed = 2
        self.score = 0
        self.high_score = 0

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

    def update_high_score(self):
        if self.high_score > self.score:
            self.high_score = self.score


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# starting out the window
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Infinite Runner")
fps = 60
timer = pygame.time.Clock()

player = Player()  # Create the player instance
# player_image = pygame.image.load("images/gregor_final.png")

bg = pygame.image.load("images/bg.jpg")

# obstacles
obstacle_set1 = [50, 100, 300, 400, 500]
obstacle_set2 = [150, 250, 315, 470, 650]
obstacle_set3 = [200, 256, 325, 576, 650]
obstacle_speed = 3
active = True

def select_difficulty():
    choice = random.randint(1, 3)
    if choice == 1:
        return obstacle_set1
    elif choice == 2:
        return obstacle_set2
    return obstacle_set3


# this is a list of obstacle objects
# obstacles = [Obstacle(x, screen_height - 62.5, 30, 30) for x in obstacle_set1]
obstacles =[]

# colors for obstacles
colors = [(0, 0, 0), (113, 171, 27), (255, 153, 255)]
# take user input before starting the game
isRunning = False
takeString = input("Start the game: ")
if takeString in 'yY':
    isRunning = True
# wait for three seconds before the game starts
time.sleep(3)


# Starting with handDetection

cap = cv2.VideoCapture(0)
finger_detector = PalmDetector()
hasStarted = False
# start the loop
while isRunning:

    # read the frame and show it
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)

    # starting the game loop
    timer.tick(fps)
    screen.fill(background)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not hasStarted:
                    obstacles = [Obstacle(x, screen_height - 62.5, 30, 30) for x in [500, 700]]
                    hasStarted = True
                else:
                    obstacles = [Obstacle(x, screen_height - 62.5, 30, 30) for x in select_difficulty()]
                player.jump()

    if finger_detector.is_palm_extended(frame):
        if not hasStarted:
            obstacles = [Obstacle(x, screen_height - 62.5, 30, 30) for x in [500, 700]]
            hasStarted = True
        else:
            obstacles = [Obstacle(x, screen_height - 62.5, 30, 30) for x in select_difficulty()]
        player.jump()

    player_rect = pygame.draw.rect(screen, player.color, [player.x, player.y, 25, 25])

    for i in range(len(obstacles)):
        color_index = random.randint(0, 2)
        curr_obstacle = obstacles[i]
        obstacle = pygame.draw.rect(screen, colors[color_index],
                                    [curr_obstacle.x, curr_obstacle.y, curr_obstacle.width, curr_obstacle.height])

        # checking for collisions
        if player_rect.colliderect(obstacle):
            isRunning = False
        else:
            player.score += 1

    for i in range(len(obstacles)):
        if active:
            obstacles[i].x -= obstacle_speed

        if obstacles[i].x < -10:
            obstacles[i].x = random.randint(600, 700)

    player.update()
    pygame.display.flip()


cap.release()
cv2.destroyAllWindows()

pygame.quit()

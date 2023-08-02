import black as black
import pygame

# window attributes
screen_width = 700
screen_height = 500
background = (255, 255, 255)

# player attributes

player_x = 50
player_y = 200
delta_y = 0
gravity = 1

# starting out the window
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Infinite Runner")
fps = 50
timer = pygame.time.Clock()

isRunning = True
while isRunning:
    timer.tick(fps)
    screen.fill(background)

    # checking the events occuring during the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and delta_y ==0:
                delta_y = 18

    # updating the player's position

    # updating the display
    pygame.display.flip()




pygame.quit()


import pygame

# window attributes
screen_width = 700
screen_height = 500
background = (255, 255, 255)

# player attributes
player_x = 50
player_y = 440
delta_y = 0
gravity = 1
score = 0
player_color = (255, 0, 0)

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
    floor = pygame.draw.rect(screen, (0, 0, 0), [2, 440, screen_width, 5])
    player = pygame.draw.rect(screen, player_color, [player_x, player_y, 10, 20])
    # checking the events during the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y == 440:
                delta_y = 15

                # ensuring that the player stays in the bounds
    if 0 < delta_y or player_y < screen_height:
        player_y -= delta_y
        delta_y -= gravity

    if player_y > 440:
        player_y = 440

    # ensuring the player's x coordinate

    # updating the display
    pygame.display.flip()

pygame.quit()

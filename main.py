import pygame

# window attributes
screen_width = 700
screen_height = 500
background = (255, 255, 255)

# player class
class Player:
    def __init__(self):
        self.x = 50
        self.y = 440
        self.delta_y = 0
        self.gravity = 1
        self.color = (255, 0, 0)

    def jump(self):
        if self.y == 440:  # Check if player is on the floor to jump
            self.delta_y = 15  # Adjust the jump strength as per your requirement

    def update(self):
        if 0 < self.delta_y or self.y < screen_height:
            self.y -= self.delta_y
            self.delta_y -= self.gravity

        if self.y > 440:  # Check if player has reached the floor
            self.y = 440

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
    floor = pygame.draw.rect(screen, (0, 0, 0), [2, 440, screen_width, 5])
    player_rect = pygame.draw.rect(screen, player.color, [player.x, player.y, 10, 20])

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

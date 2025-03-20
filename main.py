import time
import random
import math
import cv2
import pygame
from pygame import mixer
from detector import PalmDetector

# window attributes
screen_width = 800
screen_height = 600
background = (135, 206, 235)  # Sky blue background

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)

class Player:
    def __init__(self):
        self.x = 100
        self.y = screen_height - 100
        self.delta_y = 0
        self.gravity = 2.5
        self.delta_x = 5
        self.color = (255, 0, 0)
        self.speed = 2
        self.score = 0
        self.high_score = 0
        self.jumping = False
        # Load and scale player sprite
        self.sprite = pygame.image.load("images/player.png")
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))
        self.jump_sound = pygame.mixer.Sound('music/jump.wav')
        self.jump_particles = []

    def jump(self):
        if not self.jumping:
            self.delta_y = 20
            self.jumping = True
            self.jump_sound.play()
            # Add jump particles
            for _ in range(10):
                self.jump_particles.append({
                    'x': self.x + 30,
                    'y': self.y + 60,
                    'dx': random.uniform(-2, 2),
                    'dy': random.uniform(-5, 0),
                    'lifetime': 20
                })

    def update(self):
        self.x += self.speed
        if self.delta_y != 0 or self.y < screen_height - 100:
            self.y -= self.delta_y
            self.delta_y -= self.gravity

        if self.y > screen_height - 100:
            self.y = screen_height - 100
            self.jumping = False
            self.delta_y = 0

        if self.x < 100:
            self.x = 100

        if self.x > screen_width - 100:
            self.x = 100

        # Update particles
        for particle in self.jump_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.jump_particles.remove(particle)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        # Draw particles
        for particle in self.jump_particles:
            pygame.draw.circle(screen, WHITE, 
                             (int(particle['x']), int(particle['y'])), 
                             2)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = random.choice([(255, 100, 100), (100, 255, 100), (100, 100, 255)])
        self.animation_offset = random.randint(0, 360)
        
    def draw(self, screen, time):
        # Animated obstacle
        offset = math.sin(time * 0.1 + self.animation_offset) * 5
        pygame.draw.rect(screen, self.color, 
                        [self.x, self.y + offset, self.width, self.height])
        # Glow effect
        glow_surf = pygame.Surface((self.width + 10, self.height + 10))
        pygame.draw.rect(glow_surf, (*self.color, 128), 
                        [0, 0, self.width + 10, self.height + 10])
        screen.blit(glow_surf, (self.x - 5, self.y + offset - 5), 
                   special_flags=pygame.BLEND_ALPHA_SDL2)

# Initialize Pygame and create window
pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Infinite Runner")
fps = 60
timer = pygame.time.Clock()

# Load and scale background images for parallax effect
bg_far = pygame.image.load("images/bg_far.png").convert_alpha()
bg_far = pygame.transform.scale(bg_far, (screen_width, screen_height))
bg_mid = pygame.image.load("images/bg_mid.png").convert_alpha()
bg_mid = pygame.transform.scale(bg_mid, (screen_width, screen_height))
bg_near = pygame.image.load("images/bg_near.png").convert_alpha()
bg_near = pygame.transform.scale(bg_near, (screen_width, screen_height))

bg_x_far = 0
bg_x_mid = 0
bg_x_near = 0

player = Player()
obstacles = []
obstacle_speed = 5
active = True

# Font for score display
font = pygame.font.Font(None, 36)

def draw_score(screen, score, high_score):
    score_text = font.render(f'Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

def draw_background():
    global bg_x_far, bg_x_mid, bg_x_near
    
    # Far background (slowest)
    screen.blit(bg_far, (bg_x_far, 0))
    screen.blit(bg_far, (bg_x_far + screen_width, 0))
    bg_x_far -= 0.5
    if bg_x_far <= -screen_width:
        bg_x_far = 0
        
    # Middle background
    screen.blit(bg_mid, (bg_x_mid, 0))
    screen.blit(bg_mid, (bg_x_mid + screen_width, 0))
    bg_x_mid -= 1
    if bg_x_mid <= -screen_width:
        bg_x_mid = 0
        
    # Near background (fastest)
    screen.blit(bg_near, (bg_x_near, 0))
    screen.blit(bg_near, (bg_x_near + screen_width, 0))
    bg_x_near -= 2
    if bg_x_near <= -screen_width:
        bg_x_near = 0

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

# starting the background music
mixer.init()
mixer.music.load('music/gigachad.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)  # -1 means loop indefinitely

game_time = 0
# start the loop
while isRunning:
    game_time += 1
    
    # read the frame and show it
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)

    # starting the game loop
    timer.tick(fps)
    
    # Draw parallax background
    draw_background()

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

    # Draw player
    player.draw(screen)

    # Draw obstacles with animation
    for obstacle in obstacles:
        obstacle.draw(screen, game_time)
        if active:
            obstacle.x -= obstacle_speed
        if obstacle.x < -50:
            obstacle.x = random.randint(screen_width, screen_width + 100)
            player.score += 10  # Increase score when passing obstacles

    # Check collisions
    player_rect = pygame.Rect(player.x + 10, player.y + 10, 40, 40)  # Smaller collision box than sprite
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        if player_rect.colliderect(obstacle_rect):
            # Collision effect
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 5)
                player.jump_particles.append({
                    'x': player.x + 30,
                    'y': player.y + 30,
                    'dx': math.cos(angle) * speed,
                    'dy': math.sin(angle) * speed,
                    'lifetime': 30
                })
            if player.score > player.high_score:
                player.high_score = player.score
            isRunning = False

    player.update()
    
    # Draw score
    draw_score(screen, player.score, player.high_score)
    
    pygame.display.flip()

# Game over screen
screen.fill(background)
game_over_text = font.render('Game Over!', True, WHITE)
final_score_text = font.render(f'Final Score: {player.score}', True, WHITE)
high_score_text = font.render(f'High Score: {player.high_score}', True, WHITE)
restart_text = font.render('Press SPACE to restart', True, WHITE)

screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 - 60))
screen.blit(final_score_text, (screen_width//2 - final_score_text.get_width()//2, screen_height//2))
screen.blit(high_score_text, (screen_width//2 - high_score_text.get_width()//2, screen_height//2 + 40))
screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 80))

pygame.display.flip()
time.sleep(2)  # Show game over screen for 2 seconds

cap.release()
cv2.destroyAllWindows()
pygame.quit()

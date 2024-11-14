import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Paddle and Puck settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PUCK_RADIUS = 15
PUCK_SPEED = 7

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('4-Way Air Hockey')

# Fonts
font = pygame.font.Font(None, 36)

# Player control settings
controls = {
    '2_players': {
        'top': [pygame.K_w, pygame.K_s],  # Top player controls (Up/Down)
        'bottom': [pygame.K_UP, pygame.K_DOWN],  # Bottom player controls (Up/Down)
    },
    '4_players': {
        'top': pygame.K_w,  # Top player
        'bottom': pygame.K_s,  # Bottom player
        'left': pygame.K_a,  # Left player
        'right': pygame.K_d  # Right player
    }
}


class Paddle:
    def __init__(self, x, y, width, height, player_num):
        self.rect = pygame.Rect(x, y, width, height)  # Paddle dimensions
        self.color = (255, 255, 255)
        self.player_num = player_num  # Player number to determine control
        self.speed = 5

    def move(self, keys):
        # Custom control based on player number
        if self.player_num == 1:  # Bottom player
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
        elif self.player_num == 2:  # Top player
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
        elif self.player_num == 3:  # Left player
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
        elif self.player_num == 4:  # Right player
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed



class Puck:
    def __init__(self, x, y, radius, color):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = color
        self.dx = random.choice([PUCK_SPEED, -PUCK_SPEED])
        self.dy = random.choice([PUCK_SPEED, -PUCK_SPEED])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dx = random.choice([PUCK_SPEED, -PUCK_SPEED])
        self.dy = random.choice([PUCK_SPEED, -PUCK_SPEED])


def handle_collisions(puck, paddles):
    if puck.rect.left <= 0 or puck.rect.right >= SCREEN_WIDTH:
        puck.dx = -puck.dx
    if puck.rect.top <= 0 or puck.rect.bottom >= SCREEN_HEIGHT:
        puck.dy = -puck.dy

    for paddle in paddles:
        if puck.rect.colliderect(paddle.rect):
            if abs(puck.rect.bottom - paddle.rect.top) < 10 and puck.dy > 0:
                puck.dy = -PUCK_SPEED
            elif abs(puck.rect.top - paddle.rect.bottom) < 10 and puck.dy < 0:
                puck.dy = PUCK_SPEED
            elif abs(puck.rect.right - paddle.rect.left) < 10 and puck.dx > 0:
                puck.dx = -PUCK_SPEED
            elif abs(puck.rect.left - paddle.rect.right) < 10 and puck.dx < 0:
                puck.dx = PUCK_SPEED


def game_loop(player_mode):
    # Initialize paddles for 2 or 4 players
    if player_mode == 2:
        paddles = [
            Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, 50, PADDLE_WIDTH, PADDLE_HEIGHT, RED),   # Top paddle
            Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 70, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)  # Bottom paddle
        ]
    else:  # 4 player mode
        paddles = [
            Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, 50, PADDLE_WIDTH, PADDLE_HEIGHT, RED),  # Top paddle
            Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 70, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE),  # Bottom paddle
            Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_HEIGHT, PADDLE_WIDTH, GREEN),  # Left paddle
            Paddle(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_HEIGHT, PADDLE_WIDTH, YELLOW)  # Right paddle
        ]

    puck = Puck(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PUCK_RADIUS, WHITE)
    
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move paddles based on player input
        keys = pygame.key.get_pressed()
        
        # Handle 2 players mode
        if player_mode == 2:
            if keys[pygame.K_a]:  # Move top paddle up
                paddles[0].rect.x -= 5
            if keys[pygame.K_d]:  # Move top paddle down
                paddles[0].rect.x += 5
            if keys[pygame.K_LEFT]:  # Move bottom paddle up
                paddles[1].rect.x -= 5
            if keys[pygame.K_RIGHT]:  # Move bottom paddle down
                paddles[1].rect.x += 5
        
        # Handle 4 players mode
        else:
            if keys[pygame.K_w]: paddles[0].rect.y -= 5  # Top paddle
            if keys[pygame.K_s]: paddles[0].rect.y += 5
            if keys[pygame.K_a]: paddles[2].rect.x -= 5  # Left paddle
            if keys[pygame.K_d]: paddles[2].rect.x += 5
            if keys[pygame.K_LEFT]: paddles[1].rect.x -= 5  # Right paddle
            if keys[pygame.K_RIGHT]: paddles[1].rect.x += 5

        # Move the puck
        puck.move()

        # Handle collisions with walls and paddles
        handle_collisions(puck, paddles)

        # Draw paddles and puck
        for paddle in paddles:
            paddle.draw()

        puck.draw()

        # Update the display
        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()
    sys.exit()


def main_menu():
    running = True
    while running:
        screen.fill(BLACK)

        title_text = font.render("4-Way Air Hockey", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        play_2p_text = font.render("Press 2 for 2 Players", True, WHITE)
        play_4p_text = font.render("Press 4 for 4 Players", True, WHITE)
        screen.blit(play_2p_text, (SCREEN_WIDTH // 2 - play_2p_text.get_width() // 2, 300))
        screen.blit(play_4p_text, (SCREEN_WIDTH // 2 - play_4p_text.get_width() // 2, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    game_loop(2)  # Start game in 2-player mode
                if event.key == pygame.K_4:
                    game_loop(4)  # Start game in 4-player mode

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()

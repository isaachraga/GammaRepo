import pygame
import pygame.freetype  # Import the freetype module.


pygame.init()
screen = pygame.display.set_mode((1280, 720))
GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 24)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Hello World!", (0, 0, 0))
    screen.blit(text_surface, (40, 250))
    # or just `render_to` the target surface.
    GAME_FONT.render_to(screen, (40, 350), "Hello World!", (0, 0, 0))

    pygame.display.flip()

pygame.quit()
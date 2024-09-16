import pygame
import pygame.freetype  # Import the freetype module.
import random


pygame.init()
screen = pygame.display.set_mode((1280, 720))
GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", 24)
clock = pygame.time.Clock()
running = True
dt = 0
num1 = 0
num2 = 0
result = ""
tmpScore = 0
score = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Dice 1:  "+str(num1), (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    # or just `render_to` the target surface.
    GAME_FONT.render_to(screen, (10, 30), "Dice 2: "+str(num2), (0, 0, 0))

    GAME_FONT.render_to(screen, (10, 250), result, (0, 0, 0))

    GAME_FONT.render_to(screen, (10, 350), "Press SPACE to roll", (0, 0, 0))

    

  

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("roll")
            #roll dice
            num1 = random.randint(1, 6)
            num2 = random.randint(1, 6)
            if num1==num2:
                if num1 == 1:
                    result = "SNAKE EYES"
                    score = 0
                    tmpScore = 0
                else:
                    result = "RESET"
                    tmpScorecore = 0
            else:
                result = ""
                tmpScore = tmpScore+num1+num2

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            score = score + tmpScore
            tmpScore = 0
            print("leave")

    GAME_FONT.render_to(screen, (10, 480), "Round: "+str(tmpScore), (0, 0, 0))
    GAME_FONT.render_to(screen, (10, 500), "Score: "+str(score), (0, 0, 0))
                
        
    


    
    pygame.display.flip()

pygame.quit()

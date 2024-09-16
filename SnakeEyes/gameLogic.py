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


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Player:
    tmpScore = 0
    score = 0
    stillIn = True

p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()

Players = [p1, p2, p3, p4]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            #print("hit key")
            if event.key == pygame.K_SPACE:
                #print("roll")
                #roll dice
                num1 = random.randint(1, 6)
                num2 = random.randint(1, 6)
                if num1==num2:
                    if num1 == 1:
                        result = "SNAKE EYES"
                        for p in Players:
                            p.tmpScore = 0
                            if p.stillIn is True:
                                p.score = 0
                            else:
                                p.stillIn = True
                                
                    else:
                        result = "RESET"

                        for p in Players:
                            p.stillIn = True
                            p.tmpScore = 0
                else:
                    result = ""
                    for p in Players:
                        if p.stillIn is True:
                            p.tmpScore = p.tmpScore+num1+num2
                        

            if event.key == pygame.K_1:
                p1.score = p1.score + p1.tmpScore
                p1.tmpScore = 0
                p1.stillIn = False
                #print("leave")
            if event.key == pygame.K_2:
                p2.score = p2.score + p2.tmpScore
                p2.tmpScore = 0
                p2.stillIn = False
                #print("leave")
            if event.key == pygame.K_3:
                p3.score = p3.score + p3.tmpScore
                p3.tmpScore = 0
                p3.stillIn = False
                #print("leave")
            if event.key == pygame.K_4:
                p4.score = p4.score + p4.tmpScore
                p4.tmpScore = 0
                p4.stillIn = False
                #print("leave")
        
        count = 0
        for p in Players:
            if p.stillIn == False:
                count = count + 1

        if count == 4:
            for p in Players:
                p.stillIn = True
                p.tmpScore = 0
                count = 0


    screen.fill((255,255,255))
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Dice 1:  "+str(num1), (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    # or just `render_to` the target surface.
    GAME_FONT.render_to(screen, (10, 30), "Dice 2: "+str(num2), (0, 0, 0))

    GAME_FONT.render_to(screen, (10, 250), result, (0, 0, 0))

    GAME_FONT.render_to(screen, (10, 350), "Press SPACE to roll", (0, 0, 0))
    GAME_FONT.render_to(screen, (10, 370), "Press Num key for player (P1 == 1) to leave the round", (0, 0, 0))

    

  

    
        

    GAME_FONT.render_to(screen, (10, 480), "Round:", (0, 0, 0))
    GAME_FONT.render_to(screen, (10, 500), "P!: "+str(p1.tmpScore)+"   P2: "+str(p2.tmpScore)+"   P3: "+str(p3.tmpScore)+"   P4: "+str(p4.tmpScore), (0, 0, 0))
    GAME_FONT.render_to(screen, (10, 520), "Score:", (0, 0, 0))
    GAME_FONT.render_to(screen, (10, 540), "P!: "+str(p1.score)+"   P2: "+str(p2.score)+"   P3: "+str(p3.score)+"   P4: "+str(p4.score), (0, 0, 0))
                
        
    


    
    pygame.display.flip()

pygame.quit()

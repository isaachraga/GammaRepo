import pygame
import socket #connection from 
import pickle #data has to be unserialized from server

WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 10
WHITE = (0, 255, 0)
BLACK = (0, 0, 0)

HOST = 'localhost' #connect with 
# HOST = ''
PORT = 5555

#GUI for the game
def draw_window(win, game_state, player):
    win.fill(BLACK)
    #makes adjustments for the position of ball based on where it was hit
    pygame.draw.circle(win, WHITE, game_state['ball_pos'], BALL_RADIUS)
    
    pygame.draw.rect(win, WHITE, (10, game_state['paddle1_pos'], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, WHITE, (WIDTH - 20, game_state['paddle2_pos'], PADDLE_WIDTH, PADDLE_HEIGHT))
    
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f"{game_state['score'][0]} - {game_state['score'][1]}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.update()

def client():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Client")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    player = pickle.loads(client_socket.recv(4096))
    print(f"Connected as Player {player}")

    paddle_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2
    run = True

    while run:
        pygame.time.delay(40)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle_pos > 0:
            paddle_pos -= 5
        if keys[pygame.K_DOWN] and paddle_pos < HEIGHT - PADDLE_HEIGHT:
            paddle_pos += 5
        
        client_socket.send(pickle.dumps(paddle_pos))
        
        game_state = pickle.loads(client_socket.recv(1024))

        draw_window(win, game_state, player)

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    client()
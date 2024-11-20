import pygame 

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel
        
        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

def main():
    run = True
    p = Player(50,50,100,100, (0,255,0))
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p)

main()

# import pygame
# import socket
# import pickle

# # Constants
# WIDTH, HEIGHT = 800, 600
# PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
# BALL_RADIUS = 10
# FPS = 60

# # Client to connect to the server
# class PongClient:
#     def __init__(self, server_ip='localhost', server_port=5555):
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client_socket.connect((server_ip, server_port))
#         self.game_state = None  # Store the current game state received from the server

#     def send_movement(self, movement):
#         try:
#             self.client_socket.send(pickle.dumps(movement))  # Send paddle movement to the server
#         except Exception as e:
#             print(f"Error sending movement: {e}")

#     def receive_game_state(self):
#         try:
#             return pickle.loads(self.client_socket.recv(4096))  # Receive updated game state from the server
#         except Exception as e:
#             print(f"Error receiving game state: {e}")
#             return None

# # Main client game loop to handle input and rendering
# def client_game_loop(pong_client):
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     clock = pygame.time.Clock()

#     run = True
#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False

#         keys = pygame.key.get_pressed()
#         movement = 0
#         if keys[pygame.K_UP]:
#             movement = -10  # Move up
#         elif keys[pygame.K_DOWN]:
#             movement = 10  # Move down

#         pong_client.send_movement(movement)

#         # Get the latest game state from the server
#         game_state = pong_client.receive_game_state()

#         if game_state:
#             # Render game based on the received game state
#             screen.fill((0, 0, 0))  # Clear the screen
#             # Draw paddles
#             for player in game_state.players:
#                 pygame.draw.rect(screen, (255, 255, 255), (player.x, player.y, PADDLE_WIDTH, PADDLE_HEIGHT))
#             # Draw ball
#             pygame.draw.circle(screen, (255, 255, 255), (game_state.ball.x, game_state.ball.y), BALL_RADIUS)

#             pygame.display.flip()  # Update the screen

#         clock.tick(FPS)

#     pygame.quit()
#     pong_client.client_socket.close()

# if __name__ == "__main__":
#     client = PongClient()  # Replace 'localhost' with the server IP if testing remotely
#     client_game_loop(client)

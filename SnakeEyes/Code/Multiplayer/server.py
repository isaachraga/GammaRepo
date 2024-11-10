import socket
from _thread import * 
import sys

server = "0.0.0.0" #localhost  "0.0.0.0";"127.0.0.1"

port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)

print("waiting for connection, Server started")

def threaded_client(conn):
    conn.send(str.encode("connected"))
    reply = ""
    while True:
        try: 
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("disconnected")
                break
            else:
                print("REcieved: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except: 
            break

while True : 
    conn, addr = s.accept()
    print("Connected to: " , addr)

    start_new_thread(threaded_client, (conn,))

# import socket
# import threading
# import pickle

# # Constants for the game
# WIDTH, HEIGHT = 800, 600
# PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
# BALL_RADIUS = 10

# # Player object to hold paddle positions
# class Player:
#     def __init__(self, paddle_x, paddle_y):
#         self.x = paddle_x
#         self.y = paddle_y

# class Ball:
#     def __init__(self):
#         self.x = WIDTH // 2
#         self.y = HEIGHT // 2
#         self.vx = 5  # Velocity X
#         self.vy = 5  # Velocity Y

# # Game state that will be synchronized between server and clients
# class GameState:
#     def __init__(self):
#         self.players = [Player(30, HEIGHT // 2 - PADDLE_HEIGHT // 2),  # Left player
#                         Player(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)]  # Right player
#         self.ball = Ball()

#     def update(self):
#         # Move the ball
#         self.ball.x += self.ball.vx
#         self.ball.y += self.ball.vy

#         # Ball collision with top and bottom walls
#         if self.ball.y - BALL_RADIUS <= 0 or self.ball.y + BALL_RADIUS >= HEIGHT:
#             self.ball.vy = -self.ball.vy

        # TODO: Add paddle collisions and scoring logic

# # Handle a single client connection
# def handle_client(conn, player_id, game_state):
#     try:
#         conn.send(pickle.dumps(game_state))  # Send initial game state to the client

#         while True:
#             data = conn.recv(1024)  # Receive paddle movement from client
#             if not data:
#                 break

#             # Update player's paddle position
#             move = pickle.loads(data)
#             if 0 <= game_state.players[player_id].y + move <= HEIGHT - PADDLE_HEIGHT:
#                 game_state.players[player_id].y += move

#             # Send updated game state to the client
#             conn.sendall(pickle.dumps(game_state))

#     except Exception as e:
#         print(f"Error with client {player_id}: {e}")
#     finally:
#         conn.close()

# # Main server function
# def server_program():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', 5555))
#     server.listen(2)  # Two players (clients) for Pong

#     game_state = GameState()
    
#     print("Server started, waiting for connections...")

#     connections = []
#     for player_id in range(2):
#         conn, addr = server.accept()
#         print(f"Player {player_id} connected from {addr}.")
#         connections.append(conn)
#         thread = threading.Thread(target=handle_client, args=(conn, player_id, game_state))
#         thread.start()

#     while True:
#         # Update game state every frame
#         game_state.update()
#         # Send the updated game state to all clients
#         for conn in connections:
#             try:
#                 conn.sendall(pickle.dumps(game_state))
#             except:
#                 pass  # Handle any disconnects

# if __name__ == "__main__":
#     server_program()

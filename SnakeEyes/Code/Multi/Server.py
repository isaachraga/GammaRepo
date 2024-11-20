import socket # Sends data over the network in this case we use 
import threading
import pickle

# HOST = '0.0.0.0' #change into 
# #make sure you use a TCP port dummy otherwise the server to client mapping can only be 1-to-1 using UDP (I would know I did that ... that was dumb)
# PORT = 8080

#drawing the window
PADDLE_HEIGHT = 100

PADDLE_WIDTH = 10
BALL_RADIUS = 10
WIDTH, HEIGHT = 600, 400 # used for the 

# game state map for update
game_state = {
    "ball_pos": [300, 200],
    "ball_vel": [5, 5],
    "paddle1_pos": 200,
    "paddle2_pos": 200,
    "score": [0, 0]
}

#updates clients for server (better org)
def handle_client(conn, addr, player):
    global game_state
    print(f"Player {player} connected from {addr}")
    
    conn.send(pickle.dumps(player))  
    #while game is running relay this information to all instances of client
    while True:
        try:

            #sets up player
            data = pickle.loads(conn.recv(4096))
            if player == 1:
                game_state['paddle1_pos'] = data
            else:
                game_state['paddle2_pos'] = data

            ball_pos = game_state['ball_pos']
            ball_vel = game_state['ball_vel']

            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
                ball_vel[1] = -ball_vel[1]

            if (ball_pos[0] - BALL_RADIUS <= PADDLE_WIDTH and
                game_state['paddle1_pos'] <= ball_pos[1] <= game_state['paddle1_pos'] + PADDLE_HEIGHT):
                ball_vel[0] = -ball_vel[0]  

                hit_pos = ball_pos[1] - (game_state['paddle1_pos'] + PADDLE_HEIGHT // 2)
                ball_vel[1] += hit_pos // 10  

            if (ball_pos[0] + BALL_RADIUS >= WIDTH - PADDLE_WIDTH and
                game_state['paddle2_pos'] <= ball_pos[1] <= game_state['paddle2_pos'] + PADDLE_HEIGHT):
                ball_vel[0] = -ball_vel[0]

                hit_pos = ball_pos[1] - (game_state['paddle2_pos'] + PADDLE_HEIGHT // 2)
                ball_vel[1] += hit_pos // 10

            if ball_pos[0] - BALL_RADIUS <= 0:  
                game_state['score'][1] += 1
                ball_pos[0], ball_pos[1] = WIDTH // 2, HEIGHT // 2  
                ball_vel[0] = -5  
                ball_vel[1] = 5

            if ball_pos[0] + BALL_RADIUS >= WIDTH:  
                game_state['score'][0] += 1
                ball_pos[0], ball_pos[1] = WIDTH // 2, HEIGHT // 2
                ball_vel[0] = 5 
                ball_vel[1] = -5
            #unserializes the connection 
            conn.sendall(pickle.dumps(game_state))
        #error handling
        except:
            print(f"Player {player} disconnected")
            break

    conn.close()

def server(HOST, PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(2)  # Listen for 2 players

            print("Server started. Waiting for connections...")
            player = 1
            while player <= 2:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr, player)).start()
                player += 1  # Add to player count after another player has connected
    
    except ConnectionRefusedError:
        print("Connection was refused. Check IP, port, and network setup.")



if __name__ == "__main__":
    # host = socket.gethostbyname(socket.gethostname())
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #part of setup
    # s.connect(("8.8.8.8", 80)) #checks connection to network
    # #host = s.getsockname()[0]
    # s.close()
    # host = "0.0.0.0"
    host = 'localhost'
    port = 5555
    server(host,port)
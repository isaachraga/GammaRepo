import socket
import pygame

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Connect to the server
server_addr = ('localhost', 65432)  # Change this as needed
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_addr)

def handle_paddle_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return -10  # Move paddle up
    elif keys[pygame.K_DOWN]:
        return 10  # Move paddle down
    return 0  # No movement

running = True
left_paddle_pos = 0
right_paddle_pos = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get paddle movement and send it to the server
    movement = handle_paddle_movement()
    sock.send(str(movement).encode('utf-8'))
    
    # Receive updated paddle positions from the server
    positions = sock.recv(1024).decode('utf-8')
    print(f"Recieved from server: {positions}")
    try:
        left_paddle_pos, right_paddle_pos = map(int, positions.split(','))
    except ValueError:
        print(f"Error parsing positions: {positions}")
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the paddles
    pygame.draw.rect(screen, (255, 255, 255), (50, left_paddle_pos, 10, 100))
    pygame.draw.rect(screen, (255, 255, 255), (740, right_paddle_pos, 10, 100))
    
    # Update the screen
    pygame.display.flip()
    
    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Close the connection
sock.close()
pygame.quit()

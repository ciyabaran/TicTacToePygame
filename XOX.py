import pygame
import sys

pygame.init()

# Set up window dimensions
width, height = 300, 400  
cell_size = width // 3
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')  

# Define colors
bg_color = (0, 0, 102)  
line_color = (0, 51, 102)  
cross_color = (255, 255, 255)  
circle_color = (0, 204, 255)  
font_color = (255, 255, 255)  
button_color = (0, 102, 204)  
button_hover_color = (0, 153, 255)  

# Load font
font = pygame.font.Font(None, 36)

# Initialize game board and state
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 0 means empty, 1 means 'X', 2 means 'O'
current_player = 1  # Start with player 'X'
winner = None  # Track who wins


def draw_shapes():
    # Draw 'X's and 'O's on the board based on game state
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:   # Player 'X'
                pygame.draw.line(screen, cross_color, (col * cell_size + 15, row * cell_size + 15), 
                                 (col * cell_size + cell_size - 15, row * cell_size + cell_size - 15), 10)
                pygame.draw.line(screen, cross_color, (col * cell_size + cell_size - 15, row * cell_size + 15), 
                                 (col * cell_size + 15, row * cell_size + cell_size - 15), 10)
            elif board[row][col] == 2:  # Player 'O'
                pygame.draw.circle(screen, circle_color, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), cell_size // 4, 10)

def draw_grid():
    for i in range(1, 4):
        # Draw horizontal lines
        pygame.draw.line(screen, line_color, (0, i * cell_size), (width, i * cell_size), 10)
        # Draw vertical lines
        pygame.draw.line(screen, line_color, (i * cell_size, 0), (i * cell_size, height - 100), 10)

def check_winner():
    for i in range(3):
        # Check rows for a winner
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        # Check columns for a winner
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]

    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    return None  # No winner yet

def check_draw():
    # Check if the game is a draw (all cells are filled with no winner)
    for row in board:
        if 0 in row:
            return False
    return True  # All cells are filled but no winner -> draw

def reset_game():
    # Reset the game state
    global board, current_player, winner
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    current_player = 1  
    winner = None  

def draw_buttons():
    # Draw restart and quit buttons
    restart_button = pygame.Rect(50, 320, 100, 50)
    quit_button = pygame.Rect(150, 320, 100, 50)

    restart_text = font.render("Restart", True, font_color)
    quit_text = font.render("Quit", True, font_color)
    screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 30, quit_button.y + 10))

# Game loop
while True:
    screen.fill(bg_color)  
    draw_grid()  
    draw_shapes()   
    draw_buttons()  

    # Display winner or draw message
    if winner:
        text = font.render(f"Player {winner} wins!", True, font_color)
        screen.blit(text, (50, 250))
    elif check_draw():
        text = font.render("It's a Draw!", True, font_color)
        screen.blit(text, (100, 250))

    for event in pygame.event.get():
        # Check if the close button is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Check for mouse click event if no winner yet
        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            # Get mouse position
            mx, my = event.pos
            
            # Calculate row and column based on mouse position
            row, col = my // cell_size, mx // cell_size
            
            # Check if the clicked cell is valid and empty
            if (0 <= row < 3) and (0 <= col < 3) and (board[row][col] == 0):  
                # Mark the cell with the current player's symbol
                board[row][col] = current_player
                
                # Check if this move resulted in a winner
                winner = check_winner()  
                
                # Switch to the other player
                current_player = 2 if current_player == 1 else 1  
                
        # Check for mouse click if there's a winner or a draw        
        if event.type == pygame.MOUSEBUTTONDOWN and (winner or check_draw()):
            mx, my = event.pos
            # Define restart and quit button areas
            restart_button = pygame.Rect(50, 320, 100, 50)
            quit_button = pygame.Rect(150, 320, 100, 50)
            
            # If restart button is clicked, reset the game
            if restart_button.collidepoint(mx, my):
                reset_game()
                
            # If quit button is clicked, exit the game
            elif quit_button.collidepoint(mx, my):
                pygame.quit()
                sys.exit()

    pygame.display.update()

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS, ROWS = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0),
          (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1], [1, 1]],  # O
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Lite")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

def new_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {"shape": shape, "x": COLUMNS // 2 - len(shape[0]) // 2, "y": 0, "color": color}

def draw_piece(piece):
    for i, row in enumerate(piece["shape"]):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    piece["color"],
                    pygame.Rect((piece["x"] + j) * BLOCK_SIZE, (piece["y"] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )

def draw_grid():
    for y in range(ROWS):
        for x in range(COLUMNS):
            if grid[y][x]:
                pygame.draw.rect(
                    screen,
                    grid[y][x],
                    pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
            pygame.draw.rect(
                screen,
                GRAY,
                pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )

def valid_position(piece, dx=0, dy=0):
    for i, row in enumerate(piece["shape"]):
        for j, cell in enumerate(row):
            if cell:
                x = piece["x"] + j + dx
                y = piece["y"] + i + dy
                if x < 0 or x >= COLUMNS or y >= ROWS:
                    return False
                if y >= 0 and grid[y][x]:
                    return False
    return True

def lock_piece(piece):
    for i, row in enumerate(piece["shape"]):
        for j, cell in enumerate(row):
            if cell:
                x = piece["x"] + j
                y = piece["y"] + i
                if 0 <= y < ROWS:
                    grid[y][x] = piece["color"]

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    lines_cleared = ROWS - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [None for _ in range(COLUMNS)])
    grid = new_grid

def show_game_over_screen():
    screen.fill(BLACK)
    text = font.render("Game Over", True, WHITE)

    # Use a smaller font for subtext
    small_font = pygame.font.SysFont("Arial", 18)
    line1 = small_font.render("Press R to Restart", True, WHITE)
    line2 = small_font.render("or Q to Quit", True, WHITE)

    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
    screen.blit(line1, line1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(line2, line2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def reset_game():
    global grid, current_piece, fall_time, running
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_piece = new_piece()
    fall_time = 0
    running = True

# Game loop
current_piece = new_piece()
fall_time = 0
fall_speed = 0.5  # seconds
running = True

while True:
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if valid_position(current_piece, dx=-1):
                        current_piece["x"] -= 1
                elif event.key == pygame.K_RIGHT:
                    if valid_position(current_piece, dx=1):
                        current_piece["x"] += 1
                elif event.key == pygame.K_DOWN:
                    if valid_position(current_piece, dy=1):
                        current_piece["y"] += 1
                elif event.key == pygame.K_UP:
                    rotated = list(zip(*current_piece["shape"][::-1]))
                    rotated = [list(row) for row in rotated]
                    old_shape = current_piece["shape"]
                    current_piece["shape"] = rotated
                    if not valid_position(current_piece):
                        current_piece["shape"] = old_shape
                elif event.key == pygame.K_SPACE:
                    while valid_position(current_piece, dy=1):
                        current_piece["y"] += 1
                    lock_piece(current_piece)
                    clear_lines()
                    current_piece = new_piece()
                    if not valid_position(current_piece):
                        running = False

        if fall_time / 1000 > fall_speed:
            if valid_position(current_piece, dy=1):
                current_piece["y"] += 1
            else:
                lock_piece(current_piece)
                clear_lines()
                current_piece = new_piece()
                if not valid_position(current_piece):
                    running = False
            fall_time = 0

        draw_grid()
        draw_piece(current_piece)
        pygame.display.flip()

    show_game_over_screen()

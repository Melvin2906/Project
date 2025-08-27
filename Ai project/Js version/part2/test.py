import pygame
import sys
import random

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)      # Snake color
DARK_GREEN = (0, 100, 0)   # Snake outline
RED = (200, 0, 0)        # Food color
GRAY = (40, 40, 40)        # Grid color

# Game speed
GAME_SPEED = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Game Classes/Functions ---

class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Prevent the snake from turning back on itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)

        # Check for self-collision
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Collision detected

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False # No collision

    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, DARK_GREEN, r, 1)

    def handle_keys(self, event):
        if event.key == pygame.K_UP:
            self.turn(UP)
        elif event.key == pygame.K_DOWN:
            self.turn(DOWN)
        elif event.key == pygame.K_LEFT:
            self.turn(LEFT)
        elif event.key == pygame.K_RIGHT:
            self.turn(RIGHT)


class Food:
    """Represents the food in the game."""
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        # Ensure food does not spawn on the snake
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, DARK_GREEN, r, 1)


def draw_grid(surface):
    """Draws the background grid."""
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, GRAY, r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, rr)


def show_game_over_screen(screen, score, font):
    """Displays the game over screen and waits for user input."""
    screen.fill(BLACK)
    
    # "Game Over" text
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # "Final Score" text
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(score_text, score_rect)

    # "Play Again" text
    play_again_text = font.render("Press any key to Play Again", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(play_again_text, play_again_rect)

    pygame.display.flip()

    # Wait for a key press to restart or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def main():
    """Main game function."""
    pygame.init()

    # Setup the screen and clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Python Snake")
    
    # Fonts for score and game over text
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Create game objects
    snake = Snake()
    food = Food()
    food.randomize_position(snake.positions)

    # --- Main Game Loop ---
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake.handle_keys(event)

        # Move the snake and check for self-collision
        collided = snake.move()
        if collided:
            show_game_over_screen(screen, snake.score, font)
            snake.reset()
            food.randomize_position(snake.positions)

        # Check for collision with food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position(snake.positions)

        # --- Drawing ---
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        # Display the score
        score_text = small_font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (5, 5))
        
        # Update the display
        pygame.display.update()

        # Control the game speed
        clock.tick(GAME_SPEED)


# --- Start the game ---
if __name__ == "__main__":
    main()                                        
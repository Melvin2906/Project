import pygame
import random
import webbrowser
import sys
import os

# Initialisation
pygame.init()

# Dimensions de base
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fenêtre non redimensionnable
pygame.display.set_caption("Menu Principal")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Classe pour les boutons
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

font = pygame.font.Font(None, 35)

def resource_path(relative_path):
    try:
        # PyInstaller crée un dossier temporaire pour les fichiers ajoutés
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def draw_image(str_img):
    image = resource_path("assets/" + str_img)
    sprite = pygame.image.load(image).convert_alpha()
    sprite = pygame.transform.scale(sprite, (500, 600))
    screen.fill(BLACK)
    screen.blit(sprite, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def first_step(score, num):
    if num == 84:
        return False
    if score >= num:
        if num == 1000:
            draw_image("bottle3.png")
        elif num == 330:
            draw_image("bottle1.png")
        elif num == 500:
            draw_image("bottle2.jpg")
        return "interface"
    return False

def interface():
    screen.fill(BLACK)
    running = True
    while running:
        screen.fill(BLACK)
        button_easy = Button("Easy", WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 50)
        button_medium = Button("Medium", WIDTH // 2 - 100, HEIGHT // 2 - 75, 200, 50)
        button_hard = Button("Hard", WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        button_loop = Button("Loop", WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50)
        button_back = Button("Back", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)

        for btn in [button_easy, button_medium, button_hard, button_loop, button_back]:
            btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy.rect.collidepoint(event.pos): return 330
                elif button_medium.rect.collidepoint(event.pos): return 500
                elif button_hard.rect.collidepoint(event.pos): return 1000
                elif button_loop.rect.collidepoint(event.pos): return 84
                elif button_back.rect.collidepoint(event.pos): return menu()

def play_snake(lim):
    score = 0
    BLOCK_SIZE = 20
    snake_speed = 10
    snake_list = [[WIDTH // 2, HEIGHT // 2]]
    snake_direction = "RIGHT"
    food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    clock = pygame.time.Clock()

    sprites = {
        "food": pygame.transform.scale(pygame.image.load(resource_path("assets/water2.png")), (BLOCK_SIZE, BLOCK_SIZE)),
        "head": pygame.transform.scale(pygame.image.load(resource_path("assets/head.png")), (BLOCK_SIZE + 2, BLOCK_SIZE + 2)),
        "body": pygame.transform.scale(pygame.image.load(resource_path("assets/body.png")), (BLOCK_SIZE - 1, BLOCK_SIZE - 1)),
        "bg": pygame.transform.scale(pygame.image.load(resource_path("assets/grass.jpeg")), (WIDTH, HEIGHT))
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT": snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT": snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN": snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP": snake_direction = "DOWN"

        head_x, head_y = snake_list[0]
        if snake_direction == "UP": head_y -= BLOCK_SIZE
        elif snake_direction == "DOWN": head_y += BLOCK_SIZE
        elif snake_direction == "LEFT": head_x -= BLOCK_SIZE
        elif snake_direction == "RIGHT": head_x += BLOCK_SIZE

        new_head = [head_x, head_y]
        snake_list.insert(0, new_head)

        if head_x == food_x and head_y == food_y:
            score += 10
            food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        else:
            snake_list.pop()

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake_list[1:]:
            break

        screen.blit(sprites["bg"], (0, 0))
        screen.blit(sprites["head"], (head_x, head_y))
        for s in snake_list[1:]: screen.blit(sprites["body"], s)
        screen.blit(sprites["food"], (food_x, food_y))

        score_text = font.render(f"Score: {score} cl", True, WHITE)
        screen.blit(score_text, (10, 10))
        if first_step(score, lim) == "interface":
            return interface()

        pygame.display.update()
        clock.tick(snake_speed)

def play_subway(lim):
    player_x = 100
    player_y = 300
    lane_positions = [100, 200, 300]
    current_lane = 1
    jumping = False
    jump_count = 10

    obstacles = []
    coins = []
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.SysFont(None, 36)

    background = pygame.image.load(resource_path("assets/sky.jpeg"))
    background = pygame.transform.scale(background, (800, 600))
    sprite = pygame.image.load(resource_path("assets/water2.png")).convert_alpha()
    sprite = pygame.transform.scale(sprite, (30, 40))
    runner = pygame.image.load(resource_path("assets/runner.png")).convert_alpha()
    runner = pygame.transform.scale(runner, (60, 60))
    obstacl = pygame.image.load(resource_path("assets/sun.png")).convert_alpha()
    obstacl = pygame.transform.scale(obstacl, (50, 50))
    bg_x = 0

    running = True
    while running:
        screen.fill(WHITE)

        bg_x -= 5
        if bg_x <= -800:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + 800, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and current_lane > 0:
                    current_lane -= 1
                elif event.key == pygame.K_DOWN and current_lane < len(lane_positions) - 1:
                    current_lane += 1
                elif event.key == pygame.K_SPACE and not jumping:
                    jumping = True
                elif event.key == pygame.K_ESCAPE:
                    menu()
                    running = False

        if jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = 10
        else:
            player_y = lane_positions[current_lane]

        if random.randint(1, 50) == 1:
            obstacles.append([800, random.choice(lane_positions)])
        if random.randint(1, 100) == 1:
            coins.append([800, random.choice(lane_positions)])

        for obstacle in obstacles[:]:
            obstacle[0] -= 10
            if obstacle[0] < -30:
                obstacles.remove(obstacle)

        for coin in coins[:]:
            coin[0] -= 7
            if coin[0] < -10:
                coins.remove(coin)

        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        for obstacle in obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 30, 50)
            if player_rect.colliderect(obstacle_rect):
                running = False

        for coin in coins[:]:
            coin_rect = pygame.Rect(coin[0] - 10, coin[1] - 10, 20, 20)
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                score += 10

        #pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
        screen.blit(runner, (player_x, player_y))
        for obstacle in obstacles:
            screen.blit(obstacl, (obstacle[0], obstacle[1]))
            #pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], 30, 50))
        for coin in coins:
            screen.blit(sprite, (coin[0], coin[1]))
            #pygame.draw.circle(screen, GOLD, (coin[0], coin[1]), 10)
            #print(coin[0], coin[0])

        score_text = font.render(f"Score: {score} cl", True, BLACK)
        screen.blit(score_text, (10, 550))
        if first_step(score, lim) == "interface":
            return interface()
        pygame.display.update()
        clock.tick(30)


def menu():
    background = pygame.transform.scale(pygame.image.load(resource_path("assets/images.png")), (WIDTH, HEIGHT))
    waiting = True
    while waiting:
        screen.blit(background, (0, 0))
        buttons = [
            Button("Snake Game", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50),
            Button("Runner Game", WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50),
            Button("En savoir plus", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50),
            Button("Quitter", WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
        ]
        for b in buttons: b.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(event.pos): play_snake(interface())
                elif buttons[1].rect.collidepoint(event.pos): play_subway(interface())
                elif buttons[2].rect.collidepoint(event.pos): webbrowser.open("https://68900fbf76be9100b10983e5--rainbow-pudding-85160e.netlify.app/")
                elif buttons[3].rect.collidepoint(event.pos): pygame.quit(); sys.exit()

menu()


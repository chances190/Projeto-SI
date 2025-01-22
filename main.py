import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class SnakeGame:
    def __init__(self):
        self.snake = [(0, 0)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.random_food()

    def random_food(self):
        return (
            random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
        )

    def move(self):
        head = (self.snake[-1][0] + self.direction[0], self.snake[-1][1] + self.direction[1])
        self.snake.append(head)
        if head == self.food:
            self.food = self.random_food()
        else:
            self.snake.pop(0)

    def collision(self):
        head = self.snake[-1]
        if head in self.snake[:-1] or not (0 <= head[0] < WIDTH) or not (0 <= head[1] < HEIGHT):
            return True
        return False

    def draw(self):
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (*self.food, CELL_SIZE, CELL_SIZE))
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()


def main():
    game = SnakeGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != (0, CELL_SIZE):
                    game.direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and game.direction != (0, -CELL_SIZE):
                    game.direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and game.direction != (CELL_SIZE, 0):
                    game.direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and game.direction != (-CELL_SIZE, 0):
                    game.direction = (CELL_SIZE, 0)

        game.move()
        if game.collision():
            break
        game.draw()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import numpy as np
import random
from enum import Enum

# Constants
# *********

# Game Constants
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREEN1 = (0, 255, 0)
GREEN2 = (100, 255, 0)
RED = (255, 0, 0)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class SnakeGame:
    def __init__(self, width=640, height=480, fps=20):
        self.width = width
        self.height = height
        self.fps = fps

        pygame.init()

        # Init display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")

        # Init other game features
        self.font = pygame.font.SysFont('arial', 25)
        self.clock = pygame.time.Clock()

        # Init features for the game
        self.head = None
        self.body = None
        self.direction = None
        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self.iterations_since_reward = 0
        self.reset()
        self._place_food()

    def reset(self):
        # Init game state
        self.direction = Direction.RIGHT

        # Place the head in the center of the screen
        self.head = Point(self.width / 2, self.height / 2)

        self.body = [self.head,
                     Point(self.head.x - BLOCK_SIZE, self.head.y),
                     Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0

        self.frame_iteration = 0
        self.iterations_since_reward = 0

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.body:
            self._place_food()

    def _move(self):
        new_head = self.body.pop()
        if self.direction == Direction.RIGHT:
            new_head.x = self.head.x + BLOCK_SIZE
            new_head.y = self.head.y
        elif self.direction == Direction.LEFT:
            new_head.x = self.head.x - BLOCK_SIZE
            new_head.y = self.head.y
        elif self.direction == Direction.DOWN:
            new_head.y = self.head.y + BLOCK_SIZE
            new_head.x = self.head.x
        elif self.direction == Direction.UP:
            new_head.y = self.head.y - BLOCK_SIZE
            new_head.x = self.head.x

        self.body.insert(0, new_head)
        self.head = new_head

    def _extend_snake(self):
        new_tail = Point(0, 0)
        if self.direction == Direction.RIGHT:
            new_tail.x = self.body[-1].x - BLOCK_SIZE
            new_tail.y = self.body[-1].y
        elif self.direction == Direction.LEFT:
            new_tail.x = self.body[-1].x + BLOCK_SIZE
            new_tail.y = self.body[-1].y
        elif self.direction == Direction.DOWN:
            new_tail.y = self.body[-1].y - BLOCK_SIZE
            new_tail.x = self.body[-1].x
        elif self.direction == Direction.UP:
            new_tail.y = self.body[-1].y + BLOCK_SIZE
            new_tail.x = self.body[-1].x

        self.body.append(new_tail)

    def _update_ui(self):
        self.screen.fill(BLACK)

        # Draw head
        pygame.draw.rect(self.screen, GREEN1, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, GREEN2,
                         pygame.Rect(self.head.x + 4, self.head.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))

        # Draw rest of body
        for body_part in self.body[1:]:
            pygame.draw.rect(self.screen, BLUE1, pygame.Rect(body_part.x, body_part.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, BLUE2,
                             pygame.Rect(body_part.x + 4, body_part.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
        # Draw fruit
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Print current score
        text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (0, 0))

        pygame.display.flip()

    def play_step_human(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. Move snake
        self._move()

        # 3. Check if game is over
        if self.is_collision():
            return True

        # 4. Check if food is reached
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self._extend_snake()

        # 5. Update UI och clock
        self._update_ui()
        self.clock.tick(self.fps)

        # 6. Return game state
        return False

    def play_step_ai(self, action):
        self.frame_iteration += 1
        self.iterations_since_reward += 1

        # Check if user closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Convert AI action to a new direction

        # action = [straight, right, left]
        # [1, 0, 0] = > Keep on going straight
        # [0, 1, 0] = > Turn right
        # [0, 0, 1] = > Turn left

        clockwise_dir = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        dir_idx = clockwise_dir.index(self.direction)

        if np.array_equal(action, [0, 1, 0]):  # Turn right
            dir_idx = (dir_idx + 1) % len(clockwise_dir)
        if np.array_equal(action, [0, 0, 1]):  # Turn left
            dir_idx = (dir_idx - 1) % len(clockwise_dir)

        self.direction = clockwise_dir[dir_idx]

        # Move the snake
        self._move()

        # Check if game is over
        if self.is_collision():
            return True, -10, self.score  # Game over, reward, final score
        elif self.iterations_since_reward > 100 * len(self.body):
            return True, -5, self.score   # Game over, reward, final score

        reward = 0
        # Check if food is reached
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self._extend_snake()

            self.iterations_since_reward = 0
            reward = 10
        # elif self._within_one():
        #     reward = 5

        # Update UI and clock
        self._update_ui()
        self.clock.tick(self.fps)

        # Return game state
        return False, reward, self.score



    def is_collision(self, point=None):
        if not point:
            point = self.head

        # Check if snake hits itself
        if point in self.body[1:]:
            return True

        # Check if we hit a wall
        if point.x + BLOCK_SIZE > self.width or \
                point.x < 0 or \
                point.y + BLOCK_SIZE > self.height or \
                point.y < 0:
            return True

        return False

    def _within_one(self):
        # TODO: Fix this one PLEASE
        return abs(self.head.x - self.food.x) == BLOCK_SIZE and abs(self.head.y - self.food.y) == BLOCK_SIZE

    @staticmethod
    def human_play():
        game = SnakeGame()

        # Game loop
        while True:
            if game.play_step_human():
                break
        print('Final score: ', game.score)

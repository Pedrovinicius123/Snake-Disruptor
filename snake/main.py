import pygame
import random
import time
import sys
from typing import List, Tuple
from snake import Snake
from robo import change_direction, Direction

# Constants
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 50)
RED = (200, 0, 0)
WINDOW_SIZE = 400
BLOCK_SIZE = 20
FPS = 10
MOVE_DELAY = 0.1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.clock = pygame.time.Clock()
        self.block_size = BLOCK_SIZE
        self.fruit_possibilities = self.generate_fruit_possibilities()
        self.reset_game()
        
    def reset_game(self):
        """Reset the game state for a new round"""
        self.fruit = random.choice(self.fruit_possibilities)
        self.snake = Snake(random.choice([pos for pos in self.fruit_possibilities if pos != self.fruit]))
        self.direction = random.choice(['N', 'S', 'E', 'W'])
        self.last_position = (0, 0)
        self.game_over = False
        
    def generate_fruit_possibilities(self) -> List[List[int]]:
        """Generate all possible fruit positions on the grid"""
        return [
            [x, y] 
            for x in range(0, WINDOW_SIZE, self.block_size)
            for y in range(0, WINDOW_SIZE, self.block_size)
        ]
    
    def check_collision(self) -> bool:
        """Check if snake has collided with itself"""
        head = self.snake.positions[-1]
        
        if head in self.snake.positions[:-1]:
            print(head, self.snake.positions[:-1].index(head))
            return True
        
        return False

    
    def check_boundaries(self) -> bool:
        """Check if snake is within game boundaries"""
        x, y = self.snake.positions[-1]
        return 0 <= x < WINDOW_SIZE and 0 <= y < WINDOW_SIZE
    
    def update_fruit(self):
        """Update fruit position when eaten"""
        self.fruit_possibilities.append(self.last_position)
        self.fruit_possibilities.remove(self.snake.positions[-1])
        self.fruit = random.choice(self.fruit_possibilities)
    
    def handle_movement(self):
        """Handle snake movement based on current direction"""
        head_x, head_y = self.snake.positions[-1]
        
        direction_map = {
            'E': [head_x + self.block_size, head_y],
            'W': [head_x - self.block_size, head_y],
            'S': [head_x, head_y + self.block_size],
            'N': [head_x, head_y - self.block_size]
        }
        
        next_position = direction_map[self.direction]
        
        if next_position == self.fruit:
            self.last_position = self.snake.forward(next_position, grow=True)
            self.update_fruit()
        else:
            self.last_position = self.snake.forward(next_position)
            if next_position in self.fruit_possibilities:
                self.fruit_possibilities.remove(next_position)
    
    def draw_grid(self):
        """Draw the game grid"""
        for x in range(0, WINDOW_SIZE, self.block_size):
            for y in range(0, WINDOW_SIZE, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_snake(self):
        """Draw the snake on the screen"""
        for position in self.snake.positions:
            x, y = position
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(self.screen, GREEN, rect)
    
    def draw_fruit(self):
        """Draw the fruit on the screen"""
        rect = pygame.Rect(self.fruit[0], self.fruit[1], self.block_size, self.block_size)
        pygame.draw.rect(self.screen, RED, rect)
    
    def run(self):
        """Main game loop"""
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_over = False
            
            if not self.game_over:
                print(self.direction)
                # Update game state
                self.screen.fill(BLACK)
                self.draw_grid()
                self.draw_fruit()
                
                # AI direction decision
                self.direction = change_direction(
                    self.direction,
                    self.snake.positions,
                    self.block_size,
                    tuple(self.snake.positions[-1]),
                    self.last_position,
                    tuple(self.fruit),
                    "NSEW"
                )
                
                self.handle_movement()
                
                # Check game over conditions
                if not self.check_boundaries() or self.check_collision():
                    self.game_over = True
                
                self.draw_snake()
                time.sleep(MOVE_DELAY)
            else:
                # Game over screen
                font = pygame.font.SysFont(None, 72)
                text = font.render("Game Over", True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
                self.screen.blit(text, text_rect)
                
                restart_font = pygame.font.SysFont(None, 36)
                restart_text = restart_font.render("Press R to restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 50))
                self.screen.blit(restart_text, restart_rect)
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
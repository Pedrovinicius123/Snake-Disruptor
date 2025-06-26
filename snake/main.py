import pygame, random, time, sys
from ctypes import *
from snake import Snake

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 200, 50)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def load_main_script():
    libc = CDLL('./main.o')
    libc.change_direction.restype = c_char
    libc.change_direction.argtypes = [c_char, c_char, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(POINTER(c_int)), POINTER(POINTER(c_int)), c_char_p]
    
    return libc

def generate_fruit_possibilities(board_width, grid_size):
    possibilities = []
    print(board_width, grid_size)

    for i in range(0, board_width, grid_size):
        for j in range(0, board_width, grid_size):
            possibilities.append([i, j])

    return possibilities

def check_collision(snake:Snake):
    for idx, position in enumerate(snake.positions):
        for idx_other, other in enumerate(snake.positions):
            if idx != idx_other and position == other:
                print('?')
                return True

    return False


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    block_size = 20
    
    fruit_possib = generate_fruit_possibilities(WINDOW_WIDTH, block_size)
    fruit = random.choice(fruit_possib)
    fruit_possib.remove(fruit)

    robot_snake = load_main_script()
    snake = Snake(random.choice(fruit_possib))
    direction = 'N'   
    anterior_direction = 'S'
    last_position = None
    anterior_pos = [0, 0]
    

    next_snake = snake.return_instance()

    while True:
        array_of_rows = None
        SCREEN.fill(BLACK)
        drawGrid(block_size=block_size)
        pygame.draw.rect(SCREEN, (200, 0, 0), pygame.Rect(fruit[0], fruit[1], block_size, block_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_pos = (c_int * 2)(*snake.positions[-1])
        anterior_pos = (c_int * 2)(*anterior_pos)
        fruit_pos = (c_int * 2)(*fruit)

        choices = "NSEW"
        print(type(choices.encode('utf-8')))

        rows = [(c_int * 2)(x, y) for (x, y) in snake.positions]
        array_of_rows = (POINTER(c_int) * len(rows))(*[cast(row, POINTER(c_int)) for row in rows])

        rows_copy = [(c_int * 2)(x, y) for (x, y) in  next_snake.positions]
        array_of_rows_copy = (POINTER(c_int) * len(rows))(*[cast(row, POINTER(c_int)) for row in rows_copy])

        anterior_direction_pos = direction
        direction = robot_snake.change_direction(c_char(direction.encode()), c_char(anterior_direction.encode()), c_int(len(snake.positions)), c_int(block_size), current_pos, anterior_pos, fruit_pos, array_of_rows, array_of_rows_copy, choices.encode('utf-8')).decode()
        anterior_direction = anterior_direction_pos

        if direction == 'E':
            next_position = [snake.positions[-1][0]+block_size, snake.positions[-1][1]]

        elif direction == 'W':
            next_position = [snake.positions[-1][0]-block_size, snake.positions[-1][1]]

        elif direction == 'S':
            next_position = [snake.positions[-1][0], snake.positions[-1][1] + block_size]
            
        elif direction == 'N':
            next_position = [snake.positions[-1][0], snake.positions[-1][1] - block_size]

        current_pos = (c_int * 2)(*snake.positions[-1])
        next_pos = (c_int * 2)(*next_position)
        fruit_pos = (c_int * 2)(*fruit)

        choices = "NSEW"
        print(type(choices.encode('utf-8')))

        rows = [(c_int * 2)(x, y) for (x, y) in snake.positions]
        array_of_rows = (POINTER(c_int) * len(rows))(*[cast(row, POINTER(c_int)) for row in rows])

        rows_copy = [(c_int * 2)(x, y) for (x, y) in  next_snake.positions]
        array_of_rows_copy = (POINTER(c_int) * len(rows))(*[cast(row, POINTER(c_int)) for row in rows_copy])

        anterior_direction_pos = direction
        direction = robot_snake.change_direction(c_char(direction.encode()), c_char(anterior_direction.encode()), c_int(len(snake.positions)), c_int(block_size), next_pos, current_pos, fruit_pos, array_of_rows, array_of_rows_copy, choices.encode('utf-8')).decode()
        anterior_direction = anterior_direction_pos
                
        if not (0 <= snake.positions[-1][0] <= WINDOW_WIDTH) or not (0 <= snake.positions[-1][1] <= WINDOW_HEIGHT) or check_collision(snake):
            break

        anterior_pos = snake.positions[-1].copy()
        
        if next_position == fruit:
            last_position = snake.forward(next_position, grow=True)
            next_snake = snake.return_instance()

            fruit_possib.append(last_position)
            fruit_possib.remove(next_position)

            fruit = random.choice(fruit_possib)
        
        else:
            last_position = snake.forward(next_position)
            next_snake = snake.return_instance()

            fruit_possib.append(last_position)
            if next_position in fruit_possib:
                fruit_possib.remove(next_position)

        print('FRUIT', fruit, direction)        
        
        print(direction)
        drawSnake(snake, block_size)
        time.sleep(0.1)
        
        pygame.display.update()


def drawGrid(block_size):
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

def drawSnake(snake:Snake, block_size):
    for position in snake.positions:
        x, y = position
        rect = pygame.Rect(x, y, block_size, block_size)
        pygame.draw.rect(SCREEN, GREEN, rect)

if __name__ == '__main__':
    main()

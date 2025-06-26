import math

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def remove_char(s, index):
    if index >= len(s):
        return s
    return s[:index] + s[index+1:]

def find_and_remove(s, item):
    for i, char in enumerate(s):
        if char == item:
            return remove_char(s, i)
    return s

def check_position_in(current_pos, snake):
    for segment in snake[1:]:
        if current_pos[0] == segment[0] and current_pos[1] == segment[1]:
            print("!!!!")
            return False
    return True

def check_collision(current_direction, current_pos, anterior_pos, snake, fruit_pos):
    for position in snake[1:]:
        if current_pos[0] == position[0] and fruit_pos[0] == position[0] and fruit_pos[1] > position[1] and current_direction in ('W', 'E'):
            return change_direction('S', len(snake), 20, current_pos, anterior_pos, fruit_pos, snake, "SEW")
        
        elif current_pos[0] == position[0] and fruit_pos[0] == position[0] and fruit_pos[1] < position[1] and current_direction in ('W', 'E'):
            return change_direction('N', len(snake), 20, current_pos, anterior_pos, fruit_pos, snake, "NEW")
        
        elif current_pos[1] == position[1] and fruit_pos[1] == position[1] and fruit_pos[0] < position[0] and current_direction in ('N', 'S'):
            return change_direction('E', len(snake), 20, current_pos, anterior_pos, fruit_pos, snake, "SWE")
        
        elif current_pos[1] == position[1] and fruit_pos[1] == position[1] and fruit_pos[0] > position[0] and current_direction in ('N', 'S'):
            return change_direction('W', len(snake), 20, current_pos, anterior_pos, fruit_pos, snake, "SWE")
        
    return current_direction

def check_position_out_of_board(current_pos, board_size):
    if 20 <= current_pos[0] and current_pos[0] <= board_size and 20 <= current_pos[1] and current_pos[1] <= board_size:
        print('!!!')
        return True
    return False

def set_direction(current_direction, snake_size, chunk, snake, current_pos, anterior_pos, fruit_pos, chosed):
    next_pos = [0, 0]
    if current_direction == 'W':
        next_pos[0] = current_pos[0] - chunk
        next_pos[1] = current_pos[1]
    elif current_direction == 'E':
        next_pos[0] = current_pos[0] + chunk
        next_pos[1] = current_pos[1]
    elif current_direction == 'N':
        next_pos[0] = current_pos[0]
        next_pos[1] = current_pos[1] - chunk
    elif current_direction == 'S':
        next_pos[0] = current_pos[0]
        next_pos[1] = current_pos[1] + chunk
    
    if (check_position_in(next_pos, snake) and check_position_out_of_board(next_pos, 400)):
        print('>:(')
        return current_direction
    else:
        chosed_copy = chosed[:]
        chosed_copy = find_and_remove(chosed_copy, current_direction)
        chosed_length = len(chosed_copy)
        if current_direction == 'N':
            exc = 'S'

        elif current_direction == 'S':
            exc = 'N'

        elif current_direction == 'W':
            exc = 'E'

        elif current_direction == 'E':
            exc = 'W'

        if chosed_length == 0:
            return current_direction
        
        return check_collision(current_direction, current_pos, anterior_pos, snake, fruit_pos)

def change_direction(current_direction, snake_size, chunk, current_pos, 
                    anterior_pos, fruit_pos, snake, chosed):
    print(f"CURRENT {current_direction}")
    print(f"CURRENT position {current_pos[0]} {current_pos[1]} CURRENT fruit {fruit_pos[0]} {fruit_pos[1]}")
    if calculate_distance(current_pos, fruit_pos) > calculate_distance(anterior_pos, fruit_pos):
        if current_pos[0] > fruit_pos[0] and current_direction in ('N', 'S'):
            result = set_direction('W', snake_size, chunk, snake, current_pos, anterior_pos, 
                                    fruit_pos, chosed)
            return result
        elif current_pos[0] < fruit_pos[0] and current_direction in ('N', 'S'):
            result = set_direction('E', snake_size, chunk, snake, current_pos, anterior_pos, 
                                    fruit_pos, chosed)
            return result
        elif current_pos[1] < fruit_pos[1] and current_direction in ('E', 'W'):
            result = set_direction('S', snake_size, chunk, snake, current_pos, anterior_pos, 
                                    fruit_pos, chosed)
            return result
        elif current_pos[1] > fruit_pos[1] and current_direction in ('E', 'W'):
            result = set_direction('N', snake_size, chunk, snake, current_pos, anterior_pos, 
                                    fruit_pos, chosed)
            return result

    elif current_pos[0] == fruit_pos[0]:
        if current_direction in ('E', 'W'):
            if current_pos[1] > fruit_pos[1]:
                return set_direction('N', snake_size, chunk, snake, current_pos, anterior_pos, fruit_pos, chosed)

            elif current_pos[1] < fruit_pos[1]:
                return set_direction('S', snake_size, chunk, snake, current_pos, anterior_pos, fruit_pos, chosed)

    elif current_pos[1] == fruit_pos[1]:
        if current_pos[0] > fruit_pos[0]:
            return set_direction('W', snake_size, chunk, snake, current_pos, anterior_pos, fruit_pos, chosed)

        elif current_pos[0] < fruit_pos[0]:
            return set_direction('E', snake_size, chunk, snake, current_pos, anterior_pos, fruit_pos, chosed)
    
    return set_direction(current_direction, snake_size, chunk, snake, current_pos, anterior_pos, 
                        fruit_pos, chosed)
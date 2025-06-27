import math
from typing import List, Tuple, Optional, Set

# Type aliases for better code documentation
Position = Tuple[int, int]
Direction = str
Snake = List[Position]
BoardSize = int

def calculate_distance(pos1: Position, pos2: Position) -> float:
    """Calculate Euclidean distance between two points."""
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

def remove_char(s: str, index: int) -> str:
    """Remove character at given index from string."""
    if 0 <= index < len(s):
        return s[:index] + s[index+1:]
    return s

def find_and_remove(s: str, item: str) -> str:
    """Find and remove first occurrence of item in string."""
    index = s.find(item)
    return remove_char(s, index) if index != -1 else s

def is_position_in_snake(head:Position, snake: Snake) -> bool:
    """Check if position collides with any snake segment except head."""
    return head in snake[:-1]


def calculate_distance(pos1: Position, pos2: Position) -> float:
    """Calculate Manhattan distance (faster than Euclidean for grid-based movement)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_collision_with_self(head: Position, snake_body: List[Position]) -> bool:
    """Check if head collides with any part of the snake's body"""
    return head in snake_body

def is_collision_with_wall(head: Position, board_size: BoardSize) -> bool:
    """Check if snake hits the wall"""
    x, y = head
    return x < 0 or x >= board_size or y < 0 or y >= board_size

def get_safe_directions(
    current_pos: Position,
    snake: Snake,
    chunk: int,
    board_size: BoardSize,
    forbidden_directions: Set[Direction]
) -> List[Direction]:
    """Get list of safe directions that won't cause immediate collision"""
    safe_directions = []
    
    for direction in ['N', 'S', 'E', 'W']:
        if direction in forbidden_directions:
            continue
            
        next_pos = get_next_position(current_pos, direction, chunk)
        
        if (not is_collision_with_self(next_pos, snake[:-1]) and 
            not is_collision_with_wall(next_pos, board_size)):
            safe_directions.append(direction)
    
    return safe_directions


def is_position_out_of_bounds(current_pos: Position, board_size: BoardSize) -> bool:
    """Check if position is outside game board boundaries."""
    return not (0 <= current_pos[0] < board_size and 0 <= current_pos[1] < board_size)

def find_best_avoidance_direction(
    current_pos: Position,
    snake: Snake,
    fruit_pos: Position,
    current_direction: Direction,
    chunk: int,
    board_size: BoardSize
) -> Optional[Direction]:
    """Find the best direction to avoid collisions while moving toward fruit"""
    forbidden = {current_direction, get_opposite_direction(current_direction)}
    safe_directions = get_safe_directions(current_pos, snake, chunk, board_size, forbidden)
    
    if not safe_directions:
        return None
    
    # Prioritize directions that move toward fruit
    direction_scores = []
    for direction in safe_directions:
        new_pos = get_next_position(current_pos, direction, chunk)
        score = calculate_distance(new_pos, fruit_pos)
        direction_scores.append((score, direction))
    
    # Return direction with lowest score (closest to fruit)
    return min(direction_scores, key=lambda x: x[0])[1]

def enhanced_check_collision(
    current_direction: Direction,
    current_pos: Position,
    snake: Snake,
    fruit_pos: Position,
    chunk: int = 20,
    board_size: int = 400
) -> Direction:
    """
    Enhanced collision detection that:
    1. Checks for immediate collisions
    2. Predicts future collisions in current path
    3. Finds safest alternative direction
    """
    # Check for immediate collision in current direction
    next_pos = get_next_position(current_pos, current_direction, chunk)
    
    if (not is_collision_with_self(next_pos, snake[:-1]) and 
        not is_collision_with_wall(next_pos, board_size)):
        
        # Check for potential collisions in path
        collision_points = get_potential_collisions(current_pos, snake, current_direction, chunk)
        if not collision_points:
            return current_direction
    
    # Find alternative safe direction
    avoidance_dir = find_best_avoidance_direction(
        current_pos, snake, fruit_pos, current_direction, chunk, board_size
    )
    
    return avoidance_dir if avoidance_dir is not None else current_direction


def get_next_position(current_pos: Position, direction: Direction, chunk: int) -> Position:
    """Calculate next position based on current direction."""
    x, y = current_pos
    return {
        'W': (x - chunk, y),
        'E': (x + chunk, y),
        'N': (x, y - chunk),
        'S': (x, y + chunk)
    }.get(direction, (x, y))

def get_opposite_direction(direction: Direction) -> Direction:
    """Get opposite direction to prevent 180-degree turns."""
    return {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}.get(direction, direction)

def set_direction(
    current_direction: Direction,
    snake: Snake,
    chunk: int,
    current_pos: Position,
    fruit_pos: Position,
    allowed_directions: str
) -> Direction:
    """Determine the best direction to move while avoiding collisions."""
    next_pos = get_next_position(current_pos, current_direction, chunk)
    
    # Check if next position is valid
    if (not is_position_in_snake(next_pos, snake) and 
        not is_position_out_of_bounds(next_pos, 400)):
        return current_direction
    
    # Remove current and opposite directions from allowed options
    opposite_dir = get_opposite_direction(current_direction)
    options = find_and_remove(allowed_directions, current_direction)
    options = find_and_remove(options, opposite_dir)
    
    print(options)
    if not options:
        return current_direction
    
    elif options: 
        print('TO PROVE')
        return find_best_avoidance_direction(options[0], current_pos, snake, fruit_pos)

    return check_collision(current_direction, current_pos, snake, fruit_pos)

def change_direction(
    current_direction: Direction,
    snake: Snake,
    chunk: int,
    current_pos: Position,
    previous_pos: Position,
    fruit_pos: Position,
    allowed_directions: str
) -> Direction:
    """Change direction based on fruit position and obstacles."""
    current_dist = calculate_distance(current_pos, fruit_pos)
    previous_dist = calculate_distance(previous_pos, fruit_pos)
    
    # If moving away from fruit, consider changing direction
    if current_dist > previous_dist:
        dx = fruit_pos[0] - current_pos[0]
        dy = fruit_pos[1] - current_pos[1]

        if dx < 0 and current_direction in ('N', 'S'):
            return set_direction('W', snake, chunk, current_pos, fruit_pos, allowed_directions)
        elif dx > 0 and current_direction in ('N', 'S'):
            return set_direction('E', snake, chunk, current_pos, fruit_pos, allowed_directions)
        elif dy > 0 and current_direction in ('E', 'W'):
            return set_direction('S', snake, chunk, current_pos, fruit_pos, allowed_directions)
        elif dy < 0 and current_direction in ('E', 'W'):
            return set_direction('N', snake, chunk, current_pos, fruit_pos, allowed_directions)

    # Special cases when aligned with fruit
    if current_pos[0] == fruit_pos[0] and current_direction in ('E', 'W'):
        if current_pos[1] > fruit_pos[1]:
            return set_direction('N', snake, chunk, current_pos, fruit_pos, allowed_directions)
        else:
            return set_direction('S', snake, chunk, current_pos, fruit_pos, allowed_directions)
    
    if current_pos[1] == fruit_pos[1] and current_direction in ('N', 'S'):
        if current_pos[0] > fruit_pos[0]:
            return set_direction('W', snake, chunk, current_pos, fruit_pos, allowed_directions)
        else:
            return set_direction('E', snake, chunk, current_pos, fruit_pos, allowed_directions)
    
    # Default case
    return set_direction(current_direction, snake, chunk, current_pos, fruit_pos, allowed_directions)
from typing import List, Tuple, Optional, Set
import math

# Type aliases
Position = Tuple[int, int]
Direction = str
Snake = List[Position]
BoardSize = int

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

def get_potential_collisions(
    current_pos: Position,
    snake: Snake,
    direction: Direction,
    chunk: int
) -> Set[Position]:
    """Get set of positions that would cause collisions in the current path"""
    next_pos = get_next_position(current_pos, direction, chunk)
    path_positions = set()
    
    # Check straight path in current direction
    x, y = current_pos
    if direction in ('N', 'S'):
        step = -chunk if direction == 'N' else chunk
        for dy in range(y + step, next_pos[1] + step, step):
            path_positions.add((x, dy))
    else:  # 'E' or 'W'
        step = chunk if direction == 'E' else -chunk
        for dx in range(x + step, next_pos[0] + step, step):
            path_positions.add((dx, y))
    
    # Return intersection with snake body
    snake_tuple = list(map(tuple, snake))
    return path_positions & set(snake_tuple[:-1])

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

# Helper functions (unchanged from original)
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
    # Use enhanced collision detection
    new_direction = enhanced_check_collision(
        current_direction,
        current_pos,
        snake,
        fruit_pos,
        chunk,
        400  # board_size
    )
    
    # Additional logic if needed
    if (current_pos[0] == fruit_pos[0] and current_direction in ('E', 'W')):
        if current_pos[1] > fruit_pos[1]:
            return enhanced_check_collision('N', current_pos, snake, fruit_pos)
        elif current_pos[1] < fruit_pos[1]:
            return enhanced_check_collision('S', current_pos, snake, fruit_pos)
    return new_direction
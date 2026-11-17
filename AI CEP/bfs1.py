from collections import deque

def bfs_pathfinding(grid_dimensions, obst_loc, start, goal):
    """
    Performs BFS pathfinding on a grid based on environment loader output.
    
    Parameters:
    - grid_dimensions: tuple (rows, cols) from env[0]
    - obst_loc: list of obstacle coordinate tuples from env[2]
    - start: tuple (r, c) representing the robot's current position
    - goal: tuple (r, c) representing the target dirt/charger location
    
    Returns:
    - A list of coordinate tuples [(r, c), ...] from start to goal, or None if unreachable.
    """
    rows, cols = grid_dimensions
    obstacles = set(obst_loc)
    
    if start == goal:
        return [start]
    
    # Queue stores tuples of (current_position, path_so_far)
    queue = deque([(start, [start])])
    visited = {start}
    
    # 4-way directional movement (Up, Down, Left, Right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
            
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            # Check grid boundaries, obstacle avoidance, and visited states
            if (0 <= nr < rows) and (0 <= nc < cols) and (neighbor not in obstacles) and (neighbor not in visited):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None  # Return None if no valid path exists
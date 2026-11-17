import time
from grid_render import render_grid
from collections import deque

def visualize_BFS(grid_dimensions, obst_loc, start, goal, dirts, cleaned_dirts, charge_loc, delay=0.15):
    """Performs BFS while rendering the frontier and visited nodes step-by-step."""
    rows, cols = grid_dimensions
    obstacles = set(obst_loc)

    if start == goal:
        return [start]

    queue = deque([(start, [start])])
    visited = {start}
    frontier = {start}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current, path = queue.popleft()
        frontier.discard(current)

        render_grid(
            rows, cols, obstacles, dirts, cleaned_dirts,
            robot_pos=start, charge_loc=charge_loc,
            frontier=frontier, visited=visited,
            status_msg=f"Searching for target {goal} | Exploring {current} | Queue size: {len(queue)}"
        )
        time.sleep(delay)

        if current == goal:
            return path

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if (0 <= nr < rows) and (0 <= nc < cols) and (neighbor not in obstacles) and (neighbor not in visited):
                visited.add(neighbor)
                frontier.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
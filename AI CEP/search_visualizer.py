import os
import sys
import time
from grid_render import render_grid
from bfs_demo import visualize_BFS
from env_loader1 import load_env

# Attempt to import load_env from env_loader1, with a fallback parser if run standalone
# try:
#     from env_loader1 import load_env
# except ImportError:
#     def load_env(filename):
#         """Fallback environment loader matching env_loader1.py format."""
#         try:
#             with open(filename, "r") as env_file:
#                 lines = env_file.read().splitlines()
#             grid_dimensions = eval('(' + lines[0] + ')')
#             obst_num = eval(lines[1])
#             obst_loc = [eval(x) for x in lines[2].split(', ')] if lines[2].strip() else []
#             dirt_num = eval(lines[3])
#             dirt_loc = [eval(x) for x in lines[4].split(', ')] if lines[4].strip() else []
#             charge_loc = eval(lines[5])
#             return (grid_dimensions, obst_num, obst_loc, dirt_num, dirt_loc, charge_loc)
#         except Exception as e:
#             print(f"Error loading environment: {e}")
#             return None


def animate_movement(grid_dimensions, obst_loc, path, dirts, cleaned_dirts, charge_loc, delay=0.25):
    """Animates the robot moving along the computed shortest path."""
    rows, cols = grid_dimensions
    obstacles = set(obst_loc)

    for step_idx, pos in enumerate(path):
        render_grid(
            rows, cols, obstacles, dirts, cleaned_dirts,
            robot_pos=pos, charge_loc=charge_loc,
            path=path[step_idx:],
            status_msg=f"Moving along shortest path: Step {step_idx + 1}/{len(path)} -> {pos}"
        )
        time.sleep(delay)


def select_environment_file():
    """Allows the programmer/user to pick an environment .txt file."""
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and 'env' in f.lower()]
    if not txt_files:
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]

    print("Available .txt files in current directory:")
    for idx, fname in enumerate(txt_files, 1):
        print(f"  {idx}. {fname}")

    choice = input("\nEnter environment filename (or number from list, default 'env1.txt'): ").strip()
    if not choice:
        return "env1.txt"
    if choice.isdigit() and 1 <= int(choice) <= len(txt_files):
        return txt_files[int(choice) - 1]
    return choice


def main():
    env_file = select_environment_file()
    if not os.path.exists(env_file):
        print(f"File '{env_file}' not found.")
        sys.exit(1)

    env_data = load_env(env_file)
    if not env_data:
        sys.exit(1)

    grid_dimensions, obst_num, obst_loc, dirt_num, dirt_loc, charge_loc = env_data
    rows, cols = grid_dimensions

    try:
        speed_input = input("Animation delay in seconds (default 0.15): ").strip()
        delay = float(speed_input) if speed_input else 0.15
    except ValueError:
        delay = 0.15

    current_pos = charge_loc
    cleaned_dirts = set()
    dirts_set = set(dirt_loc)

    render_grid(
        rows, cols, set(obst_loc), dirts_set, cleaned_dirts,
        robot_pos=current_pos, charge_loc=charge_loc,
        status_msg=f"Loaded '{env_file}'. Starting at charger {charge_loc}. Press Enter to begin..."
    )
    input()

    for idx, target_dirt in enumerate(dirt_loc, 1):
        path = visualize_BFS(
            grid_dimensions, obst_loc, current_pos, target_dirt,
            dirts_set, cleaned_dirts, charge_loc, delay=delay
        )

        if not path:
            render_grid(
                rows, cols, set(obst_loc), dirts_set, cleaned_dirts,
                robot_pos=current_pos, charge_loc=charge_loc,
                status_msg=f"FAILED: Dirt {idx} at {target_dirt} is unreachable!"
            )
            break

        animate_movement(
            grid_dimensions, obst_loc, path,
            dirts_set, cleaned_dirts, charge_loc, delay=delay
        )
        cleaned_dirts.add(target_dirt)
        current_pos = target_dirt

        render_grid(
            rows, cols, set(obst_loc), dirts_set, cleaned_dirts,
            robot_pos=current_pos, charge_loc=charge_loc,
            status_msg=f"Cleaned Dirt {idx}/{dirt_num} at {target_dirt}!"
        )
        time.sleep(0.6)

    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
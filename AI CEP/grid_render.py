import os

# ANSI Color Codes for Terminal Rendering
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ROBOT = "\033[96m"     # Bright Cyan
    CHARGER = "\033[93m"   # Bright Yellow
    DIRT = "\033[91m"      # Bright Red
    OBSTACLE = "\033[90m"  # Dark Grey / Dim
    PATH = "\033[92m"      # Bright Green
    FRONTIER = "\033[95m"  # Bright Magenta
    VISITED = "\033[37m"   # White / Dim
    CLEANED = "\033[32m"   # Green Dim


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def render_grid(rows, cols, obstacles, dirts, cleaned_dirts, robot_pos, charge_loc,
                frontier=None, visited=None, path=None, status_msg=""):
    """Renders the grid state in the terminal with ANSI colors."""
    frontier = frontier or set()
    visited = visited or set()
    path = set(path) if path else set()

    clear_screen()
    print("=" * (cols * 4 + 3))
    print(f"  {Colors.BOLD}AUTOMATED CLEANER ROBOT - SEARCH VISUALIZER{Colors.RESET}")
    print("=" * (cols * 4 + 3))
    print(f"Legend: {Colors.ROBOT}[R] Robot{Colors.RESET}  {Colors.CHARGER}[C] Charger{Colors.RESET}  {Colors.DIRT}[D] Dirt{Colors.RESET}  {Colors.CLEANED}[*] Cleaned{Colors.RESET}")
    print(f"        {Colors.OBSTACLE}[#] Wall{Colors.RESET}   {Colors.PATH}[+] Path{Colors.RESET}     {Colors.VISITED}[.] Seen{Colors.RESET}  {Colors.FRONTIER}[?] Frontier{Colors.RESET}\n")

    # Column headers
    header = "    " + " ".join(f"{c:2d} " for c in range(cols))
    print(header)
    print("   +" + "---+" * cols)

    for r in range(rows):
        row_str = f"{r:2d} |"
        for c in range(cols):
            pos = (r, c)
            if pos == robot_pos:
                cell = f"{Colors.ROBOT}{Colors.BOLD} R {Colors.RESET}"
            elif pos in obstacles:
                cell = f"{Colors.OBSTACLE} # {Colors.RESET}"
            elif pos in dirts and pos not in cleaned_dirts:
                cell = f"{Colors.DIRT}{Colors.BOLD} D {Colors.RESET}"
            elif pos == charge_loc:
                cell = f"{Colors.CHARGER}{Colors.BOLD} C {Colors.RESET}"
            elif pos in path:
                cell = f"{Colors.PATH} + {Colors.RESET}"
            elif pos in frontier:
                cell = f"{Colors.FRONTIER} ? {Colors.RESET}"
            elif pos in visited:
                cell = f"{Colors.VISITED} . {Colors.RESET}"
            elif pos in cleaned_dirts:
                cell = f"{Colors.CLEANED} * {Colors.RESET}"
            else:
                cell = "   "
            row_str += cell + "|"
        print(row_str)
        print("   +" + "---+" * cols)

    print(f"\n{Colors.BOLD}Status:{Colors.RESET} {status_msg}")
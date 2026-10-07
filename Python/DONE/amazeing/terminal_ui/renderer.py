import sys
import time
from .terminal_utils import (
    check_terminal_size,
    clear_screen,
    get_char,
    kbhit,
    setup_terminal,
    restore_terminal,
    flush_input,
)
from maze_generator import MazeGenerator
from maze_generator.models import DIRECTIONS

# aNSI Colors for terminal styling
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

COLORS = [WHITE, CYAN, MAGENTA, YELLOW, GREEN, RED]

# unicode Box Drawing Character Maps (N, S, E, W)
BOX_STANDARD = {
    (False, False, False, False): " ",
    (True, False, False, False): "╵",
    (False, True, False, False): "╷",
    (False, False, True, False): "╶",
    (False, False, False, True): "╴",
    (True, True, False, False): "│",
    (False, False, True, True): "─",
    (False, True, True, False): "┌",
    (False, True, False, True): "┐",
    (True, False, True, False): "└",
    (True, False, False, True): "┘",
    (True, True, True, False): "├",
    (True, True, False, True): "┤",
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, True, True): "┼",
}

BOX_DOUBLE = {
    (False, False, False, False): " ",
    (True, False, False, False): "║",
    (False, True, False, False): "║",
    (False, False, True, False): "═",
    (False, False, False, True): "═",
    (True, True, False, False): "║",
    (False, False, True, True): "═",
    (False, True, True, False): "╔",
    (False, True, False, True): "╗",
    (True, False, True, False): "╚",
    (True, False, False, True): "╝",
    (True, True, True, False): "╠",
    (True, True, False, True): "╣",
    (False, True, True, True): "╦",
    (True, False, True, True): "╩",
    (True, True, True, True): "╬",
}

BOX_THICK = {
    (False, False, False, False): " ",
    (True, False, False, False): "╹",
    (False, True, False, False): "╻",
    (False, False, True, False): "╺",
    (False, False, False, True): "╸",
    (True, True, False, False): "┃",
    (False, False, True, True): "━",
    (False, True, True, False): "┏",
    (False, True, False, True): "┓",
    (True, False, True, False): "┗",
    (True, False, False, True): "┛",
    (True, True, True, False): "┣",
    (True, True, False, True): "┫",
    (False, True, True, True): "┳",
    (True, False, True, True): "┻",
    (True, True, True, True): "╋",
}

BOX_ROUNDED = {
    (False, False, False, False): " ",
    (True, False, False, False): "╵",
    (False, True, False, False): "╷",
    (False, False, True, False): "╶",
    (False, False, False, True): "╴",
    (True, True, False, False): "│",
    (False, False, True, True): "─",
    (False, True, True, False): "╭",
    (False, True, False, True): "╮",
    (True, False, True, False): "╰",
    (True, False, False, True): "╯",
    (True, True, True, False): "├",
    (True, True, False, True): "┤",
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, True, True): "┼",
}

STYLES = [
    ("Double", BOX_DOUBLE),
    ("Rounded", BOX_ROUNDED),
    ("Thick", BOX_THICK),
    ("Standard", BOX_STANDARD),
]


def render_frame(
    generator: MazeGenerator,
    path_sequence: list,
    path_progress: int,
    show_path: bool,
    animating_path: bool,
    path_speed: float,
    style_idx: int,
    color_idx: int,
) -> None:
    grid = generator.grid_manager
    width = grid.width
    height = grid.height

    physical_cols = width * 3 + 1
    req_lines = height * 2 + 7

    is_ok, cols, lines = check_terminal_size(physical_cols + 1, req_lines + 1)
    if not is_ok:
        sys.stdout.write("\033[H\033[J")
        print(
            f"Terminal too small!\nRequired: {physical_cols+1}x{req_lines+1}"
            f"\nCurrent: {cols}x{lines}\nPlease resize your terminal."
        )
        sys.stdout.flush()
        return

    # build an intermediate boolean matrix for walls
    is_wall = [
        [False for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)
    ]
    for y in range(height + 1):
        for x in range(width + 1):
            is_wall[y * 2][x * 2] = True  # structural intersections

    for y in range(height):
        for x in range(width):
            cx, cy = x * 2 + 1, y * 2 + 1
            if grid.grid[y][x]["N"]:
                is_wall[cy - 1][cx] = True
            if grid.grid[y][x]["S"]:
                is_wall[cy + 1][cx] = True
            if grid.grid[y][x]["W"]:
                is_wall[cy][cx - 1] = True
            if grid.grid[y][x]["E"]:
                is_wall[cy][cx + 1] = True

    path_set = set()
    head = None
    if animating_path:
        path_set = set(path_sequence[:path_progress])
        head = path_sequence[path_progress - 1] if path_progress > 0 else None
    elif show_path:
        path_set = set(path_sequence)
        head = path_sequence[-1] if path_sequence else None

    style_name, char_map = STYLES[style_idx % len(STYLES)]
    wall_color = COLORS[color_idx % len(COLORS)]

    rows_output = []
    for y in range(height * 2 + 1):
        row_str = ""
        for x in range(width * 2 + 1):
            if is_wall[y][x]:
                # determine connections
                n = y > 0 and is_wall[y - 1][x]
                s = y < height * 2 and is_wall[y + 1][x]
                e = x < width * 2 and is_wall[y][x + 1]
                w = x > 0 and is_wall[y][x - 1]

                char = char_map.get((n, s, e, w), " ")
                colored_char = f"{wall_color}{char}{RESET}"

                if x % 2 == 0:
                    row_str += colored_char
                else:
                    # stretch horizontal lines
                    row_str += colored_char * 2
            else:
                # empty space / path / entry / exit
                maze_x, maze_y = x // 2, y // 2
                is_interior = (x % 2 == 1) and (y % 2 == 1)

                is_pattern = (
                    is_interior and (maze_x, maze_y) in grid.pattern_cells
                )
                is_entry = is_interior and (maze_x, maze_y) == grid.entry
                is_exit = is_interior and (maze_x, maze_y) == grid.exit

                if (
                    (x, y) in path_set
                    and not is_pattern
                    and not is_entry
                    and not is_exit
                ):
                    if (x, y) == head and animating_path:
                        if x % 2 == 0:
                            row_str += f"{GREEN}⬤{RESET}"
                        else:
                            row_str += f"{GREEN}⬤ {RESET}"
                    else:
                        if x % 2 == 0:
                            row_str += f"{BLUE}█{RESET}"
                        else:
                            row_str += f"{BLUE}██{RESET}"
                else:
                    if x % 2 == 0:
                        row_str += " "
                    else:
                        if is_pattern:
                            row_str += f"{wall_color}██{RESET}"
                        elif is_entry:
                            row_str += f"{MAGENTA}██{RESET}"
                        elif is_exit:
                            row_str += f"{RED}██{RESET}"
                        else:
                            row_str += "  "
        rows_output.append(row_str)

    # move cursor to top-left instead of full clear to prevent flickering
    sys.stdout.write("\033[H")
    for row in rows_output:
        print(row + "\033[K")

    print("\033[K")  # empty line
    print("=" * physical_cols + "\033[K")
    if animating_path:
        print(f"A-Maze-ing - Solving... | Speed: {path_speed:.2f}s/step\033[K")
        print("[-] Slower | [+] Faster | [5] Stop Animation\033[K")
    else:
        print(f"A-Maze-ing - Interactive Viewer | Style: {style_name}\033[K")
        print(
            "[1] Regen | [2] Toggle Path | [3] Style"
            "| [4] Color | [5] Animate | [Q] Quit\033[K"
        )
    print("=" * physical_cols + "\033[K\033[J", end="", flush=True)
    sys.stdout.flush()


def interactive_loop(generator: MazeGenerator) -> None:
    """runs the live terminal rendering loop handling user input."""
    sys.stdout.write("\033[?25l")  # hide cursor for visual aesthetics
    sys.stdout.flush()
    setup_terminal()
    try:
        show_path = False
        animating_path = False
        path_progress = 0
        path_speed = 0.05  # seconds per step

        style_idx = 0
        color_idx = 0

        cheat_buffer = ""
        # EASTER EGG FOUND
        mastoof_mode = False

        import shutil

        clear_screen()  # ensure clean slate before rendering
        last_size = (0, 0)

        def calculate_path() -> list[tuple[int, int]]:
            seq: list[tuple[int, int]] = []
            try:
                from maze_generator.solver import MazeSolver

                current = generator.grid_manager.entry
                seq.append((current[0] * 2 + 1, current[1] * 2 + 1))
                for direction in MazeSolver.solve(generator.grid_manager):
                    dx, dy, _ = DIRECTIONS[direction]
                    seq.append(
                        (current[0] * 2 + 1 + dx, current[1] * 2 + 1 + dy)
                    )
                    current = (current[0] + dx, current[1] + dy)
                    seq.append((current[0] * 2 + 1, current[1] * 2 + 1))
            except ValueError:
                pass
            return seq

        path_sequence = calculate_path()

        while True:
            curr_size = shutil.get_terminal_size()
            if (curr_size.columns, curr_size.lines) != last_size:
                clear_screen()
                last_size = (curr_size.columns, curr_size.lines)

            render_frame(
                generator,
                path_sequence,
                path_progress,
                show_path,
                animating_path,
                path_speed,
                style_idx,
                color_idx,
            )
            # so funny
            if mastoof_mode:
                color_idx = (color_idx + 1) % len(COLORS)
                style_idx = (style_idx + 1) % len(STYLES)

            char = None
            if animating_path:
                start = time.time()
                while time.time() - start < path_speed:
                    if kbhit():
                        char = get_char()
                        if char == "+":
                            path_speed = max(0.01, path_speed - 0.02)
                            char = None
                        elif char == "-":
                            path_speed = min(0.5, path_speed + 0.02)
                            char = None
                        else:
                            break
                    time.sleep(0.01)

                if not char:
                    path_progress += 1
                    if path_progress >= len(path_sequence):
                        animating_path = False
                        show_path = True
            else:
                # 10 FPS idle refresh to continuously
                # check for terminal resizes
                start = time.time()
                while time.time() - start < 0.1:
                    if kbhit():
                        char = get_char()
                        break
                    if mastoof_mode:
                        time.sleep(0.03)  # cap disco speed to ~30 FPS
                        break
                    time.sleep(0.01)

            if char:
                cheat_buffer += char
                if len(cheat_buffer) > 7:
                    cheat_buffer = cheat_buffer[-7:]
                if cheat_buffer == "mastoof":
                    mastoof_mode = not mastoof_mode
                    cheat_buffer = ""

                if char == "1" and not animating_path:
                    try:
                        generator.generate()
                        path_sequence = calculate_path()
                        show_path = False
                        animating_path = False
                        path_progress = 0
                        flush_input()
                    except ValueError:
                        pass
                elif char == "2" and not animating_path:
                    animating_path = False
                    show_path = not show_path
                    path_progress = len(path_sequence) if show_path else 0
                elif char == "5":
                    if path_sequence and not animating_path:
                        show_path = False
                        animating_path = True
                        path_progress = 1
                    elif animating_path:
                        animating_path = False
                elif char == "+":
                    path_speed = max(0.01, path_speed - 0.02)
                elif char == "-":
                    path_speed = min(0.5, path_speed + 0.02)
                elif char == "3" and not animating_path:
                    style_idx += 1
                elif char == "4" and not animating_path:
                    color_idx += 1
                elif char == "q":
                    clear_screen()
                    print("Exiting A-Maze-ing...")
                    break
    except KeyboardInterrupt:
        clear_screen()
        print("Exiting A-Maze-ing...")
    finally:
        restore_terminal()
        sys.stdout.write("\033[?25h")  # show cursor
        sys.stdout.flush()

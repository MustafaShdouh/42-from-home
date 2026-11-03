*This activity has been created as part of the 42 curriculum by mel-shdo, adnasser.*

## Description
A-Maze-ing is a highly optimized maze generator and interactive terminal visualizer. It parses a configuration file to generate either a perfect maze (one unique path) or a playable Pac-Man-like board with loops. The project features a robust Pydantic-based configuration parser, a reusable `maze_generator` module, and a sophisticated cross-platform ASCII rendering engine that provides live terminal resizing, multiple visual styles, neon colors, and an animated path solver.

## Instructions
**Requirements:** Python 3.10+

**Installation:**
```bash
make install
```

**Execution:**
Run the program by passing a valid configuration file:
```bash
make run
# or
python3 a_maze_ing.py config.txt
```

**Interactive Controls:**
Once the maze is generated, use the following keys in the terminal:
- `1`: Re-generate a new maze
- `2`: Toggle shortest path visibility
- `3`: Cycle through rendering styles (Double, Rounded, Thick, Standard)
- `4`: Cycle through maze colors
- `5`: Toggle the animated path solver
- `+` / `-`: Speed up or slow down the animation
- `Q`: Quit

## Config File Format
The configuration file requires one `KEY=VALUE` pair per line. Lines starting with `#` are ignored.
```ini
WIDTH=40          # Maze width (min 9, max 40)
HEIGHT=20         # Maze height (min 7, max 20)
ENTRY=0,0         # Entry coordinates (x,y)
EXIT=39,19        # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt   # Output filename (saved in hexadecimal format)
PERFECT=True      # True for a perfect maze, False for playable board
```

## Maze Generation Algorithm
This project utilizes **Kruskal's Algorithm** (via a randomized Union-Find disjoint set data structure) to generate the maze. 

### Why this algorithm?
Kruskal's algorithm is exceptionally well-suited for this project because it guarantees a perfect, unbiased spanning tree (a perfect maze). By randomly selecting walls (edges) and only knocking them down if they connect two disjoint sets, we inherently avoid isolated cells and loops. Furthermore, for the imperfect (Pac-Man) mode, we can simply continue the algorithm past the spanning tree phase to selectively knock down additional walls while respecting the `3x3` open area constraint.

## Reusable Code
The entire maze generation logic has been decoupled from the visualizer and encapsulated into a standalone `maze_generator` package.

**How to reuse it:**
The module can be built into a `.whl` or `.tar.gz` and installed via `pip`.
```python
from maze_generator import MazeGenerator
from maze_generator.solver import MazeSolver

# 1. Instantiate the generator (width, height, entry, exit, perfect, seed)
generator = MazeGenerator(20, 20, (0,0), (19,19), True, 42)

# 2. Generate the maze and export
generator.generate()
generator.write_output("out.txt")

# 3. Access the generated structure and solution
grid = generator.grid_manager
solution_path = MazeSolver.solve(grid)
```

## Advanced Features
- **Live Terminal Resizing**: The terminal renderer uses `shutil` and ANSI cursor snapping (`\033[H`) to dynamically adapt to window resizing without flickering or breaking the frame buffer.
- **Cross-Platform Asynchronous Input**: Uses `msvcrt` on Windows and `tty`/`termios` on Linux to capture keystrokes in real-time without blocking the animation loop.
- **Raycasted Solid Geometry**: The famous "42" pattern is rendered by mathematically evaluating high-resolution sub-grid coordinates to create a perfectly solid, contiguous block of color that seamlessly swallows its own internal walls while perfectly maintaining its external boundaries.

## Team and Project Management
- **Roles**: Mustafa decided what system architecture we are going to use and the repositoty structure. He also worked on the maze parser and maze renderer. Adel did the maze generator class with all of it's packegized features, he also worked on the makefile and license and decided the method of making the whl file.
- **Planning**: The project started with the configuration parser, moved to the backend Union-Find generator, and finished with the frontend interactive ASCII renderer.
- **Successes/Improvements**: The integration of Pydantic for validation made error handling incredibly clean. Terminal rendering required complex math for the sub-grid expansion and ANSI escape codes to prevent ghosting, which was a great learning experience.
- **Specific Tools**: Python, Pydantic, Make, Git.

## Resources
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Disjoint-set data structure (Union-Find)](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- **AI Usage**: AI was used as a pair-programmer throughout this activity. Specifically, it assisted in refactoring the configuration parser to use `Pydantic`, designing the mathematical 2x resolution grid expansion for the ASCII rendering engine, implementing the non-blocking cross-platform terminal input loop, and debugging complex terminal UI artifacts like text ghosting and screen flickering. All AI-generated code was actively reviewed and tested.

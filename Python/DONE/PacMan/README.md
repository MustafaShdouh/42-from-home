*This activity has been created as part of the 42 curriculum by mel-shdo, adnasser.*

## Description
This project recreates **Pac-Man** in Python for the 42 School curriculum. It uses Object-Oriented Programming (OOP) and a modular architecture divided between backend logic (`core/`) and graphical presentation (`ui/`). Ghost targeting is inspired by the arcade game, with adjustments for procedural mazes.

The game incorporates procedural maze generation via an external `A-Maze-ing` package, authentic ghost AI targeting strategies (Blinky, Pinky, Inky, Clyde), 7-phase Scatter/Chase wave cycles, Cruise Elroy dynamic speed scaling, a persistent top-10 highscore system, and comprehensive peer-review cheat controls.

---

## Instructions

### Requirements
* Python 3.10 or later
* Pygame 2.0+
* The assigned `mazegenerator` wheel in `mazegenerator-00001/`
* GNU Make and a POSIX shell for the Makefile (for example, Git Bash with Make installed on Windows)

`make install` installs the supplied wheel without changing its source. Other dependencies require access to a package index. You can select an interpreter with `make PYTHON=python install`.

### Execution via Makefile
A `Makefile` is provided to automate dependency installation, linting, execution, and packaging:

```bash
# 1. Install dependencies
make install

# 2. Run the game with default config
make run

# 3. Run with Python's built-in debugger (pdb)
make debug

# 4. Enforce strict flake8 and mypy type checking
make lint
make lint-strict

# 5. Clean up caches and temporary files
make clean

# 6. Build standalone executable
make package
```

### Direct Command-Line Usage
Per Section 5.1 of the 42 subject, the game is launched with exactly one configuration file argument:

```bash
python3 pac-man.py config.json
```

The entry point validates arguments before importing the UI. Missing graphical dependencies produce a logged error and a nonzero exit status. It does not report a headless simulation as a successful game launch.

### Packaged build

`make package CONFIG=config.json` uses the root `PacMan.spec` recipe. You can use `make package CONFIG=other.json` to package a different configuration. The selected file is copied to `dist/config.json` and is the editable runtime configuration used by the packaged executable. `core/packaging_hook.py` supplies that adjacent configuration path if the executable is started with no arguments (for example by double-clicking). It bundles the renderer, the assigned generator, and package data, and copies editable `config.json` and these instructions beside the executable in `dist/`. Build separately on each target operating system.

From the distribution directory, launch with `./run-pacman.sh` or `./PacMan config.json` on Linux or `PacMan.exe config.json` on Windows. Keep that directory writable so the default highscore file can be saved. Controls are listed below; change game options by editing `config.json` before launching.

Before uploading the contents of `dist/` as a free private/unlisted build, test the executable on a machine without the source checkout. Packaging and platform deployment remain release checks; a build recipe alone does not establish that they passed.

---

## Controls & Cheat Modes

### Standard Gameplay Controls
| Action | Primary Key | Alternate Key |
|---|---|---|
| **Move UP** | `UP Arrow` | `W` |
| **Move DOWN** | `DOWN Arrow` | `S` |
| **Move LEFT** | `LEFT Arrow` | `A` |
| **Move RIGHT** | `RIGHT Arrow` | `D` |
| **Pause / Resume** | `P` | `ESCAPE` |
| **Start Game (Menu)** | `SPACE` | Mouse Click |

### Peer-Review Cheat Modes (Section 6.5)
To facilitate thorough peer-evaluation defense, the following real-time cheats are available during active gameplay:

| Key | Cheat Function | Description |
|---|---|---|
| `C` / `I` | **Invincibility** | Pac-Man cannot be killed by ghosts; passes harmlessly through active ghosts. |
| `L` | **Level Skip** | Instantly wins the current level and advances to the next stage. |
| `F` | **Ghost Freeze** | Freezes all ghost movement and timers while Pac-Man navigates freely. |
| `E` | **Extra Life** | Adds +1 life to the player's remaining life counter. |
| `B` | **Speed Boost** | Accelerates Pac-Man's movement speed to 14.0 tiles/sec (toggle back to 8.0). |

---

## Resources

* **The Pac-Man Dossier (Jamey Pittman):** Primary reference for authentic ghost targeting vectors, 7-phase Scatter/Chase wave durations, and Cruise Elroy dot count thresholds.
* **Original Namco Z80 Arcade Disassembly:** Used to verify authentic ghost AI decision trees, tile intersection priorities, and pixel-to-tile coordinate transformations.
* **`pacman-c` GitHub Repository:** Reference C translation of the original arcade ROM used to reverse-engineer Cruise Elroy acceleration formulas and frightened ghost PRNG behavior.
* **AI Assistant Usage:** Google Antigravity (Agentic AI) was utilized as an engineering pair-programmer for:
  * Deconstructing the original arcade assembly logic into clean Gang of Four (GoF) design patterns.
  * Writing unit tests and running automated bug bounties to eliminate quantum phasing and sprite jitter.
  * Verifying strict compliance with PEP 8 / `flake8` line lengths ($\le 79$ characters) and PEP 257 Google docstrings.
  * Configuring Makefile automation and PyInstaller packaging pipelines.
* **Codex review and fixes:** Compared backend behavior with the subject, corrected configuration validation, center spawning, frightened navigation, persistence and lint commands, and ran temporary backend regression checks. Full flake8/mypy execution and UI compliance remain separate checks.

---

## Configuration

The game engine relies on a user-supplied JSON configuration file (`config.json`).
Full lines beginning with `#` or `//` are treated as comments and ignored, as required by the subject. Quoted JSON keys such as `"# note"` are handled as ordinary unknown keys and ignored; they do not cause the rest of the line to be stripped.

### Fault Tolerance & Bounds Clamping (Section 5.3)
If any key is missing, invalid, or out of bounds, the loader logs a clear warning and safely falls back to robust defaults without throwing a Python traceback:
* `lives`: Must be $\ge 1$ (defaults to `3`).
* `level_max_time`: Must be finite and $> 0.0$ (defaults to `90.0` seconds).
* `points_per_pacgum`, `points_per_super_pacgum`, `points_per_ghost`: Non-negative integers ($\ge 0$).
* `width`, `height`: Integers from `5` to `100`; invalid dimensions independently fall back to `15`. The upper bound limits memory use during generation.
* `level`: At least 10 nonempty string or integer labels (booleans are rejected). Labels determine the number of generated levels; they are not file paths.
* `seed`: A positive integer (`42` by default) for the first level. Zero and negative values fall back to `42`; later levels use the generator's random mode.
* Numeric keys reject booleans. Unknown keys are ignored, and a non-object JSON root falls back to defaults with an error message.

The complete backend defaults are:

| Key | Default | Meaning |
|---|---|---|
| `highscore_filename` | `"highscores.json"` | Save path relative to the launch directory; blank and NUL-containing paths use the default. |
| `level` | `["level1", ..., "level10"]` | Progression labels; at least ten entries. |
| `width`, `height` | `15`, `15` | External maze cells; block-grid dimensions are `2 * cells + 1`. |
| `lives` | `3` | Initial lives, at least one. |
| `points_per_pacgum` | `10` | Non-negative integer dot reward. |
| `points_per_super_pacgum` | `50` | Non-negative integer power-pellet reward. |
| `points_per_ghost` | `200` | Non-negative integer edible-ghost reward. |
| `seed` | `42` | Fixed first-level seed. |
| `level_max_time` | `90.0` | Positive finite level time in seconds. |
| `pacgum` | `10` | Legacy accepted value; dot placement fills corridors and scoring uses `points_per_pacgum`. |
| `enable_42` | `true` | Compatibility flag retained by the adapter; the supplied generator controls its own logo. |

```json
{
    # Highscore file location
    "highscore_filename": "highscores.json",
    
    # Progression levels (minimum 10 levels)
    "level": ["level1", "level2", "level3", "level4", "level5",
              "level6", "level7", "level8", "level9", "level10"],
    
    # Core gameplay parameters
    "lives": 3,
    "level_max_time": 90.0,
    "seed": 42,
    
    # Maze dimensions (passed to external generator)
    "width": 15,
    "height": 15,
    
    # Scoring metrics
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200
}
```

---

## Highscore System

The persistent highscore system saves the **Top 10** scores to `highscores.json`.
* **File errors:** Reads and writes handle filesystem, invalid-path, encoding, and JSON errors with clear messages. A missing file starts an empty leaderboard. Saves write a temporary file, flush it, and replace the destination atomically; a failed replacement preserves the previous file and cleans up the temporary file.
* **Data Sanitization:** Player names are filtered via Regex (`[^a-zA-Z0-9 ]`) and limited to 10 characters (defaulting to `"ANONYMOUS"`). Loaded scores must be non-negative integers; booleans, fractions, numeric strings, and negative values are rejected. Valid scores are saved without an artificial upper cap.
* **Name Entry:** Players enter their name upon completing the game (Win or Game Over) before returning to the main menu.

JSON keeps the leaderboard human-readable and needs no database. Atomic replacement reduces the risk of corrupting an existing leaderboard during a failed save. If saving fails, the game retains the updated in-memory leaderboard and returns to the menu.

---

## Maze Generation

Mazes are generated using the assigned external `A-Maze-ing` package without modifying third-party source code:
* **Adapter Pattern (`MazeAdapter` in `core/maze_loader.py`):** Translates third-party bitmask corridor arrays into a physical grid of walls (`1`), corridors (`0`), dots (`2`), and Super Pacgums (`3`).
* **Corridor Carving:** Mazes are generated with `perfect=False` to produce authentic intersecting corridors.
* **Deterministic vs Random:** Level 1 uses the configured positive seed (`42` by default) for reproducibility. All subsequent levels (2-10+) use random mode (`seed = 0`).
* **Key Item Placement:** Super Pacgums and Ghosts occupy the four corners. Pac-Man starts and respawns on the existing corridor nearest the geometric center, exactly at `(15, 15)` for the default 31-by-31 block grid. If the center is a wall, the adapter preserves the supplied maze and uses the nearest walkable tile.
* **Failure Handling:** Empty, malformed, or blocked-corner output and generator exceptions use a small static fallback maze. The fallback is not another procedural generator.

---

## Implementation

* **Fixed-Timestep Accumulator:** The physics loop runs on a decoupled fixed-timestep accumulator (60 FPS physics), preventing speed inconsistencies across varying monitor refresh rates.
* **Sub-Tile Visual Interpolation:** Entities maintain `prev_x, prev_y` and compute continuous `render_x, render_y` coordinates, providing fluid 60 FPS sprite motion.
* **Continuous Hitbox Collision:** Collisions use sub-tile distances (`dx < 0.45 and dy < 0.45`) plus a head-on crossing check.
* **Frightened Navigation:** Edible ghosts maximize shortest-path corridor distance from Pac-Man. They may reverse direction to flee and choose randomly only between equally distant options. A dead end can force a move toward the player.
* **Ghost Return-to-Base Navigation:** Eaten ghosts use BFS to return to their own corner at twice their level-dependent base speed, wait three seconds after arrival, and revive. A 25-second return timeout relocates a stuck ghost to its corner. The subject's five- or ten-second recovery times are examples, not mandatory constants.
* **New Games and Respawns:** A new game clears cheat toggles and temporary freezes. Life loss resets player interpolation and ghost recovery state while preserving eaten dots and score.

---

## General Software Architecture

The codebase enforces a strict 50/50 division contract separating backend core logic from UI presentation:

```
PacMan/
├── pac-man.py              # Main entry point, CLI validation & orchestration
├── config.json             # Game configuration with comment support
├── Makefile                # Build automation (install, run, lint, package)
├── PacMan.spec             # PyInstaller packaging specification
├── core/                   # Mustafa's Backend Domain
│   ├── config.py           # JSON loader, comment handling & validation
│   ├── packaging_hook.py   # PyInstaller startup hook for external config
│   ├── game_state.py       # Central context and state machine coordinator
│   ├── maze_loader.py      # GoF Adapter for external A-Maze-ing generator
│   ├── player.py           # Pac-Man physics, cornering & dot eating
│   ├── ghost.py            # Ghost state machine (Chase, Scatter, Frightened, Dead)
│   ├── event_bus.py        # GoF Observer pattern event dispatcher
│   ├── score_manager.py    # Observer-driven scoring calculator
│   ├── ai/                 # GoF Strategy pattern ghost targeting algorithms
│   └── states/             # GoF State pattern (Menu, Playing, Paused, GameOver, Victory)
├── ui/                     # Adel's Frontend Domain
│   ├── renderer.py         # Pygame window loop and frame orchestration
│   ├── input_handler.py    # Keyboard & mouse event router (WASD, cheats)
│   ├── game_view.py        # Maze, HUD overlay & animated sprite rendering
│   ├── menu.py             # Main menu screen with "Push SPACE to play"
│   ├── pause_menu.py       # In-game pause overlay
│   ├── game_over.py        # Game over screen with highscore text input
│   ├── victory.py          # Victory screen with congratulatory display
│   ├── highscores.py       # Top 10 highscore leaderboard view
│   └── instructions.py     # How-to-play instructions screen
└── project_management/     # Chapter 8 Deliverables
    ├── timeline.md         # Gantt chart, milestones & progress tracking
    ├── risk_analysis.md    # Risk matrix, failure modes & mitigations
    ├── team_organization.md# Roles, API contracts & conflict resolution
    └── acceptance_test_plan.md # 42 Subject verification matrix & bug log
```

---
## Download

The Linux version is available on itch.io:

https://adnasser42.itch.io/pacman-42

## Project Management

Project management was conducted using an Agile methodology with weekly sprint tracking, architectural decision records (ADRs), and continuous risk mitigation. All project management artifacts required by Chapter 8 are maintained in the dedicated [`project_management/`](project_management/) directory:
* [Timeline and Gantt Schedule](project_management/timeline.md)
* [Risk Analysis and Mitigation Matrix](project_management/risk_analysis.md)
* [Team Organization and Interface Contracts](project_management/team_organization.md)
* [Acceptance Test Plan and Verification Matrix](project_management/acceptance_test_plan.md)

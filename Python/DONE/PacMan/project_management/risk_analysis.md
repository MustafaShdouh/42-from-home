# Risk Analysis and Mitigation Strategies

*Activity: Pac-Man (42 School Curriculum)*  
*Authors: mel-shdo (Mustafa), adnasser (Adel)*

---

## 1. Risk Management Framework

To guarantee strict compliance with 42 School evaluation criteria (zero unhandled exceptions, zero crashes, robust fault tolerance, strict code styling), we established a proactive Risk Management Framework. Risks were classified by Probability ($P$) and Impact ($I$) on a 1–5 scale, yielding a composite Risk Priority Number ($RPN = P \times I$).

---

## 2. Risk Matrix

| Risk ID | Category | Description | $P$ | $I$ | $RPN$ | Status |
|---|---|---|---|---|---|---|
| **R-01** | Architecture | Unhandled exceptions causing program crash during defense | 4 | 5 | **20** | Mitigated |
| **R-02** | Physics | Quantum phasing (Pac-Man & ghosts passing through each other) | 4 | 4 | **16** | Mitigated |
| **R-03** | Stability | Ghost jitter / freak-out when reaching corners or spawn house | 4 | 3 | **12** | Mitigated |
| **R-04** | Compatibility | Malformed or corrupted external config / highscores JSON files | 5 | 4 | **20** | Mitigated |
| **R-05** | Integration | External `A-Maze-ing` package interface changes or failures | 3 | 4 | **12** | Mitigated |
| **R-06** | Code Quality | Norm violations (`flake8` >79 chars, mypy typing errors, `# type: ignore`) | 4 | 5 | **20** | Mitigated |
| **R-07** | Team | Desynchronization between Core simulation and UI rendering | 3 | 4 | **12** | Mitigated |

---

## 3. Detailed Risk Analysis & Implemented Mitigations

### R-01: Unhandled Exceptions & Traceback Prevention (Subject Section 3.1 & 5.1)
- **Risk:** Any uncaught Python exception results in an immediate failure during the 42 peer-evaluation defense.
- **Root Causes:** Missing files, invalid CLI arguments, JSON decode errors, division by zero in timer calculations, array index out-of-bounds.
- **Mitigation Strategy:**
  1. Top-level CLI wrapper in `pac-man.py` catches all unexpected errors gracefully and logs clear messages to `stderr` with exit code 1.
  2. All file I/O operations are enclosed in strict `try-except (OSError, json.JSONDecodeError)` blocks with safe fallback defaults.
  3. Continuous testing using automated malformed input scripts.

### R-02: Quantum Phasing & Grid Collision Integrity
- **Risk:** Fast-moving entities (especially under Speed Boost cheats or Cruise Elroy) swapping tiles in a single frame without triggering a collision.
- **Root Causes:** Discrete frame updates checking only current tile coordinates $(x_1 == x_2, y_1 == y_2)$.
- **Mitigation Strategy:**
  1. Implemented historical coordinate tracking: every entity tracks `prev_x` and `prev_y`.
  2. Two-phase collision check: entities collide if they occupy the same tile OR if they swapped tiles between consecutive frames (`player.x == ghost.prev_x and player.prev_x == ghost.x`).
  3. Fixed-timestep physics accumulator (60 updates per second) prevents large $\Delta t$ jumps.

### R-03: Entity Jitter & Spawn Point Oscillation
- **Risk:** When Pac-Man hit a wall or a dead ghost returned to its home corner, sub-tile interpolation caused visual back-and-forth jitter.
- **Root Causes:** State machine returning early without updating `prev_x, prev_y` or clearing `move_timer`, leaving `render_x` to swing across progress fractions.
- **Mitigation Strategy:**
  1. Added coordinate and timer locking: whenever an entity comes to a complete halt, `prev_x, prev_y` are locked to `x, y` and `move_timer` is reset to 0.0.
  2. Added a 5-second respawn timer for dead ghosts, ensuring clear visual stability before entering active chase mode.

### R-04: Corrupted Configuration and Highscore Storage (Subject Section 5.3 & 5.5)
- **Risk:** Evaluator injects negative lives, negative score values, empty level lists, or malformed highscore JSON files during defense.
- **Root Causes:** Implicit trust in user-supplied configuration data.
- **Mitigation Strategy:**
  1. Strip comments (`#` and `//`) prior to JSON deserialization.
  2. Implement strict bounds clamping in `core/config.py`: `lives >= 1` (default 3), `level_max_time > 0` (default 90.0), non-negative scores, dimensions $\ge 5$, and a fallback level list of at least 10 levels.
  3. Highscore sanitizer filters non-dict objects, strips non-alphanumeric characters, enforces a 10-character limit, clamps scores to $\ge 0$, and catches `KeyError` gracefully.

### R-05: External Maze Generator Dependency
- **Risk:** The assigned external `A-Maze-ing` package failing to install, throwing exceptions, or producing non-standard output.
- **Mitigation Strategy:**
  1. GoF Adapter Pattern (`MazeAdapter` in `core/maze_loader.py`) wraps the external package call.
  2. Internal sanity verification ensures corridors are traversable, corners are cleared for Super Pacgums, and the center is allocated for Pac-Man.
  3. Clear logging and clean error messages if the generator fails.

### R-06: Strict 42 Coding Standards & Type Safety
- **Risk:** Linters catching lines $>79$ characters or reviewers finding forbidden `# type: ignore` workarounds.
- **Mitigation Strategy:**
  1. Strict zero `# type: ignore` policy across the entire repository.
  2. Automated pre-commit checks enforcing `flake8 --max-line-length=79` and `mypy --disallow-untyped-defs`.
  3. Full PEP 257 docstring coverage for all classes and functions.

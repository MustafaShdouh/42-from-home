# Team Organization and Work Division

*Activity: Pac-Man (42 School Curriculum)*  
*Authors: mel-shdo (Mustafa), adnasser (Adel)*

---

## 1. Team Structure & Division of Labor

The project was executed by a two-student team under a strict 50/50 division contract, separating the software architecture into decoupled modules: Backend Core Engine and Frontend Presentation.

### Roles & Responsibilities

```
+-------------------------------------------------------------------------+
|                              mel-shdo (Mustafa)                         |
|                          Backend & Core Engine Lead                     |
+-------------------------------------------------------------------------+
| • Core physics engine, fixed-timestep accumulator, and collision grid   |
| • Authentic Ghost AI targeting strategies (Blinky, Pinky, Inky, Clyde)  |
| • Scatter/Chase wave scheduling & Cruise Elroy dynamic speed scaling    |
| • GoF State Pattern (`core/states/`) & Observer EventBus architecture    |
| • External Maze Generator Adapter (`core/maze_loader.py`)               |
| • Fault-tolerant config loader, bounds clamping & highscore resilience  |
| • Makefile automation, flake8/mypy CI enforcement, and packaging        |
+-------------------------------------------------------------------------+
                                    |
                    API Contract & Interface Boundary
                                    |
+-------------------------------------------------------------------------+
|                              adnasser (Adel)                            |
|                          Frontend & UI/UX Lead                          |
+-------------------------------------------------------------------------+
| • Pygame / MLX-compliant graphics rendering pipeline                    |
| • Sprite animations (mouth chomp, ghost eye direction, frightened flash)|
| • Real-time HUD overlay (Score, Lives, Current Level, Countdown Timer)  |
| • Interactive Menu navigation (Main Menu, Pause, Highscores, Game Over) |
| • User input event mapping (Arrow keys, WASD, Cheat keys)              |
| • Sound effects synthesis and background audio event triggers           |
+-------------------------------------------------------------------------+
```

---

## 2. API Contract & Architectural Boundary

To enable concurrent development without merge conflicts or mutual blocking, a strict interface contract was established on Day 1:

1. **Unidirectional Dependency:** The `ui/` package imports and queries public properties of `core.game_state.GameState`. The `core/` package **never** imports anything from `ui/`.
2. **State Pattern Transparency:** UI screens query `game_state.state` (which returns `"MENU"`, `"PLAYING"`, `"PAUSED"`, `"GAME_OVER"`, `"VICTORY"`) without needing to know the underlying state class implementation.
3. **Command Delegation:** User actions from `ui/input_handler.py` delegate cleanly to high-level methods on `GameState`:
   - `set_player_direction(direction)`
   - `start_game()`
   - `pause()` / `resume()`
   - `toggle_cheat(cheat_name)`
   - `submit_highscore(name)`
4. **Rendering Interpolation:** The physics engine computes `render_x` and `render_y` at sub-tile precision for both Pac-Man and ghosts, allowing the UI to render smooth animations at any display refresh rate without desynchronizing the backend grid.

---

## 3. Communication & Code Review Protocols

- **Daily Syncs:** Brief 15-minute syncs at the start of each working day to review progress against the Gantt chart and identify blockers.
- **Git Feature Branching:**
  - `main`: Production-ready, fully passing `make lint-strict` and zero-crash test suites.
  - `feature/core-*`: Mustafa's backend branches for physics, AI, and persistence.
  - `feature/ui-*`: Adel's frontend branches for renderer, menus, and input handling.
- **Peer Code Review:** No pull request was merged into `main` without cross-review by both partners. Code was reviewed against:
  - 42 Coding Standards (flake8 $\le 79$ characters).
  - Static typing (mypy zero warnings, zero `# type: ignore`).
  - Graceful exception handling (zero tracebacks on malformed inputs).

---

## 4. Conflict Resolution & Blocking Points Summary

| Issue / Conflict | Root Cause | Resolution & Architectural Decision |
|---|---|---|
| **Collision Phasing** | Fast entities crossing paths between frames. | Resolved collaboratively: Mustafa implemented historical `prev_x`/`prev_y` check, while Adel adjusted sprite render origins. |
| **Menu Keybind Clashes** | Cheat keys conflicting with standard game input. | Established keybind hierarchy: in typing screens (highscore entry), character inputs take precedence over cheats. |
| **Dot Eating Ahead Artifact** | Rendering interpolation progress vs. tile occupancy. | Investigated authentic arcade ROM logic: aligned dot consumption with tile center crossing ($t \ge 0.5$). |
| **External Maze Interface** | Bitmask format incompatible with tile grid. | Mustafa created `MazeAdapter` to translate external 2D bitmasks into standard corridor matrices without touching third-party code. |

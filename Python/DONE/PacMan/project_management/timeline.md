# Project Timeline and Progress Tracking

*Activity: Pac-Man (42 School Curriculum)*  
*Authors: mel-shdo (Mustafa), adnasser (Adel)*

---

## 1. Project Overview & Methodology

The Pac-Man project was organized using an Agile development framework adapted to the two-person engineering team structure. The development cycle spanned 4 weeks, structured into 5 iterative sprints with distinct deliverables, rigorous continuous integration, and milestone reviews.

---

## 2. Planned Sprints & Gantt Schedule

```
Sprint 1: Architecture & Interface Contracts  [Day 1  - Day 5 ] |==================|
Sprint 2: Core Physics Engine & Maze Adapter   [Day 6  - Day 12]       |======================|
Sprint 3: Authentic Ghost AI & State Machine  [Day 13 - Day 18]             |====================|
Sprint 4: UI Rendering, HUD & Audio Engine    [Day 17 - Day 23]                |=====================|
Sprint 5: QA Testing, Hardening & Packaging   [Day 24 - Day 28]                      |================|
```

### Detailed Sprint Breakdown

| Sprint | Timeline | Primary Objectives | Deliverables |
|---|---|---|---|
| **Sprint 1** | Days 1–5 | • Define architectural boundary (`core/` vs `ui/`)<br>• Formalize API contract between team members<br>• Configure flake8, mypy, and Makefile automation | Interface specification, project skeleton, Makefile |
| **Sprint 2** | Days 6–12 | • External `A-Maze-ing` package integration (`MazeAdapter`)<br>• Fixed-timestep physics accumulator<br>• Collision detection grid and coordinate interpolation | `core/maze_loader.py`, `core/player.py`, unit test suite |
| **Sprint 3** | Days 13–18 | • Ghost AI strategies (Blinky, Pinky, Inky, Clyde)<br>• Scatter/Chase 7-phase wave scheduler<br>• Cruise Elroy speed boost mechanics<br>• State pattern (`Menu`, `Playing`, `Paused`, `GameOver`, `Victory`) | `core/ai/`, `core/states/`, `core/ghost.py` |
| **Sprint 4** | Days 17–23 | • Pygame / MLX surface rendering pipeline<br>• HUD overlay (Score, Lives, Level, Timer)<br>• Menu screens, Highscore input, and Audio triggers | `ui/renderer.py`, `ui/menu.py`, `ui/audio.py` |
| **Sprint 5** | Days 24–28 | • Fault-tolerant config and highscore hardening<br>• Subagent QA and peer review simulation<br>• Standalone executable packaging (`make package`) | `dist/pac-man`, documentation, complete deliverables |

---

## 3. Actual Progress Tracking vs. Planned Schedule

| Phase / Feature | Planned Completion | Actual Completion | Variance | Notes & Adjustments |
|---|---|---|---|---|
| **Repository Setup & Makefile** | Day 2 | Day 2 | On Schedule | Strict flags configured early (`--disallow-untyped-defs`). |
| **Maze Generator Adapter** | Day 8 | Day 7 | +1 Day Early | Bitmask conversion completed ahead of time. |
| **Player Collision & Grid Movement** | Day 11 | Day 12 | -1 Day Delay | Additional time required to eliminate corner jitter. |
| **Ghost AI Algorithms** | Day 16 | Day 15 | +1 Day Early | Disassembly formulas ported cleanly into Strategy pattern. |
| **Scatter/Chase Wave Scheduler** | Day 18 | Day 18 | On Schedule | Implemented authentic 7-phase wave schedule. |
| **Cruise Elroy Mechanics** | Day 19 | Day 19 | On Schedule | Added proportional threshold scaling for variable maze sizes. |
| **UI Menus & Highscores Input** | Day 22 | Day 23 | -1 Day Delay | Text input handling required regex character filtering. |
| **Ghost Spawn Lock & Stabilization** | Day 25 | Day 25 | On Schedule | Eliminated spawn jitter and added 5-second dead timer. |
| **Config & Highscore Robustness** | Day 26 | Day 26 | On Schedule | Clamped numerical bounds and sanitized corrupted JSON entries. |
| **Standalone Packaging** | Day 28 | Day 27 | +1 Day Early | PyInstaller build script tested on Windows and Linux. |

---

## 4. Kanban Progress Snapshot

### Completed (Done)
- [x] External maze generator adapter (`MazeAdapter`) with `PERFECT=False`
- [x] Fixed-timestep accumulator (60 FPS decouple)
- [x] Ghost Strategy pattern (Blinky, Pinky, Inky, Clyde)
- [x] 7-phase Scatter/Chase wave cycles
- [x] Blinky Cruise Elroy speed scaling
- [x] Ghost eaten return-to-base and 5-second spawn timer
- [x] GoF State Pattern (`MenuState`, `PlayingState`, `PausedState`, `GameOverState`, `VictoryState`)
- [x] Observer EventBus decoupling (`SUPER_PACGUM_EATEN`, `GHOST_EATEN`, `LIFE_LOST`)
- [x] Fault-tolerant `config.json` parsing with `#` comment support and bounds clamping
- [x] Crash-proof persistent highscores (top 10, sanitization, regex name filtering)
- [x] 5 Peer review cheat toggles (Invincibility, Level Skip, Freeze Ghosts, Extra Lives, Speed Boost)
- [x] Automated Makefile (`install`, `run`, `debug`, `clean`, `lint`, `lint-strict`, `package`)
- [x] 100% adherence to strict 42 rules (<=79 chars, zero `# type: ignore`, zero crashes)

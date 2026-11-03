# Acceptance Test Plan and Verification Record

*Activity: Pac-Man (42 School Curriculum)*  
*Authors: mel-shdo (Mustafa), adnasser (Adel)*

## Scope and evidence

This record follows `pacman.pdf` version 1.5. The backend review on
2026-10-28 deliberately excluded reading or editing `ui/`. Temporary
`unittest` programs were run outside the repository, as suggested by
subject section 3.3. They are not part of the submission.

The backend regression suite passed 21 tests, including parameterized
configuration cases, 15 maze size/seed combinations and 48 frightened
movement cases. The assigned wheel was imported directly for these checks;
its source was not modified.

Syntax, function annotations, docstrings, obvious unused imports and the
79-character line limit were checked across all 19 backend/entry-point
Python files. These preliminary checks do not replace flake8 or mypy.
Neither checker nor GNU Make is installed in the review environment, and
installing the checkers failed because PyPI could not be resolved.

## Requirement verification matrix

| Subject | Requirement | Current evidence | Status |
|---|---|---|---|
| 3.1 | flake8 and mypy | Backend preliminary checks completed; actual checkers unavailable | Pending |
| 3.2 | Required lint commands | `make lint` includes `flake8 .` and all required mypy options; optional `lint-strict` exists | Implemented; execution pending |
| 5.1 | Exactly one JSON argument | Missing, extra and non-JSON arguments return 1 before importing UI | Backend pass |
| 5.2-5.3 | Comments, defaults and warnings | Comment lines, unknown keys, malformed JSON, bad encodings, non-object roots and missing keys checked | Backend pass |
| 5.3 | Invalid values | Booleans rejected as numbers; finite positive times, bounded dimensions, positive first seed and valid level labels checked | Backend pass |
| 5.4 | Assigned maze package | Bundled wheel used as-is with `perfect=False`; exceptions, missing package and malformed output use fallback | Backend pass |
| 5.5 | Persistent top ten | Save/reload, descending order, valid integer scores and filtered ten-character names checked | Backend pass |
| 5.5 | File errors | Invalid paths, missing/corrupt files, bad encoding and failed atomic replacement checked; old file preserved and temp file removed | Backend pass |
| 6.1 | Fixed first seed, random later | Repeated level 1 matches; adapter receives seed 0 for later levels | Backend pass |
| 6.1 | Reachability and corners | All corridors reachable; four power pellets and four corner ghosts in 15 size/seed cases | Backend pass |
| 6.1-6.2 | Middle start and respawn | Default spawn `(15, 15)`; nearest existing central corridor for other mazes; life-loss reset checked | Backend pass |
| 6.2 | Item consumption and collisions | Item consumed once; active ghost costs one life; edible ghost awards points; invincibility checked | Backend pass |
| 6.3 | Edible ghosts flee | Every legal neighbor considered, including reverse; selected move maximizes corridor distance from player | Backend pass |
| 6.3 | Ghost recovery | Ghost returns home, waits three seconds after arrival and revives; examples of five/ten seconds are not mandatory | Backend pass |
| 6.5 | Cheats | Invincibility, freeze, extra life, speed boost and level skip checked; new game clears toggles | Backend pass |
| 6.6 | Scoring | Dot +10, power pellet +50 and ghost +200 checked; saved valid large scores remain intact | Backend pass |
| 6.7 | Progression, lives, timeout and pause | Score/lives retained across ten levels; victory/game-over transitions, timeout life loss and paused timer checked | Backend pass |
| 4, 6.8 | UI, controls and MLX-equivalent functions | UI excluded from this review | Unverified |
| 7 | Reproducible packaging | Root `PacMan.spec` and Makefile packaging recipe added; includes data and external instructions/config copies | Build unverified |
| 7 | Private/unlisted platform build | No platform upload or downloaded-build test performed | Pending |

## Regressions addressed

- Lower-maze spawning replaced with nearest-center corridor selection.
- Random frightened branching replaced with distance-based fleeing.
- Missing configuration warnings added. Numeric booleans, infinite/NaN
  times, nonpositive seeds, blank paths, malformed level labels and extreme
  dimensions now fall back safely.
- All highscore path preparation is inside the error handler. Invalid-path
  errors are handled during directory creation, file writing and cleanup.
  Corrupted records are rejected, and valid large integer scores are not
  truncated to an arbitrary maximum.
- Ghost navigation caches now distinguish different maze objects.
- New games clear temporary freezes and cheat toggles. Respawning clears
  player consumption state and ghost recovery state.
- CLI errors are validated before graphical imports. Missing dependencies
  no longer produce a misleading successful headless launch.
- Required repository-wide lint flags and the optional strict target added.
- Installation selects the supplied wheel. Packaging uses a committed root
  recipe; cleanup preserves that recipe. README instructions updated.

## Remaining release checks

1. In an environment with dependencies and GNU Make, run `make install`,
   `make lint` and, optionally, `make lint-strict`. Fix any UI diagnostics
   with Adel; the backend-only review cannot certify repository-wide lint.
2. Check all UI flows and each graphical API against subject chapter 4.
3. Run `make package`, launch the resulting executable outside the source
   checkout, and verify controls, config edits, resources and persistence.
4. Upload a free private/unlisted build to the chosen gaming platform and
   verify a fresh download installs and launches with the included guide.

A missing configuration file is allowed to log an error and continue with
defaults under section 5.3. It is not required to exit with code 1.

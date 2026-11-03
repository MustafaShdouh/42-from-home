"""Central game state module for the core engine.

This module implements the Context of the State Pattern to manage the
overarching flow of the Pac-Man game without relying on complex conditional
statements.
"""

import os
import re
import json
import logging
import random
from typing import List, Dict, Any, Tuple

from core.player import Player
from core.ghost import Ghost
from core.maze_loader import MazeAdapter
from core.ai import (
    BlinkyChaseStrategy,
    PinkyChaseStrategy,
    InkyChaseStrategy,
    ClydeChaseStrategy,
)
from core.states import (
    GameStateInterface,
    MenuState,
    PlayingState,
    PausedState,
    GameOverState,
    VictoryState,
)

logger = logging.getLogger(__name__)


class GameState:
    """The central context of the game engine.

    This class holds all the dynamic data for a running game of Pac-Man,
    including the maze layout, player, ghosts, and scoring. It delegates
    behavioral logic to its active state object.

    Attributes:
        config (Dict[str, Any]): The configuration dictionary loaded
            at startup.
        maze (List[List[int]]): A 2D grid representing the current
            level geometry.
        player (Player): The player entity instance.
        ghosts (List[Ghost]): A list containing the four ghost entities.
        score (int): The player's current score.
        level (int): The current level number (1-indexed).
        lives (int): The player's remaining lives.
        time_remaining (float): The number of seconds left to
            complete the level.
        highscores (List[Dict[str, Any]]): A list of recorded highscores.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the GameState with the loaded configuration.

        Args:
            config (Dict[str, Any]): The configuration dictionary containing
                default and user-defined game parameters.
        """
        self.config = config
        self._current_state_obj: GameStateInterface = MenuState()

        self.maze: List[List[int]] = []
        self.player: Player = Player(0, 0)
        self.ghosts: List[Ghost] = []

        self.score: int = 0
        self.level: int = 1
        self.lives: int = config.get("lives", 3)
        self.is_invincible: bool = False
        self.ghosts_frozen: bool = False
        self.time_remaining: float = config.get("level_max_time", 90.0)
        self.highscores: List[Dict[str, Any]] = []
        self._load_highscores()
        self.wave_index: int = 0
        self.wave_timer: float = 0.0
        self.wave_mode: str = "SCATTER"
        self.elroy_stage: int = 0
        self.total_dots: int = 0
        self.freeze_timer: float = 0.0
        self.siren_stage: int = 1
        self.player_start_x: int = 1
        self.player_start_y: int = 1

        # Initialize Observer Pattern components
        from core.event_bus import EventBus
        from core.score_manager import ScoreManager

        self.event_bus = EventBus()
        self.score_manager = ScoreManager(self, self.event_bus)

        # Hook the physics engine into the ghost state machines
        self.event_bus.subscribe(
            "SUPER_PACGUM_EATEN", self._on_super_pacgum_eaten
        )

        # Pre-load level 1 so Adel has a maze to draw on the Menu screen
        self._load_level(self.level, announce=False)
        self._update_siren_stage()

    def get_frightened_duration(self) -> float:
        """Return level-scaled frightened duration in seconds.

        Decoupled from harsh arcade 0s/1s cliffs to maintain fair, engaging
        gameplay across all levels.

        Returns:
            float: Duration in seconds for frightened mode.
        """
        return max(4.0, 6.5 - (self.level - 1) * 0.25)

    def _on_super_pacgum_eaten(self, data: Any = None) -> None:
        """Trigger frightened mode on all active ghosts as an event callback.

        Args:
            data (Any, optional): Event payload (unused). Defaults to None.
        """
        duration = self.get_frightened_duration()
        for ghost in self.ghosts:
            ghost.set_frightened(duration=duration)

    @property
    def state(self) -> str:
        """Get the string representation of the current state.

        This property ensures backwards compatibility with the UI rendering
        logic, which expects a string rather than a state object.

        Returns:
            str: The string identifier of the current active state.
        """
        return self._current_state_obj.get_state_name()

    def change_state(self, new_state: GameStateInterface) -> None:
        """Change the active state pattern object.

        Args:
            new_state (GameStateInterface): The new state object to
                transition to.
        """
        self._current_state_obj = new_state
        state_name = new_state.get_state_name()
        logger.info("State changed to: %s", state_name)
        self.event_bus.publish("STATE_CHANGED", {"new_state": state_name})

    def _load_level(
        self, level_num: int, announce: bool = True
    ) -> None:
        """Load a specific level using the MazeAdapter.

        Per the 42 subject rules, level 1 uses a fixed positive seed,
        while all subsequent levels use a random seed (0).

        Args:
            level_num (int): The level number to load and generate.
        """
        if announce:
            logger.info("Loading level %d", level_num)

        seed = self.config.get("seed", 42) if level_num == 1 else 0

        width = self.config.get("width", 15)
        height = self.config.get("height", 15)

        enable_42 = self.config.get("enable_42", True)
        adapter = MazeAdapter(
            width=width, height=height, seed=seed, enable_42=enable_42
        )
        self.maze = adapter.generate_level()
        if not self.maze or not self.maze[0]:
            self.maze = adapter._generate_safe_fallback()

        # Use the closest existing corridor to the geometric center. Do not
        # carve through the assigned generator's walls (including its logo).
        h = len(self.maze)
        w = len(self.maze[0])
        target_x = w // 2
        target_y = h // 2

        best_pos = None
        best_score = float("inf")

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if self.maze[y][x] == 1:
                    continue
                dist = (x - target_x) ** 2 + (y - target_y) ** 2
                if dist < best_score:
                    best_score = dist
                    best_pos = (x, y)

        if best_pos is None:
            raise ValueError("Generated maze has no walkable spawn tile")
        spawn_x, spawn_y = best_pos
        self.player_start_x = spawn_x
        self.player_start_y = spawn_y
        self.player = Player(spawn_x, spawn_y)
        self.maze[spawn_y][spawn_x] = 0

        max_y = len(self.maze) - 2
        max_x = len(self.maze[0]) - 2
        self.ghosts = [
            Ghost(1, 1, "RED", BlinkyChaseStrategy()),
            Ghost(max_x, 1, "PINK", PinkyChaseStrategy()),
            Ghost(1, max_y, "CYAN", InkyChaseStrategy()),
            Ghost(max_x, max_y, "ORANGE", ClydeChaseStrategy()),
        ]

        if level_num == 1:
            base_ghost_speed = 6.0
        elif 2 <= level_num <= 4:
            base_ghost_speed = 6.8
        else:
            base_ghost_speed = 7.6

        for ghost in self.ghosts:
            ghost.base_speed = base_ghost_speed
            ghost.speed = base_ghost_speed

        self.wave_index = 0
        self.wave_timer = 0.0
        self.wave_mode = "SCATTER"
        self.elroy_stage = 0
        self._apply_pacgum_count(level_num)

    def _apply_pacgum_count(self, level_num: int) -> None:
        """Keep the configured number of regular dots in walkable cells.

        Power pellets (tile 3) are handled separately and preserved. The
        external maze generator and wall layout are not modified.
        """
        positions = [
            (x, y)
            for y, row in enumerate(self.maze)
            for x, tile in enumerate(row)
            if tile == 2
        ]
        requested = self.config.get("pacgum", 10)
        available = len(positions)
        if requested > available:
            logger.warning(
                "Config 'pacgum' (%d) exceeds available regular "
                "pacgum cells (%d) in level %d; using %d.",
                requested, available, level_num, available,
            )
        selected_count = min(requested, available)
        # Level 1 uses a stable distribution; later levels can vary.
        rng = random.Random(self.config.get("seed", 42)) if level_num == 1 \
            else random.Random()
        selected = set(rng.sample(positions, selected_count))
        for x, y in positions:
            if (x, y) not in selected:
                self.maze[y][x] = 0
        self.total_dots = sum(
            row.count(2) + row.count(3) for row in self.maze
        )

    # --- UI Contract Methods ---

    def set_player_direction(self, direction: str) -> None:
        """Set the queued direction for the player entity.

        Args:
            direction (str): The desired direction ('UP', 'DOWN', 'LEFT',
                'RIGHT').
        """
        if self.state == "PLAYING":
            self.player.queue_direction(direction)

    def start_game(self) -> None:
        """Transition the game state from a menu to active gameplay.

        Resets the score, level, and lives to their default values.
        """
        if self.state in ("MENU", "GAME_OVER", "VICTORY"):
            self.score = 0
            self.level = 1
            self.lives = self.config.get("lives", 3)
            self.is_invincible = False
            self.ghosts_frozen = False
            self.freeze_timer = 0.0
            self.config["multiplier_enabled"] = False
            self._load_level(self.level)
            self.time_remaining = self.config.get("level_max_time", 90.0)
            self.event_bus.publish("GAME_STARTED")
            self.change_state(PlayingState())

    def pause(self) -> None:
        """Pause the active gameplay."""
        if self.state == "PLAYING":
            self.change_state(PausedState())

    def resume(self) -> None:
        """Resume the gameplay from a paused state."""
        if self.state == "PAUSED":
            self.change_state(PlayingState())

    def toggle_cheat(self, cheat: str) -> None:
        """Toggle a specific cheat mode for peer review purposes.

        Args:
            cheat (str): The string identifier of the cheat to activate.
        """
        if cheat == "skip_level":
            self._win_level()
        elif cheat == "invincibility":
            self.is_invincible = not self.is_invincible
            logger.info("Cheat: Invincibility is now %s", self.is_invincible)
        elif cheat == "freeze_ghosts":
            self.ghosts_frozen = not self.ghosts_frozen
            logger.info("Cheat: Ghost Freeze is now %s", self.ghosts_frozen)
        elif cheat == "extra_life":
            self.lives += 1
            logger.info("Cheat: Extra Life! Lives now %d", self.lives)
        elif cheat == "speed_boost":
            if self.player.speed <= 8.0:
                self.player.speed = 14.0
            else:
                self.player.speed = 8.0
            logger.info("Cheat: Player speed is now %f", self.player.speed)
        elif cheat == "multiplier":
            current = self.config.get("multiplier_enabled", False)
            self.config["multiplier_enabled"] = not current
            logger.info("Cheat: Score multiplier is now %s", not current)

    def submit_highscore(self, name: str) -> None:
        """Submit a new highscore and return to the main menu.

        Args:
            name (str): The player's name, clamped to a maximum of 10
                characters.
        """
        # Enforce alphanumeric and spaces only per 42 rules
        clean_name = re.sub(
            r'[^a-zA-Z0-9 ]', '', str(name or '')
        ).strip()[:10]

        if not clean_name:
            clean_name = "ANONYMOUS"

        final_score = (
            self.score if type(self.score) is int and self.score >= 0 else 0
        )

        self.highscores.append({"name": clean_name, "score": final_score})

        # Sort by score descending and keep only the top 10
        self.highscores.sort(
            key=lambda x: int(x.get("score", 0)), reverse=True
        )
        self.highscores = self.highscores[:10]

        self._save_highscores()

        self.change_state(MenuState())

    # --- Internal Logic Methods ---

    def _win_level(self) -> None:
        """Handle the internal logic for successfully completing a level.

        Advances the level counter and transitions to the VictoryState if all
        levels are completed.
        """
        self.event_bus.publish(
            "LEVEL_COMPLETED",
            {"level": self.level, "next_level": self.level + 1}
        )
        self.level += 1
        levels = self.config.get("level", [1] * 10)
        max_levels = len(levels) if isinstance(levels, list) else 10

        if max_levels <= 0 or self.level > max_levels:
            self.event_bus.publish(
                "VICTORY", {"final_score": int(self.score)}
            )
            self.change_state(VictoryState())
        else:
            self._load_level(self.level)
            self._update_siren_stage()
            self.time_remaining = self.config.get("level_max_time", 90.0)

    def _lose_life(self) -> None:
        """Handle the internal logic for the player losing a life.

        Decrements the life counter and transitions to GameOverState if no
        lives remain. Otherwise, respawns the player.
        """
        self.lives -= 1
        self.time_remaining = self.config.get("level_max_time", 90.0)
        self.event_bus.publish(
            "PACMAN_DIED", {"lives_remaining": self.lives}
        )
        if self.lives <= 0:
            self.event_bus.publish(
                "GAME_OVER", {"final_score": int(self.score)}
            )
            self.change_state(GameOverState())
        else:
            if not self.maze or not self.maze[0]:
                return
            self.player.x = self.player_start_x
            self.player.y = self.player_start_y
            self.player.prev_x = self.player_start_x
            self.player.prev_y = self.player_start_y
            self.player.move_timer = 0.0
            self.player.dot_eaten_this_step = False
            self.player.direction = "LEFT"
            self.player.next_direction = "LEFT"
            self.wave_index = 0
            self.wave_timer = 0.0
            self.wave_mode = "SCATTER"
            self.elroy_stage = 0
            self._update_siren_stage()
            for ghost in self.ghosts:
                ghost.x = ghost.start_x
                ghost.y = ghost.start_y
                ghost.prev_x = ghost.start_x
                ghost.prev_y = ghost.start_y
                ghost.move_timer = 0.0
                ghost.direction = "LEFT"
                ghost.frightened_timer = 0.0
                ghost.dead_timer = 0.0
                ghost.home_arrived = False
                ghost.transit_timer = 0.0
                ghost.wave_mode = "SCATTER"
                ghost.mode = "SCATTER"
                ghost.speed = getattr(ghost, "base_speed", 6.0)
            logger.info("Lost a life! %d lives remaining.", self.lives)

    def _get_wave_schedule(self) -> List[Tuple[str, float]]:
        """Return the authentic 7-phase wave cycle for the current level.

        Returns:
            List[Tuple[str, float]]: Sequence of (mode, duration) intervals.
        """
        if self.level == 1:
            return [
                ("SCATTER", 7.0),
                ("CHASE", 20.0),
                ("SCATTER", 7.0),
                ("CHASE", 20.0),
                ("SCATTER", 5.0),
                ("CHASE", 20.0),
                ("SCATTER", 5.0),
                ("CHASE", float("inf")),
            ]
        elif 2 <= self.level <= 4:
            return [
                ("SCATTER", 7.0),
                ("CHASE", 20.0),
                ("SCATTER", 7.0),
                ("CHASE", 20.0),
                ("SCATTER", 5.0),
                ("CHASE", 1033.0),
                ("SCATTER", 1.0 / 60.0),
                ("CHASE", float("inf")),
            ]
        else:
            return [
                ("SCATTER", 5.0),
                ("CHASE", 20.0),
                ("SCATTER", 5.0),
                ("CHASE", 20.0),
                ("SCATTER", 5.0),
                ("CHASE", 1037.0),
                ("SCATTER", 1.0 / 60.0),
                ("CHASE", float("inf")),
            ]

    def _update_wave_cycles(self, dt: float) -> None:
        """Advance the 7-phase Scatter/Chase wave cycle timer.

        Args:
            dt (float): Delta time in seconds elapsed since last frame.
        """
        # Pause wave schedule progression during frightened mode
        if any(g.mode == "FRIGHTENED" for g in self.ghosts):
            return

        schedule = self._get_wave_schedule()
        if self.wave_index >= len(schedule):
            return

        _, duration = schedule[self.wave_index]
        self.wave_timer += dt
        if self.wave_timer >= duration:
            self.wave_timer -= duration
            self.wave_index += 1
            if self.wave_index < len(schedule):
                new_mode, _ = schedule[self.wave_index]
                self._switch_wave_mode(new_mode)

    def _switch_wave_mode(self, new_mode: str) -> None:
        """Transition all non-frightened/non-dead ghosts to the new mode.

        Args:
            new_mode (str): The new mode ('SCATTER' or 'CHASE').
        """
        self.wave_mode = new_mode
        for ghost in self.ghosts:
            if ghost.mode in ("SCATTER", "CHASE"):
                # Cruise Elroy Stage 2 override: Blinky ignores Scatter waves
                if (
                    ghost.color == "RED"
                    and self.elroy_stage == 2
                    and new_mode == "SCATTER"
                ):
                    continue
                ghost.mode = new_mode
                ghost._reverse_direction()
        logger.info(
            "Wave transition: %s (Phase %d)", new_mode, self.wave_index
        )

    def _update_cruise_elroy(self) -> None:
        """Update Cruise Elroy speed and behavior for Blinky."""
        dots_remaining = sum(
            row.count(2) + row.count(3) for row in self.maze
        )

        if self.level == 1:
            th1, th2 = 20, 10
        elif self.level == 2:
            th1, th2 = 30, 15
        elif self.level in (3, 4):
            th1, th2 = 40, 20
        else:
            th1, th2 = 50, 25

        # Scale down thresholds proportionally if total dots is small
        if 0 < self.total_dots < 100:
            th1 = max(4, self.total_dots // 5)
            th2 = max(2, self.total_dots // 10)

        if dots_remaining <= th2:
            new_stage = 2
        elif dots_remaining <= th1:
            new_stage = 1
        else:
            new_stage = 0

        blinky = next(
            (g for g in self.ghosts if getattr(g, "color", "") == "RED"),
            None,
        )
        if blinky is not None and blinky.mode not in ("DEAD", "FRIGHTENED"):
            target_speed = 6.0
            if new_stage == 2:
                target_speed = 8.2
                if blinky.mode == "SCATTER":
                    blinky.mode = "CHASE"
            elif new_stage == 1:
                target_speed = 7.0
            else:
                target_speed = getattr(blinky, "base_speed", 6.0)
            if hasattr(blinky, "_set_speed"):
                blinky._set_speed(target_speed)
            else:
                blinky.speed = target_speed

        if new_stage != self.elroy_stage:
            self.elroy_stage = new_stage
            speed_val = blinky.speed if blinky else 0.0
            logger.info(
                "Cruise Elroy stage %d active! Blinky speed: %.1f",
                new_stage, speed_val
            )

    def _update_siren_stage(self) -> None:
        """Evaluate remaining dots and publish SIREN_STAGE_CHANGED on shift.

        Authentic Namco arcade escalates across 5 background siren tiers as
        dots are eaten in the maze (pacman.c:4228-4325).
        """
        if not self.maze or not self.maze[0] or self.total_dots <= 0:
            return

        dots_remaining = sum(
            row.count(2) + row.count(3) for row in self.maze
        )

        # 5-tier escalation based on authentic remaining dot ratios
        if dots_remaining <= max(2, self.total_dots // 15):
            new_stage = 5
        elif dots_remaining <= max(4, self.total_dots // 8):
            new_stage = 4
        elif dots_remaining <= max(8, self.total_dots // 4):
            new_stage = 3
        elif dots_remaining <= max(16, self.total_dots // 2):
            new_stage = 2
        else:
            new_stage = 1

        if new_stage != getattr(self, "siren_stage", 1):
            self.siren_stage = new_stage
            self.event_bus.publish(
                "SIREN_STAGE_CHANGED",
                {
                    "stage": new_stage,
                    "dots_remaining": dots_remaining,
                    "total_dots": self.total_dots,
                },
            )

    def _load_highscores(self) -> None:
        """Load the highscores from the configured JSON file."""
        filename = self.config.get("highscore_filename", "highscores.json")
        sanitized: List[Dict[str, Any]] = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for entry in data:
                        if (
                            not isinstance(entry, dict)
                            or "score" not in entry
                        ):
                            continue
                        name_raw = str(entry.get("name", "ANONYMOUS"))
                        clean_name = re.sub(
                            r'[^a-zA-Z0-9 ]', '', name_raw
                        ).strip()[:10]
                        if not clean_name:
                            clean_name = "ANONYMOUS"
                        score_raw = entry.get("score")
                        if type(score_raw) is not int or score_raw < 0:
                            continue
                        sanitized.append(
                            {"name": clean_name, "score": score_raw}
                        )
                else:
                    logger.warning("Highscores must be a JSON array.")
            sanitized.sort(
                key=lambda x: int(x.get("score", 0)), reverse=True
            )
            self.highscores = sanitized[:10]
        except FileNotFoundError:
            self.highscores = []
        except (OSError, ValueError, TypeError) as err:
            logger.warning("Failed to load highscores: %s", err)
            self.highscores = []

    def _save_highscores(self) -> None:
        """Save the highscores atomically to the configured JSON file."""
        filename = self.config.get("highscore_filename", "highscores.json")
        temp_filename = None
        try:
            dir_name = os.path.dirname(filename)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            temp_filename = f"{filename}.tmp.{os.getpid()}"
            with open(temp_filename, "w", encoding="utf-8") as f:
                json.dump(self.highscores, f, indent=4)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_filename, filename)
        except (OSError, ValueError, TypeError) as e:
            logger.error("Failed to save highscores: %s", e)
        finally:
            if temp_filename is not None:
                try:
                    os.remove(temp_filename)
                except (OSError, ValueError):
                    pass

    def tick(self, dt: float) -> None:
        """Advance the game simulation by delegating to the current state.

        Args:
            dt (float): The delta time (in seconds) elapsed since the
                last frame.
        """
        self._current_state_obj.tick(self, dt)

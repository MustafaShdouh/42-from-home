"""Inky's authentic pincer targeting algorithm."""

from typing import Tuple, Optional, Any
from core.ai.base_strategy import BehaviorStrategy


class InkyChaseStrategy(BehaviorStrategy):
    """Inky (Cyan Ghost) Chase Strategy.

    Inky's nickname is 'Bashful'. His targeting logic is the most complex. He
    calculates a pivot point 2 tiles ahead of Pac-Man, and then draws a vector
    from Blinky to that pivot point, doubling the vector to find his target.
    This creates a deadly 'pincer' movement with Blinky.
    """

    def calculate_target(
        self, ghost: Any, game_state: Any
    ) -> Optional[Tuple[int, int]]:
        """Calculate Inky's target using Pac-Man and Blinky's coordinates.

        Args:
            ghost (Any): The ghost instance executing this strategy.
            game_state (Any): The central game context containing player
                and ghost data.

        Returns:
            Optional[Tuple[int, int]]: A tuple containing the (x, y) target
                coordinates.
        """
        pacman = game_state.player

        # When Inky is within close proximity, close the pincer and target
        # Pac-Man directly to prevent walking past or oscillating.
        dist_to_pac = abs(ghost.x - pacman.x) + abs(ghost.y - pacman.y)
        if dist_to_pac <= 4:
            return (pacman.x, pacman.y)

        # Check if Pac-Man is stationary (not actively moving)
        is_stationary = (
            pacman.x == pacman.prev_x
            and pacman.y == pacman.prev_y
            and pacman.move_timer == 0.0
        )

        inter_x = pacman.x
        inter_y = pacman.y

        # If Pac-Man is actively moving, project 2 tiles ahead including the
        # authentic UP overflow bug from the original ROM.
        if not is_stationary:
            if pacman.direction == "UP":
                inter_y -= 2
                inter_x -= 2
            elif pacman.direction == "DOWN":
                inter_y += 2
            elif pacman.direction == "LEFT":
                inter_x -= 2
            elif pacman.direction == "RIGHT":
                inter_x += 2

        # Find Blinky's current tile (fallback to pacman tile if no ghosts)
        blinky = next(
            (g for g in getattr(game_state, "ghosts", [])
             if getattr(g, "color", "") == "RED"),
            game_state.ghosts[0] if getattr(game_state, "ghosts", None)
            else None,
        )
        blinky_x = blinky.x if blinky else pacman.x
        blinky_y = blinky.y if blinky else pacman.y

        # Vector from Blinky to the pivot
        vec_x = inter_x - blinky_x
        vec_y = inter_y - blinky_y

        # Bound flank offset to a tactical ambush radius (3 tiles) to prevent
        # flinging Inky to the outer edge of the world when Blinky is far.
        clamp_x = max(-3, min(3, vec_x))
        clamp_y = max(-3, min(3, vec_y))

        target_x = inter_x + clamp_x
        target_y = inter_y + clamp_y

        # Ensure target coordinates stay within valid maze bounds
        w = len(game_state.maze[0])
        h = len(game_state.maze)
        target_x = max(1, min(w - 2, target_x))
        target_y = max(1, min(h - 2, target_y))

        return (target_x, target_y)

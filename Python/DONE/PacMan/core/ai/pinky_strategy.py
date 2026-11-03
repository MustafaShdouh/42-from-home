"""Pinky's authentic ambush targeting algorithm."""

from typing import Tuple, Optional, Any
from core.ai.base_strategy import BehaviorStrategy


class PinkyChaseStrategy(BehaviorStrategy):
    """Pinky (Pink Ghost) Chase Strategy.

    Pinky's nickname is 'Speedy'. She attempts to ambush the player by
    targeting a coordinate exactly 4 tiles ahead of Pac-Man's current
    direction.
    """

    def calculate_target(
        self, ghost: Any, game_state: Any
    ) -> Optional[Tuple[int, int]]:
        """Calculate a target 4 tiles ahead of the player's current direction.

        Preserves the authentic Z80 16-bit math overflow bug where facing UP
        causes the target to shift 4 tiles UP and 4 tiles LEFT.

        Args:
            ghost (Any): The ghost instance executing this strategy.
            game_state (Any): The central game context containing player data.

        Returns:
            Optional[Tuple[int, int]]: A tuple containing the (x, y) target
                coordinates.
        """
        pacman = game_state.player
        target_x = pacman.x
        target_y = pacman.y

        if pacman.direction == "UP":
            target_y -= 4
            target_x -= 4  # The overflow bug
        elif pacman.direction == "DOWN":
            target_y += 4
        elif pacman.direction == "LEFT":
            target_x -= 4
        elif pacman.direction == "RIGHT":
            target_x += 4

        return (target_x, target_y)

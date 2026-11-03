"""Blinky's authentic direct pursuit targeting algorithm."""

from typing import Tuple, Optional, Any
from core.ai.base_strategy import BehaviorStrategy


class BlinkyChaseStrategy(BehaviorStrategy):
    """Blinky (Red Ghost) Chase Strategy.

    Blinky's nickname is 'Shadow'. His target tile in chase mode is exactly
    Pac-Man's current tile, making him the most aggressive direct pursuer.
    """

    def calculate_target(
        self, ghost: Any, game_state: Any
    ) -> Optional[Tuple[int, int]]:
        """Target the player's exact current grid coordinates.

        Args:
            ghost (Any): The ghost instance executing this strategy.
            game_state (Any): The central game context containing player data.

        Returns:
            Optional[Tuple[int, int]]: A tuple containing the (x, y) target
                coordinates.
        """
        pacman = game_state.player
        return (pacman.x, pacman.y)

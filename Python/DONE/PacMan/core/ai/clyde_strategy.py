"""Clyde's authentic proximity-based targeting algorithm."""

from typing import Tuple, Optional, Any
from core.ai.base_strategy import BehaviorStrategy


class ClydeChaseStrategy(BehaviorStrategy):
    """Clyde (Orange Ghost) Chase Strategy.

    Clyde's nickname is 'Pokey'. He pretends not to care. If he is far from
    Pac-Man (>= 8 tiles Euclidean distance), he targets Pac-Man directly just
    like Blinky. However, if he gets within 8 tiles, he loses his nerve and
    targets his home scatter corner (bottom-left) to flee.
    """

    def calculate_target(
        self, ghost: Any, game_state: Any
    ) -> Optional[Tuple[int, int]]:
        """Calculate Clyde's target based on radial proximity to the player.

        Args:
            ghost (Any): The ghost instance executing this strategy.
            game_state (Any): The central game context containing player data.

        Returns:
            Optional[Tuple[int, int]]: A tuple containing the (x, y) target
                coordinates.
        """
        pacman = game_state.player
        if ghost is None:
            return (pacman.x, pacman.y)

        # Calculate Euclidean distance squared
        squared_dist = (pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2

        if squared_dist < 64:
            maze_height = len(game_state.maze) if game_state.maze else 0
            return (1, max(1, maze_height - 2))
        else:
            return (pacman.x, pacman.y)

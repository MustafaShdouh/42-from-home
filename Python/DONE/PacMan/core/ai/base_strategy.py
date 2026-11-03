"""Base interface for Ghost AI strategies.

This module defines the BehaviorStrategy interface which all concrete ghost
algorithms (e.g., Blinky, Pinky) must implement to calculate their target
tiles.
"""

from typing import Tuple, Optional, Any


class BehaviorStrategy:
    """Base interface for ghost targeting algorithms.

    Defines the contract for how a ghost calculates its target tile based on
    the current state of the game, the player, and other ghosts.
    """

    def calculate_target(
        self, ghost: Any, game_state: Any
    ) -> Optional[Tuple[int, int]]:
        """Calculate the target grid coordinate for the ghost.

        Args:
            ghost (Any): The ghost instance this strategy is attached to.
            game_state (Any): The central game context containing maze
                and player data.

        Returns:
            Optional[Tuple[int, int]]: The (x, y) grid coordinates to target,
                or None if no specific target is required.
        """
        return None

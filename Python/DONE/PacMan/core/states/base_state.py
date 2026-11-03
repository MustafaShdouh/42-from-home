"""Base state interface for the game state machine."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game_state import GameState


class GameStateInterface:
    """Base interface for all game states in the State Pattern.

    This interface defines the required methods that any concrete game state
    must implement to handle frame updates and provide state identification.
    """

    def tick(self, context: GameState, dt: float) -> None:
        """Handle per-frame logic specific to this game state.

        Args:
            context (GameState): The central game context holding all data.
            dt (float): The delta time (in seconds) elapsed since the
                last frame.
        """

    def get_state_name(self) -> str:
        """Retrieve the string identifier for this state.

        Returns:
            str: A string representing the state name (e.g., 'MENU').
        """
        return "UNKNOWN"

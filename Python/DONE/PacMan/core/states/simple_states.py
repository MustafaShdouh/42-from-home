"""Simple states module for inactive game phases (Menus, Pauses, etc.)."""

from core.states.base_state import GameStateInterface


class MenuState(GameStateInterface):
    """Represents the main menu state of the game."""

    def get_state_name(self) -> str:
        """Retrieve the string identifier for the menu state.

        Returns:
            str: The string 'MENU'.
        """
        return "MENU"


class PausedState(GameStateInterface):
    """Represents the paused state of the game."""

    def get_state_name(self) -> str:
        """Retrieve the string identifier for the paused state.

        Returns:
            str: The string 'PAUSED'.
        """
        return "PAUSED"


class GameOverState(GameStateInterface):
    """Represents the game over state after all lives are lost."""

    def get_state_name(self) -> str:
        """Retrieve the string identifier for the game over state.

        Returns:
            str: The string 'GAME_OVER'.
        """
        return "GAME_OVER"


class VictoryState(GameStateInterface):
    """Represents the victory state after all levels are completed."""

    def get_state_name(self) -> str:
        """Retrieve the string identifier for the victory state.

        Returns:
            str: The string 'VICTORY'.
        """
        return "VICTORY"

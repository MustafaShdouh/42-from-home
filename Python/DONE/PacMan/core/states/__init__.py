"""States package initialization."""

from core.states.base_state import GameStateInterface
from core.states.playing_state import PlayingState
from core.states.simple_states import (
    MenuState,
    PausedState,
    GameOverState,
    VictoryState,
)

__all__ = [
    "GameStateInterface",
    "PlayingState",
    "MenuState",
    "PausedState",
    "GameOverState",
    "VictoryState",
]

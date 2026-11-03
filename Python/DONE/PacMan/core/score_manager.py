"""Score management system hooked into the Event Bus."""

import logging
from typing import Any
from core.event_bus import EventBus
from core.game_state import GameState

logger = logging.getLogger(__name__)


class ScoreManager:
    """Manages scoring logic using the Observer Pattern.

    Subscribes to game events via the EventBus and updates the central
    GameState score safely. It handles complex isolated scoring logic.

    Attributes:
        game_state (GameState): The central game context holding the score.
        event_bus (EventBus): The message bus to listen to for scoring events.
    """

    def __init__(self, game_state: GameState, event_bus: EventBus) -> None:
        """Initialize the ScoreManager and subscribe to events.

        Args:
            game_state (GameState): The game context to mutate.
            event_bus (EventBus): The event bus to subscribe to.
        """
        self.game_state = game_state
        self.event_bus = event_bus
        self.ghosts_eaten_in_wave: int = 0
        # Subscribe to relevant events broadcasted by the physics engine
        self.event_bus.subscribe("DOT_EATEN", self._on_dot_eaten)
        self.event_bus.subscribe(
            "SUPER_PACGUM_EATEN", self._on_super_pacgum_eaten
        )
        self.event_bus.subscribe("GHOST_EATEN", self._on_ghost_eaten)
        self.event_bus.subscribe(
            "FRIGHTENED_MODE_ENDED", self._on_frightened_ended
        )

    def _add_score(self, points: int) -> None:
        """Add points to the total score and log the update.

        Args:
            points (int): The number of points to add.
        """
        self.game_state.score += points
        logger.debug(
            "Score updated: +%d (Total: %d)", points, self.game_state.score
        )

    def _on_dot_eaten(self, data: Any = None) -> None:
        """Handle normal dot consumption (10 points).

        Args:
            data (Any, optional): Event payload (unused). Defaults to None.
        """
        pts = self.game_state.config.get("points_per_pacgum", 10)
        self._add_score(pts)

    def _on_super_pacgum_eaten(self, data: Any = None) -> None:
        """Handle super pacgum consumption and reset wave eaten counter.

        Args:
            data (Any, optional): Event payload (unused). Defaults to None.
        """
        self.ghosts_eaten_in_wave = 0
        pts = self.game_state.config.get("points_per_super_pacgum", 50)
        self._add_score(pts)

    def _on_ghost_eaten(self, data: Any = None) -> None:
        """Handle ghost consumption with optional authentic doubling.

        Per Section 6.6 of the 42 subject, eating an edible ghost awards
        Z points by default without decreasing. If 'multiplier_enabled' is
        active, authentic arcade exponential doubling (200, 400, 800, 1600)
        is applied.

        Args:
            data (Any, optional): Event payload (unused). Defaults to None.
        """
        base_points = self.game_state.config.get("points_per_ghost", 200)
        use_multiplier = self.game_state.config.get(
            "multiplier_enabled", False
        )

        if use_multiplier:
            self.ghosts_eaten_in_wave = min(4, self.ghosts_eaten_in_wave + 1)
            multiplier = 2 ** (self.ghosts_eaten_in_wave - 1)
            points = base_points * multiplier
        else:
            points = base_points

        self._add_score(points)

    def _on_frightened_ended(self, data: Any = None) -> None:
        """Handle the end of frightened mode and reset eaten counter.

        Args:
            data (Any, optional): Event payload (unused). Defaults to None.
        """
        self.ghosts_eaten_in_wave = 0

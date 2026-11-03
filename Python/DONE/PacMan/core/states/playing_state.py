"""Playing state module for active gameplay logic."""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any
from core.states.base_state import GameStateInterface

if TYPE_CHECKING:
    from core.game_state import GameState

logger = logging.getLogger(__name__)


class PlayingState(GameStateInterface):
    """Represents the active gameplay state."""

    def _handle_collision(
        self, context: GameState, ghost: Any
    ) -> bool:
        """Handle collision between player and a ghost.

        Args:
            context (GameState): The central game context.
            ghost (Any): The ghost entity involved in collision.

        Returns:
            bool: True if simulation tick should terminate immediately
                (e.g., player lost a life or eat-pause freeze triggered).
        """
        if ghost.mode == "FRIGHTENED":
            was_any_dead = any(g.mode == "DEAD" for g in context.ghosts)
            if hasattr(ghost, "set_dead"):
                ghost.set_dead()
            else:
                ghost.mode = "DEAD"
            context.event_bus.publish(
                "GHOST_EATEN", {"ghost": ghost.color}
            )
            if not was_any_dead:
                context.event_bus.publish(
                    "GHOST_EYES_ACTIVE", {"ghost": ghost.color}
                )
            context.freeze_timer = 0.5
            return True
        elif ghost.mode in ("CHASE", "SCATTER"):
            if not context.is_invincible:
                logger.info(
                    "Player caught by %s ghost!", ghost.color
                )
                context._lose_life()
                return True
        return False

    def _is_colliding(self, player: Any, ghost: Any) -> bool:
        """Determine if the player and a ghost are in physical contact.

        Uses continuous interpolated sub-tile coordinates (render_x, render_y)
        to ensure collisions trigger when sprites visually touch, preventing
        phantom hits from a full tile away.

        Args:
            player (Any): The player entity.
            ghost (Any): The ghost entity.

        Returns:
            bool: True if entities visually overlap (within 0.55 tiles).
        """
        dx = abs(player.render_x - ghost.render_x)
        dy = abs(player.render_y - ghost.render_y)
        if dx < 0.45 and dy < 0.45:
            return True

        # Head-on corridor swap: verify sub-tile coordinates actually crossed
        swapped = (
            ghost.x == player.prev_x
            and ghost.y == player.prev_y
            and ghost.prev_x == player.x
            and ghost.prev_y == player.y
        )
        if swapped:
            if player.prev_x != player.x:
                rel_old = player.prev_x - ghost.prev_x
                rel_cur = player.render_x - ghost.render_x
                if rel_old * rel_cur <= 0:
                    return True
            elif player.prev_y != player.y:
                rel_old = player.prev_y - ghost.prev_y
                rel_cur = player.render_y - ghost.render_y
                if rel_old * rel_cur <= 0:
                    return True

        return False

    def tick(self, context: GameState, dt: float) -> None:
        """Advance the active gameplay simulation by the given time delta.

        Decrements the level timer and handles life loss if the time runs out.
        Updates player and ghost movement and detects collisions.

        Args:
            context (GameState): The central game context holding all data.
            dt (float): The delta time (in seconds) elapsed since the
                last frame.
        """
        if not context.maze or not context.maze[0]:
            return

        if getattr(context, "freeze_timer", 0.0) > 0.0:
            context.freeze_timer -= dt
            return

        context.time_remaining -= dt
        if context.time_remaining <= 0:
            logger.info("Time ran out!")
            context._lose_life()
            return

        # Update player physics and collisions (eating dots)
        context.player.update(context.maze, context.event_bus, dt)
        context._update_siren_stage()

        # Check collision immediately after player moves (prevents phasing)
        for ghost in context.ghosts:
            if self._is_colliding(context.player, ghost):
                if self._handle_collision(context, ghost):
                    return

        # Check win condition: Are all pacgums eaten?
        dots_remaining = any(2 in row or 3 in row for row in context.maze)
        if not dots_remaining:
            logger.info("All dots eaten! Level complete.")
            context._win_level()
            return

        # Update ghost AI logic
        if not context.ghosts_frozen:
            context._update_wave_cycles(dt)
            context._update_cruise_elroy()
            had_dead = any(g.mode == "DEAD" for g in context.ghosts)

            for ghost in context.ghosts:
                ghost.tick(dt, context.event_bus, context.wave_mode)

                # 1. Ask the injected strategy for the target tile
                target_x, target_y = ghost.calculate_target(context)

                # 2. Actually move the ghost using greedy pathfinding
                ghost.move_towards(
                    target_x, target_y, context.maze, dt, context.ghosts
                )

                # 3. Check collision with Player after ghost moves
                if self._is_colliding(context.player, ghost):
                    if self._handle_collision(context, ghost):
                        return

            if had_dead and not any(g.mode == "DEAD" for g in context.ghosts):
                context.event_bus.publish("GHOST_EYES_ENDED")

    def get_state_name(self) -> str:
        """Retrieve the string identifier for the playing state.

        Returns:
            str: The string 'PLAYING'.
        """
        return "PLAYING"

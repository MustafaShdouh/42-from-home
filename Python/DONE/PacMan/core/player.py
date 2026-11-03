"""Player entity module for Pac-Man."""

import logging
from typing import List, Tuple, Any

logger = logging.getLogger(__name__)


class Player:
    """Represents the Pac-Man player entity.

    Handles movement, input queuing (for smooth cornering), and interacting
    with the maze (eating dots).

    Attributes:
        x (int): Current X grid coordinate.
        y (int): Current Y grid coordinate.
        direction (str): The current movement direction.
        next_direction (str): The queued direction the user wants to turn.
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        """Initialize the Player entity.

        Args:
            start_x (int): Starting X grid coordinate.
            start_y (int): Starting Y grid coordinate.
        """
        self.x = start_x
        self.y = start_y
        self.prev_x = start_x
        self.prev_y = start_y
        self.direction = "LEFT"
        self.next_direction = "LEFT"
        self.speed = 8.0  # tiles per second
        self.move_timer = 0.0
        self.dot_eaten_this_step = False
        self.dots_eaten_count = 0

    @property
    def render_x(self) -> float:
        """Calculate sub-tile fractional X for smooth 60 FPS rendering.

        Returns:
            float: Interpolated X coordinate between prev_x and x.
        """
        if self.speed <= 0:
            return float(self.x)
        if abs(self.x - self.prev_x) > 1:
            return float(self.x)
        step_duration = 1.0 / self.speed
        progress = min(1.0, max(0.0, self.move_timer / step_duration))
        return self.prev_x + (self.x - self.prev_x) * progress

    @property
    def render_y(self) -> float:
        """Calculate sub-tile fractional Y for smooth 60 FPS rendering.

        Returns:
            float: Interpolated Y coordinate between prev_y and y.
        """
        if self.speed <= 0:
            return float(self.y)
        if abs(self.y - self.prev_y) > 1:
            return float(self.y)
        step_duration = 1.0 / self.speed
        progress = min(1.0, max(0.0, self.move_timer / step_duration))
        return self.prev_y + (self.y - self.prev_y) * progress

    def queue_direction(self, direction: str) -> None:
        """Queue a direction or execute an immediate 180-degree reversal.

        In authentic arcade Pac-Man, pressing the exact opposite of the current
        movement direction reverses immediately without waiting to reach the
        next tile center.

        Args:
            direction (str): The desired direction ('UP', 'DOWN', 'LEFT',
                'RIGHT').
        """
        if direction not in ("UP", "DOWN", "LEFT", "RIGHT"):
            return
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        if self.speed > 0 and opposites.get(direction) == self.direction:
            step_duration = 1.0 / self.speed
            if 0 < self.move_timer < step_duration:
                self.direction = direction
                self.next_direction = direction
                self.x, self.prev_x = self.prev_x, self.x
                self.y, self.prev_y = self.prev_y, self.y
                self.move_timer = max(0.0, step_duration - self.move_timer)
                self.dot_eaten_this_step = True
                return
            elif self.move_timer == 0.0:
                self.direction = direction
                self.next_direction = direction
                self.prev_x, self.prev_y = self.x, self.y
                return

        self.next_direction = direction

    def _get_next_coord(
        self, current_x: int, current_y: int, direction: str
    ) -> Tuple[int, int]:
        """Calculate the next coordinate based on a given direction.

        Args:
            current_x (int): The starting X coordinate.
            current_y (int): The starting Y coordinate.
            direction (str): The direction of movement.

        Returns:
            Tuple[int, int]: The resulting (x, y) coordinates.
        """
        if direction == "UP":
            return (current_x, current_y - 1)
        elif direction == "DOWN":
            return (current_x, current_y + 1)
        elif direction == "LEFT":
            return (current_x - 1, current_y)
        elif direction == "RIGHT":
            return (current_x + 1, current_y)
        return (current_x, current_y)

    def _can_move(
        self, x: int, y: int, direction: str, maze: List[List[int]]
    ) -> bool:
        """Check if movement into the adjacent tile is unblocked.

        Args:
            x (int): Starting X grid coordinate.
            y (int): Starting Y grid coordinate.
            direction (str): Direction of movement.
            maze (List[List[int]]): The 2D level grid.

        Returns:
            bool: True if destination coordinate is within bounds and not
                a wall.
        """
        nx, ny = self._get_next_coord(x, y, direction)
        return (
            0 <= ny < len(maze)
            and 0 <= nx < len(maze[0])
            and maze[ny][nx] != 1
        )

    def update(self, maze: List[List[int]], event_bus: Any, dt: float) -> None:
        """Update the player's position and interact with the maze.

        Handles smooth cornering by attempting to move in the `next_direction`
        first. If blocked by a wall, falls back to the current `direction`.
        If both are blocked, the player simply stops moving.

        Args:
            maze (List[List[int]]): The 2D grid representing the level
                geometry.
            event_bus (Any): The centralized event bus to publish
                consumption events.
            dt (float): The delta time in seconds elapsed since last frame.
        """
        if self.speed <= 0:
            return

        step_duration = 1.0 / self.speed

        # Unblock immediately from a stop if an open direction is requested
        if self.x == self.prev_x and self.y == self.prev_y:
            for d in (self.next_direction, self.direction):
                if self._can_move(self.x, self.y, d, maze):
                    self.direction = d
                    self.x, self.y = self._get_next_coord(self.x, self.y, d)
                    self.move_timer = 0.0
                    self.dot_eaten_this_step = False
                    break

        self.move_timer += dt
        progress = self.move_timer / step_duration

        # Mid-tile consumption: eat dot when mouth makes visual contact
        if progress >= 0.5 and not self.dot_eaten_this_step:
            self._check_collisions(maze, event_bus)
            self.dot_eaten_this_step = True

        if self.move_timer < step_duration:
            return

        self.move_timer -= step_duration

        # Safety: ensure collision was checked if dt was large
        if not self.dot_eaten_this_step:
            self._check_collisions(maze, event_bus)

        # Cornering Priority: Try to turn into the queued direction first
        moved = False
        if self._can_move(self.x, self.y, self.next_direction, maze):
            self.direction = self.next_direction
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = self._get_next_coord(
                self.x, self.y, self.next_direction
            )
            moved = True
        elif self._can_move(self.x, self.y, self.direction, maze):
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = self._get_next_coord(
                self.x, self.y, self.direction
            )
            moved = True

        if not moved:
            # Blocked by a wall: stop fully and snap prev to current tile
            self.prev_x, self.prev_y = self.x, self.y
            self.move_timer = 0.0

        self.dot_eaten_this_step = False

    def _check_collisions(self, maze: List[List[int]], event_bus: Any) -> None:
        """Check the current tile for items and consume them.

        Mutates the maze array to remove the item and publishes the event.

        Args:
            maze (List[List[int]]): The 2D grid representing the level
                geometry.
            event_bus (Any): The centralized event bus to publish events.
        """
        if not (0 <= self.y < len(maze) and 0 <= self.x < len(maze[0])):
            return
        current_tile = maze[self.y][self.x]

        # 2 = Regular Dot (Pacgum)
        if current_tile == 2:
            # Remove dot, turn into empty corridor (0)
            maze[self.y][self.x] = 0
            self.dots_eaten_count += 1
            step = self.dots_eaten_count % 2
            event_bus.publish(
                "DOT_EATEN",
                {"step": step, "tone": step, "count": self.dots_eaten_count}
            )

        # 3 = Super Pacgum
        elif current_tile == 3:
            maze[self.y][self.x] = 0  # Remove super pacgum
            self.dots_eaten_count += 1
            event_bus.publish(
                "SUPER_PACGUM_EATEN",
                {"count": self.dots_eaten_count}
            )

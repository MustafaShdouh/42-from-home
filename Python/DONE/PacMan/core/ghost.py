"""Ghost entity and state machine."""

from collections import deque
import logging
import random
from typing import Tuple, Any, List, Optional, Dict
from core.ai.base_strategy import BehaviorStrategy

logger = logging.getLogger(__name__)


class Ghost:
    """Represents a Ghost entity with its own internal State Machine.

    Attributes:
        x (int): The current X grid coordinate.
        y (int): The current Y grid coordinate.
        color (str): The visual color identifier (e.g., 'RED', 'PINK').
        mode (str): Current AI mode ('CHASE', 'SCATTER', 'FRIGHTENED', 'DEAD').
        strategy (BehaviorStrategy): The targeting algorithm used during
            CHASE mode.
        direction (str): The current movement direction.
    """

    def __init__(
        self,
        start_x: int,
        start_y: int,
        color: str,
        strategy: BehaviorStrategy,
    ) -> None:
        """Initialize a Ghost by injecting a specific AI strategy.

        Args:
            start_x (int): Starting X grid coordinate.
            start_y (int): Starting Y grid coordinate.
            color (str): The ghost's identity color.
            strategy (BehaviorStrategy): The Chase mode targeting algorithm.
        """
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.prev_x = start_x
        self.prev_y = start_y
        self.color = color

        self.strategy = strategy

        self.mode = "SCATTER"
        self.wave_mode = "SCATTER"
        self.direction = "LEFT"
        self.frightened_timer = 0.0
        self.dead_timer = 0.0
        self.base_speed = 6.0
        self.speed = 6.0  # tiles per second
        self.move_timer = 0.0
        self.home_arrived = False
        self.transit_timer = 0.0
        self._corridor_dist_cache: Optional[
            Tuple[int, int, Dict[Tuple[int, int], int]]
        ] = None
        self._corridor_maze: Optional[List[List[int]]] = None

    def _set_speed(self, new_speed: float) -> None:
        """Set movement speed while scaling move_timer to avoid visual jumps.

        Args:
            new_speed (float): The new speed in tiles per second.
        """
        old_speed = getattr(self, "speed", 6.0)
        if old_speed > 0 and new_speed > 0:
            progress = min(1.0, max(0.0, self.move_timer * old_speed))
            self.move_timer = progress / new_speed
        self.speed = new_speed

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

    @property
    def is_flashing(self) -> bool:
        """Check if frightened mode is within its final warning period.

        Returns:
            bool: True if ghost is frightened and timer is <= 2.0 seconds.
        """
        return self.mode == "FRIGHTENED" and self.frightened_timer <= 2.0

    def set_frightened(self, duration: float = 6.0) -> None:
        """Trigger the frightened state (turn blue and slow down).

        Args:
            duration (float): Duration in seconds for the frightened state.
                Defaults to 6.0.
        """
        if self.mode != "DEAD":
            if duration <= 0.0:
                # Authentic Level 17 & 19+: reverse without turning blue
                self._reverse_direction()
                return
            self.mode = "FRIGHTENED"
            self.frightened_timer = duration
            self._set_speed(getattr(self, "base_speed", 6.0) * 0.65)
            self._reverse_direction()

    def set_dead(self) -> None:
        """Transition the ghost into dead eyes mode returning home."""
        self.mode = "DEAD"
        self.home_arrived = False
        self.transit_timer = 0.0
        self.dead_timer = 3.0
        self.frightened_timer = 0.0
        self._set_speed(getattr(self, "base_speed", 6.0) * 2.0)

    def revive(self, wave_mode: Optional[str] = None) -> None:
        """Revive the ghost upon reaching its starting base.

        Args:
            wave_mode (Optional[str]): Active wave mode to resume.
                Defaults to None.
        """
        if wave_mode is not None:
            self.mode = wave_mode
        else:
            self.mode = self.wave_mode
        self.speed = self.base_speed
        self.dead_timer = 0.0
        self.transit_timer = 0.0
        self.home_arrived = False
        self.frightened_timer = 0.0
        self.prev_x, self.prev_y = self.x, self.y
        self.move_timer = 0.0

    def tick(
        self, dt: float, event_bus: Any, wave_mode: str = "CHASE"
    ) -> None:
        """Update internal timers for frightened and dead modes.

        Args:
            dt (float): Delta time in seconds.
            event_bus (Any): Central event bus to publish events.
            wave_mode (str): Active wave mode ('SCATTER' or 'CHASE') to
                resume upon timer expiration. Defaults to 'CHASE'.
        """
        self.wave_mode = wave_mode
        if self.mode == "FRIGHTENED":
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.mode = wave_mode
                self._set_speed(getattr(self, "base_speed", 6.0))
                event_bus.publish("FRIGHTENED_MODE_ENDED")
        elif self.mode == "DEAD":
            if self.home_arrived:
                self.dead_timer -= dt
                if self.dead_timer <= 0:
                    self.revive(wave_mode)
                    event_bus.publish(
                        "GHOST_REVIVED", {"ghost": self.color}
                    )
            else:
                if self.x == self.start_x and self.y == self.start_y:
                    self.home_arrived = True
                    self.dead_timer = 3.0
                else:
                    self.transit_timer += dt
                    if self.transit_timer >= 25.0:
                        self.x = self.start_x
                        self.y = self.start_y
                        self.prev_x = self.start_x
                        self.prev_y = self.start_y
                        self.move_timer = 0.0
                        self.home_arrived = True
                        self.dead_timer = 3.0

    def _reverse_direction(self) -> None:
        """Reverse the ghost's current movement direction safely."""
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        self.direction = opposites.get(self.direction, self.direction)

    def calculate_target(self, game_state: Any) -> Tuple[int, int]:
        """Calculate the current target tile based on the active mode.

        Args:
            game_state (Any): The central game context.

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the target tile.
        """
        if self.mode == "CHASE":
            # Delegate entirely to the injected Strategy Pattern object
            target = self.strategy.calculate_target(self, game_state)
            return target if target else (self.x, self.y)

        elif self.mode == "SCATTER":
            # Target outside the corner wall into the void to create
            # authentic arcade perimeter patrol loops
            max_x = len(game_state.maze[0]) - 1
            max_y = len(game_state.maze) - 1
            anchor_x = -3 if self.start_x <= max_x // 2 else max_x + 3
            anchor_y = -3 if self.start_y <= max_y // 2 else max_y + 3
            return (anchor_x, anchor_y)

        elif self.mode == "DEAD":
            # Target the ghost's home house (its starting corner/base)
            return (self.start_x, self.start_y)

        elif self.mode == "FRIGHTENED":
            # Run away from the player by targeting the exact opposite
            # direction
            target_x = self.x + (self.x - game_state.player.x)
            target_y = self.y + (self.y - game_state.player.y)
            return (target_x, target_y)

        return (self.x, self.y)

    def _find_next_step_bfs(
        self,
        target_x: int,
        target_y: int,
        maze: List[List[int]],
    ) -> Optional[Tuple[str, Tuple[int, int]]]:
        """Find the next optimal step towards target using BFS.

        Args:
            target_x (int): Target X grid coordinate.
            target_y (int): Target Y grid coordinate.
            maze (List[List[int]]): Level grid geometry.

        Returns:
            Optional[Tuple[str, Tuple[int, int]]]: Next direction and
                coordinate, or None if target is unreachable.
        """
        start = (self.x, self.y)
        target = (target_x, target_y)
        if start == target:
            return None

        queue: deque[Tuple[int, int]] = deque([start])
        parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
        dirs = [
            ("UP", 0, -1),
            ("LEFT", -1, 0),
            ("DOWN", 0, 1),
            ("RIGHT", 1, 0),
        ]

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == target:
                break
            for d_name, dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= ny < len(maze)
                    and 0 <= nx < len(maze[0])
                    and maze[ny][nx] != 1
                ):
                    if (nx, ny) not in parent and (nx, ny) != start:
                        parent[(nx, ny)] = ((cx, cy), d_name)
                        queue.append((nx, ny))

        if target not in parent:
            return None

        curr = target
        step: Optional[Tuple[str, Tuple[int, int]]] = None
        while curr in parent:
            prev_cell, d_name = parent[curr]
            if prev_cell == start:
                step = (d_name, curr)
                break
            curr = prev_cell

        return step

    def _get_corridor_distances(
        self,
        target_x: int,
        target_y: int,
        maze: List[List[int]],
    ) -> Dict[Tuple[int, int], int]:
        """Compute shortest corridor distance from target to all maze cells.

        Uses Breadth-First Search (BFS) to prevent ghosts from becoming trapped
        in local Euclidean distance minima within procedural mazes.

        Args:
            target_x (int): Target X grid coordinate.
            target_y (int): Target Y grid coordinate.
            maze (List[List[int]]): Level grid geometry.

        Returns:
            Dict[Tuple[int, int], int]: Mapping from (x, y) to corridor step
                distance.
        """
        if (
            self._corridor_dist_cache is not None
            and self._corridor_maze is maze
            and self._corridor_dist_cache[0] == target_x
            and self._corridor_dist_cache[1] == target_y
        ):
            return self._corridor_dist_cache[2]

        h = len(maze)
        w = len(maze[0])
        tx, ty = target_x, target_y
        if not (0 <= ty < h and 0 <= tx < w) or maze[ty][tx] == 1:
            best_d = float("inf")
            best_c = (1, 1)
            for y in range(h):
                for x in range(w):
                    if maze[y][x] != 1:
                        d = (x - tx) ** 2 + (y - ty) ** 2
                        if d < best_d:
                            best_d = d
                            best_c = (x, y)
            tx, ty = best_c

        dist_map: Dict[Tuple[int, int], int] = {(tx, ty): 0}
        queue: deque[Tuple[int, int]] = deque([(tx, ty)])
        dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]

        while queue:
            cx, cy = queue.popleft()
            cd = dist_map[(cx, cy)]
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= ny < h
                    and 0 <= nx < w
                    and maze[ny][nx] != 1
                    and (nx, ny) not in dist_map
                ):
                    dist_map[(nx, ny)] = cd + 1
                    queue.append((nx, ny))

        self._corridor_dist_cache = (target_x, target_y, dist_map)
        self._corridor_maze = maze
        return dist_map

    def move_towards(
        self,
        target_x: int,
        target_y: int,
        maze: List[List[int]],
        dt: float,
        other_ghosts: Optional[List["Ghost"]] = None,
    ) -> None:
        """Move the ghost one tile towards the target on a fixed timer.

        Edible ghosts maximize corridor distance from the player. Overlapping
        non-edible ghosts can branch randomly to avoid merging visually.

        Args:
            target_x (int): The target X coordinate.
            target_y (int): The target Y coordinate.
            maze (List[List[int]]): The level grid geometry.
            dt (float): The delta time since last frame.
            other_ghosts (Optional[List[Ghost]]): Peer ghosts to detect
                overlap. Defaults to None.
        """
        if self.speed <= 0:
            return

        self.move_timer += dt
        if self.move_timer < (1.0 / self.speed):
            return
        self.move_timer -= (1.0 / self.speed)

        if self.mode == "DEAD":
            if self.x == self.start_x and self.y == self.start_y:
                self.prev_x, self.prev_y = self.x, self.y
                self.move_timer = 0.0
                if not self.home_arrived:
                    self.home_arrived = True
                    self.dead_timer = 3.0
                return
            bfs_step = self._find_next_step_bfs(target_x, target_y, maze)
            if bfs_step is not None:
                next_dir, (next_x, next_y) = bfs_step
                self.prev_x, self.prev_y = self.x, self.y
                self.x, self.y = next_x, next_y
                self.direction = next_dir
                if self.x == self.start_x and self.y == self.start_y:
                    self.home_arrived = True
                    self.dead_timer = 3.0
                return

        dirs = {"UP": (0, -1), "LEFT": (-1, 0),
                "DOWN": (0, 1), "RIGHT": (1, 0)}
        opposites = {"UP": "DOWN", "DOWN": "UP",
                     "LEFT": "RIGHT", "RIGHT": "LEFT"}
        reverse_dir = opposites.get(self.direction, "")

        valid_moves: List[Tuple[str, Tuple[int, int]]] = []
        for d_name in ["UP", "LEFT", "DOWN", "RIGHT"]:
            if d_name == reverse_dir and self.mode != "FRIGHTENED":
                continue
            dx, dy = dirs[d_name]
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= ny < len(maze)
                and 0 <= nx < len(maze[0])
                and maze[ny][nx] != 1
            ):
                valid_moves.append((d_name, (nx, ny)))

        if not valid_moves:
            dx, dy = dirs.get(reverse_dir, (0, 0))
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= ny < len(maze)
                and 0 <= nx < len(maze[0])
                and maze[ny][nx] != 1
            ):
                self.prev_x, self.prev_y = self.x, self.y
                self.x, self.y = nx, ny
                self.direction = reverse_dir
            else:
                self.prev_x, self.prev_y = self.x, self.y
                self.move_timer = 0.0
            return

        overlapping = False
        occupied_next: List[Tuple[int, int]] = []
        if other_ghosts:
            for peer in other_ghosts:
                if peer is self:
                    continue
                if peer.x == self.x and peer.y == self.y:
                    overlapping = True
                if peer.prev_x == self.x and peer.prev_y == self.y:
                    overlapping = True
                    occupied_next.append((peer.x, peer.y))

        if self.mode == "FRIGHTENED":
            # calculate_target mirrors Pac-Man across this ghost's tile.
            player_x = 2 * self.x - target_x
            player_y = 2 * self.y - target_y
            distances = self._get_corridor_distances(
                player_x, player_y, maze
            )
            farthest = max(distances.get(pos, -1) for _, pos in valid_moves)
            safest = [
                move for move in valid_moves
                if distances.get(move[1], -1) == farthest
            ]
            chosen_dir, chosen_move = random.choice(safest)
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = chosen_move
            self.direction = chosen_dir
            return

        # At an intersection, overlapping ghosts may branch randomly.
        if overlapping and len(valid_moves) > 1:
            unoccupied = [m for m in valid_moves if m[1] not in occupied_next]
            candidates = unoccupied if unoccupied else valid_moves
            chosen_dir, chosen_move = random.choice(candidates)
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = chosen_move
            self.direction = chosen_dir
            return

        # In CHASE mode, use corridor distance to avoid local minima traps
        if self.mode == "CHASE":
            dist_map = self._get_corridor_distances(target_x, target_y, maze)
            best_cost = float("inf")
            best_move = (self.x, self.y)
            best_dir = self.direction
            for d_name, pos in valid_moves:
                cost = dist_map.get(pos, float("inf"))
                if cost < best_cost:
                    best_cost = cost
                    best_move = pos
                    best_dir = d_name
        else:
            best_dist = float("inf")
            best_move = (self.x, self.y)
            best_dir = self.direction
            for d_name, pos in valid_moves:
                dist = (target_x - pos[0]) ** 2 + (target_y - pos[1]) ** 2
                if dist < best_dist:
                    best_dist = dist
                    best_move = pos
                    best_dir = d_name

        self.prev_x, self.prev_y = self.x, self.y
        self.x, self.y = best_move
        self.direction = best_dir

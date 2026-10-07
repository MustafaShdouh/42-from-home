import random
import sys
from typing import Optional
from .models import (
    Coord,
    WallGrid,
    DIRECTIONS,
    PATTERN_WIDTH,
    PATTERN_HEIGHT,
    PATTERN_OFFSETS,
)


class GridManager:
    """manages the 2D grid of walls for the maze.

    this class handles checking boundaries, placing the '42' pattern,
    and opening passages between cells while preventing 3x3 open areas.

    attributes:
        width (int): maze width.
        height (int): maze height.
        entry (Coord): entry coordinate.
        exit (Coord): exit coordinate.
        perfect (bool): whether the maze should be perfect.
        grid (WallGrid): the 2D array storing cell walls.
        pattern_cells (set[Coord]): set of coordinates
        reserved for the 42 pattern.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit_coords: Coord,
        perfect: bool,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_coords
        self.perfect = perfect
        # 3shan seed for reproducibility
        self._rng = random.Random(seed)
        self.grid: WallGrid = []
        self.pattern_cells: set[Coord] = set()
        self.reset_state()

    def reset_state(self) -> None:
        """resets the grid so all walls are completely closed."""
        # close all the maze walls so we can make our path
        self.grid = [
            [
                {"N": True, "E": True, "S": True, "W": True}
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]
        # try to carve out space for the 42 pattern
        self.pattern_cells = self._choose_pattern_cells()

    def is_inside(self, cell: Coord) -> bool:
        """checks if a cell coordinate is inside the maze boundaries."""
        # just for checking boundaries
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def cell_id(self, x: int, y: int) -> int:
        """converts a 2D coordinate to a 1D ID for Union-Find."""
        # from 2d coordinate to int id
        return y * self.width + x

    def _choose_pattern_cells(self) -> set[Coord]:
        """finds a valid spot for the 42 pattern without
        overlapping critical cells."""
        # if the maze is too small, we just abort pattern placement
        if self.width < PATTERN_WIDTH + 2 or self.height < PATTERN_HEIGHT + 2:
            print(
                "Error: Maze size is too small to include the "
                "'42' pattern. Omitting.",
                file=sys.stderr,
            )
            return set()

        # we cant put the pattern on the start or end
        protected: set[Coord] = {self.entry, self.exit}

        # if imperfect, the centre must be clear for the Pac-Man player spawn
        if not self.perfect:
            centre = (self.width // 2, self.height // 2)
            protected.add(centre)

        # we try to place it as close to the actual centre as possible
        target_x = (self.width - PATTERN_WIDTH) // 2
        target_y = (self.height - PATTERN_HEIGHT) // 2
        candidates: list[Coord] = []

        for start_y in range(1, self.height - PATTERN_HEIGHT):
            for start_x in range(1, self.width - PATTERN_WIDTH):
                candidates.append((start_x, start_y))

        # sort by distance to centre
        candidates.sort(
            key=lambda pos: abs(pos[0] - target_x) + abs(pos[1] - target_y)
        )

        for start_x, start_y in candidates:
            cells = {
                (start_x + dx, start_y + dy) for dx, dy in PATTERN_OFFSETS
            }
            if cells.isdisjoint(protected):
                return cells

        return set()

    def get_active_cells(self) -> list[Coord]:
        """returns all cells that are not part of the 42 pattern."""
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.pattern_cells
        ]

    def candidate_edges(self) -> list[tuple[Coord, Coord, str]]:
        """finds all potential walls (edges) that we can knock down."""
        edges: list[tuple[Coord, Coord, str]] = []
        for y in range(self.height):
            for x in range(self.width):
                # ignore pattern cells
                if (x, y) in self.pattern_cells:
                    continue

                if x + 1 < self.width and (x + 1, y) not in self.pattern_cells:
                    edges.append(((x, y), (x + 1, y), "E"))

                if (
                    y + 1 < self.height
                    and (x, y + 1) not in self.pattern_cells
                ):
                    edges.append(((x, y), (x, y + 1), "S"))
        return edges

    def open_passage(self, x: int, y: int, direction: str) -> bool:
        """knocks down a wall between a cell and its neighbor."""
        dx, dy, opposite = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        if not self.is_inside((nx, ny)):
            return False

        if (x, y) in self.pattern_cells or (nx, ny) in self.pattern_cells:
            return False

        # update both sides of the wall for coherency
        self.grid[y][x][direction] = False
        self.grid[ny][nx][opposite] = False
        return True

    def is_open_between(self, first: Coord, second: Coord) -> bool:
        """checks if the passage between two adjacent cells is open."""
        x1, y1 = first
        x2, y2 = second
        dx, dy = x2 - x1, y2 - y1

        for direction, (step_x, step_y, _) in DIRECTIONS.items():
            if (dx, dy) == (step_x, step_y):
                return not self.grid[y1][x1][direction]
        return False

    def would_create_open_3x3(self, first: Coord, second: Coord) -> bool:
        """simulates opening a wall to see if it
        violates the 3x3 open space rule."""
        changed: Optional[tuple[int, int, str, str]] = None

        # temporarily open it
        if not self.is_open_between(first, second):
            x1, y1 = first
            x2, y2 = second
            direction = self.direction_between(first, second)
            opposite = DIRECTIONS[direction][2]
            self.grid[y1][x1][direction] = False
            self.grid[y2][x2][opposite] = False
            changed = (x1, y1, direction, opposite)

        # check for 3x3 areas locally (O(1) time instead of O(W*H))
        creates_open_area = self.has_open_3x3_around(first, second)

        # revert back
        if changed is not None:
            x1, y1, direction, opposite = changed
            dx, dy, _ = DIRECTIONS[direction]
            x2, y2 = x1 + dx, y1 + dy
            self.grid[y1][x1][direction] = True
            self.grid[y2][x2][opposite] = True

        return creates_open_area

    def _is_3x3_open(self, left: int, top: int) -> bool:
        """checks if a specific 3x3 block is fully open."""
        cells = {
            (x, y) for y in range(top, top + 3) for x in range(left, left + 3)
        }
        if cells & self.pattern_cells:
            return False

        for y in range(top, top + 3):
            for x in range(left, left + 2):
                if self.grid[y][x]["E"]:
                    return False
        for y in range(top, top + 2):
            for x in range(left, left + 3):
                if self.grid[y][x]["S"]:
                    return False
        return True

    def has_open_3x3_around(self, first: Coord, second: Coord) -> bool:
        """checks for 3x3 open areas only around the modified cells."""
        x1, y1 = first
        x2, y2 = second
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        start_x = max(0, min_x - 2)
        end_x = min(self.width - 3, max_x)
        start_y = max(0, min_y - 2)
        end_y = min(self.height - 3, max_y)

        if start_x > end_x or start_y > end_y:
            return False

        for top in range(start_y, end_y + 1):
            for left in range(start_x, end_x + 1):
                if self._is_3x3_open(left, top):
                    return True
        return False

    def has_open_3x3(self) -> bool:
        """checks the entire grid for any 3x3 block of fully open space."""
        if self.width < 3 or self.height < 3:
            return False

        for top in range(self.height - 2):
            for left in range(self.width - 2):
                if self._is_3x3_open(left, top):
                    return True
        return False

    def direction_between(self, first: Coord, second: Coord) -> str:
        """gets the string direction ('N', 'E', 'S', 'W') between two cells."""
        x1, y1 = first
        x2, y2 = second
        delta = (x2 - x1, y2 - y1)

        for direction, (dx, dy, _) in DIRECTIONS.items():
            if delta == (dx, dy):
                return direction
        raise ValueError("Cells are not direct neighbours.")

    def closed_active_neighbours(self, cell: Coord) -> list[tuple[Coord, str]]:
        """gets all neighbors of a cell that currently share a closed wall."""
        x, y = cell
        neighbours: list[tuple[Coord, str]] = []

        for direction, (dx, dy, _) in DIRECTIONS.items():
            neighbour = (x + dx, y + dy)
            if (
                self.is_inside(neighbour)
                and neighbour not in self.pattern_cells
                and self.grid[y][x][direction]
            ):
                neighbours.append((neighbour, direction))

        # randomizing neighbor order to keep the maze unpredictable
        self._rng.shuffle(neighbours)
        return neighbours

    def degree(self, cell: Coord) -> int:
        """counts how many open passages connect to a cell."""
        if cell in self.pattern_cells:
            return 0

        x, y = cell
        degree = 0
        for direction, (dx, dy, _) in DIRECTIONS.items():
            neighbour = (x + dx, y + dy)
            if (
                self.is_inside(neighbour)
                and neighbour not in self.pattern_cells
                and not self.grid[y][x][direction]
            ):
                degree += 1
        return degree

    def try_open_extra_wall(self, cell: Coord) -> bool:
        """attempts to knock down one more wall connected to a cell."""
        x, y = cell
        for neighbour, direction in self.closed_active_neighbours(cell):
            # check the 3x3 rule before knocking it down!
            if self.would_create_open_3x3(cell, neighbour):
                continue
            return self.open_passage(x, y, direction)
        return False

"""Maze loader and adapter module for Pac-Man."""

# mypy: disable-error-code=import-untyped

import logging
from typing import List

# Wrap in try-except to prevent immediate crash if the external package
# isn't installed yet.
try:
    from mazegenerator import MazeGenerator
except ImportError:
    MazeGenerator = None

logger = logging.getLogger(__name__)


class MazeAdapter:
    """Adapt the external A-Maze-ing generator to internal grid format."""

    def __init__(
        self,
        width: int = 15,
        height: int = 15,
        seed: int = 0,
        enable_42: bool = True,
    ) -> None:
        """Initialize the maze adapter.

        Args:
            width (int): The width in external maze cells.
            height (int): The height in external maze cells.
            seed (int): The random seed (0 for random).
            enable_42 (bool): Whether 42 logo is enabled (retained for API).
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.enable_42 = enable_42

    def generate_level(self) -> List[List[int]]:
        """Generate a Pac-Man compatible grid using the external package.

        Uses native MazeGenerator directly without overriding internal logic.

        Returns:
            List[List[int]]: A 2D grid where 0=corridor, 1=wall,
                2=pacgum, 3=super-pacgum.
        """
        if MazeGenerator is None:
            logger.error(
                "mazegenerator package is not installed. Using safe fallback."
            )
            return self._generate_safe_fallback()

        try:
            gen = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed,
            )
            raw_maze = gen.maze
            grid = self._convert_to_block_grid(raw_maze)

            # Place the 4 Super-Pacgums (3) in the 4 extreme corners
            grid_h = len(grid)
            grid_w = len(grid[0])
            if any(
                grid[y][x] == 1
                for x, y in (
                    (1, 1), (grid_w - 2, 1),
                    (1, grid_h - 2), (grid_w - 2, grid_h - 2),
                )
            ):
                raise ValueError("Generated maze has blocked corners")
            self._place_super_pacgum(grid, 1, 1, 1, 1)  # Top-Left
            self._place_super_pacgum(grid, grid_w - 2, 1, -1, 1)  # Top-Right
            self._place_super_pacgum(grid, 1, grid_h - 2, 1, -1)  # Bottom-Left
            self._place_super_pacgum(
                grid, grid_w - 2, grid_h - 2, -1, -1
            )  # Bottom-Right

            return grid
        except Exception as e:
            logger.error(
                "External MazeGenerator failed: %s. Using safe fallback.", e
            )
            return self._generate_safe_fallback()

    def _convert_to_block_grid(
        self, raw_maze: List[List[int]]
    ) -> List[List[int]]:
        """Convert a bitmask maze into a block-based grid.

        The external maze uses bitmasks (1=N, 2=E, 4=S, 8=W) where walls don't
        occupy space. We expand a WxH maze into a (2W+1)x(2H+1) grid where
        walls are actual blocks. Cells with bitmask 15 are solid 42 walls.

        Args:
            raw_maze (List[List[int]]): The bitmask maze.

        Returns:
            List[List[int]]: The block grid populated with pacgums.
        """
        if not raw_maze or not raw_maze[0]:
            raise ValueError("Generator returned an empty maze")

        h = len(raw_maze)
        w = len(raw_maze[0])
        if h != self.height or w != self.width:
            raise ValueError("Generator returned unexpected maze dimensions")
        if any(
            len(row) != w
            or any(type(cell) is not int or not 0 <= cell <= 15
                   for cell in row)
            for row in raw_maze
        ):
            raise ValueError("Generator returned an invalid bitmask grid")

        grid_h = 2 * h + 1
        grid_w = 2 * w + 1
        grid = [[1 for _ in range(grid_w)] for _ in range(grid_h)]

        for y in range(h):
            for x in range(w):
                cell_val = raw_maze[y][x]
                if cell_val == 15:
                    continue

                cx, cy = 2 * x + 1, 2 * y + 1
                grid[cy][cx] = 2

                if not (cell_val & 1):
                    grid[cy - 1][cx] = 2
                if not (cell_val & 4):
                    grid[cy + 1][cx] = 2
                if not (cell_val & 2):
                    grid[cy][cx + 1] = 2
                if not (cell_val & 8):
                    grid[cy][cx - 1] = 2

        return grid

    def _place_super_pacgum(
        self,
        grid: List[List[int]],
        start_x: int,
        start_y: int,
        dir_x: int,
        dir_y: int,
    ) -> None:
        """Place a super-pacgum in the nearest open corridor corner.

        Args:
            grid (List[List[int]]): The maze grid.
            start_x (int): The corner x-coordinate to start searching from.
            start_y (int): The corner y-coordinate to start searching from.
            dir_x (int): The direction to scan on the x-axis (1 or -1).
            dir_y (int): The direction to scan on the y-axis (1 or -1).
        """
        for y in range(start_y, start_y + (5 * dir_y), dir_y):
            for x in range(start_x, start_x + (5 * dir_x), dir_x):
                if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                    if grid[y][x] in (0, 2):
                        grid[y][x] = 3
                        return

    def _generate_safe_fallback(self) -> List[List[int]]:
        """Return a basic 9x7 hardcoded grid if external generator fails.

        Returns:
            List[List[int]]: Hardcoded 2D fallback maze grid.
        """
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 2, 2, 1, 2, 2, 3, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 0, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 3, 2, 2, 1, 2, 2, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

from typing import Optional
from .models import Coord
from .grid import GridManager
from .union_find import UnionFind
from .exporter import MazeExporter


class MazeGenerator:
    """the main orchestrator for creating a maze.

    ties together the GridManager, UnionFind (Kruskal's algorithm),
    and MazeExporter to build both perfect and imperfect mazes.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit_coords: Coord,
        perfect: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        """sets up the sub-components for maze generation."""
        self.grid_manager = GridManager(
            width, height, entry, exit_coords, perfect, seed
        )
        self.union_find = UnionFind(width * height)

    def _ensure_min_degree(self, cell: Coord, minimum: int) -> None:
        """forces a cell to have a minimum number of open walls.

        used to make sure corners and centres are accessible for Pac-Man mode.
        """
        if (
            not self.grid_manager.is_inside(cell)
            or cell in self.grid_manager.pattern_cells
        ):
            return
        while self.grid_manager.degree(cell) < minimum:
            if not self.grid_manager.try_open_extra_wall(cell):
                break

    def _remove_dead_ends(self) -> None:
        """finds and eliminates dead ends by knocking down walls.

        a dead end is any cell with exactly 1 open wall (degree == 1).
        """
        active = self.grid_manager.get_active_cells()
        while True:
            dead_ends = [
                cell for cell in active if self.grid_manager.degree(cell) == 1
            ]
            if not dead_ends:
                return

            self.grid_manager._rng.shuffle(dead_ends)
            changed = False

            for cell in dead_ends:
                if self.grid_manager.degree(cell) != 1:
                    continue
                if self.grid_manager.try_open_extra_wall(cell):
                    changed = True

            if not changed:
                return

    def _open_edge_count(self) -> int:
        """counts the total number of missing
        walls (open edges) in the grid."""
        count = 0
        for y in range(self.grid_manager.height):
            for x in range(self.grid_manager.width):
                if (x, y) in self.grid_manager.pattern_cells:
                    continue
                # check if there's no wall between current
                # cell and the one to its right
                if (
                    x + 1 < self.grid_manager.width
                    and (x + 1, y) not in self.grid_manager.pattern_cells
                    and not self.grid_manager.grid[y][x]["E"]
                ):
                    count += 1
                # check if there's no wall between current
                # cell and the one below it
                if (
                    y + 1 < self.grid_manager.height
                    and (x, y + 1) not in self.grid_manager.pattern_cells
                    and not self.grid_manager.grid[y][x]["S"]
                ):
                    count += 1
        return count

    def _cycle_rank(self) -> int:
        """calculates how many independent loops exist in the maze.

        formula: Cycles = Edges - Vertices + 1.
        """
        vertices = len(self.grid_manager.get_active_cells())
        if vertices == 0:
            return 0
        return self._open_edge_count() - vertices + 1

    def _make_imperfect(self) -> None:
        """modifies a perfect maze to make it a playable Pac-Man board.

        this knocks down extra walls, removes dead ends, and forces the
        corners and centre to be open corridors.
        """
        corners: tuple[Coord, ...] = (
            (0, 0),
            (self.grid_manager.width - 1, 0),
            (0, self.grid_manager.height - 1),
            (self.grid_manager.width - 1, self.grid_manager.height - 1),
        )

        # open up the corners first
        for corner in corners:
            self._ensure_min_degree(corner, 2)

        # make sure the player spawn point is open
        centre = (self.grid_manager.width // 2, self.grid_manager.height // 2)
        self._ensure_min_degree(centre, 2)

        # scrub out all dead ends
        self._remove_dead_ends()

        # check them again just to be safe
        for corner in corners:
            self._ensure_min_degree(corner, 2)
        self._ensure_min_degree(centre, 2)

        active = self.grid_manager.get_active_cells()
        self.grid_manager._rng.shuffle(active)

        attempts = 0
        max_attempts = max(20, len(active) * 4)

        # keep knocking down walls until we
        # have at least 2 loops (cycle rank >= 2)
        while self._cycle_rank() < 2 and attempts < max_attempts:
            cell = self.grid_manager._rng.choice(active)
            self.grid_manager.try_open_extra_wall(cell)
            attempts += 1

        # validations to ensure the imperfect maze meets PDF requirements
        if self._cycle_rank() < 2:
            raise ValueError(
                "Unable to create at least two independent "
                "routes for PERFECT=False."
            )

        if any(self.grid_manager.degree(corner) < 2 for corner in corners):
            raise ValueError(
                "Maze dimensions are too small to keep all "
                "four corners as open corridors."
            )

        # dead-ends are geometrically trapped,
        # which is acceptable per the PDF guidelines.
        pass

    def generate(self) -> None:
        """executes Kruskal's algorithm to generate the maze structure."""
        self.grid_manager.reset_state()
        self.union_find = UnionFind(
            self.grid_manager.width * self.grid_manager.height
        )
        active = self.grid_manager.get_active_cells()

        if (
            self.grid_manager.entry in self.grid_manager.pattern_cells
            or self.grid_manager.exit in self.grid_manager.pattern_cells
        ):
            raise ValueError("ENTRY or EXIT overlaps the '42' pattern.")

        edges = self.grid_manager.candidate_edges()
        self.grid_manager._rng.shuffle(edges)
        merges = 0

        # kruskal's algorithm
        for first, second, direction in edges:
            first_id = self.grid_manager.cell_id(*first)
            second_id = self.grid_manager.cell_id(*second)

            # if they are not in the same set,
            # merge them and tear down the wall
            if self.union_find.union(first_id, second_id):
                self.grid_manager.open_passage(first[0], first[1], direction)
                merges += 1

        expected_merges = len(active) - 1
        if active and merges != expected_merges:
            raise ValueError(
                "The chosen maze parameters make"
                "the active cells disconnected."
            )

        # apply Pac-Man logic if requested
        if not self.grid_manager.perfect:
            self._make_imperfect()

    def write_output(self, filepath: str) -> None:
        """passes the grid to the exporter to be written to a file."""
        MazeExporter.write_output(self.grid_manager, filepath)

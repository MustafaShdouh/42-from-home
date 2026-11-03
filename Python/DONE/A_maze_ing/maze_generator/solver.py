from collections import deque
from .models import Coord, DIRECTIONS
from .grid import GridManager


class MazeSolver:
    """handles pathfinding through the maze using BFS.

    This class guarantees we find the absolute shortest path from entry
    to exit, meeting the PDF requirements.
    """

    @staticmethod
    def solve(grid_manager: GridManager) -> list[str]:
        """finds the shortest path using Breadth-First Search (BFS).

        Args:
            grid_manager (GridManager): the fully generated maze grid.

        Returns:
            list[str]: A list of directions (e.g. ['N', 'E', 'E'])
            forming the shortest path.

        Raises:
            ValueError: If no valid path exists between entry and exit.
        """
        # we will use a queue for BFS to find the shortest path
        queue: deque[Coord] = deque([grid_manager.entry])
        # dict to track where we came from so we can backtrack our final path
        previous: dict[Coord, tuple[Coord, str]] = {}
        visited: set[Coord] = {grid_manager.entry}

        while queue:
            current = queue.popleft()
            if current == grid_manager.exit:
                break
            # beep boop bop
            x, y = current

            for direction, (dx, dy, _) in DIRECTIONS.items():
                neighbour = (x + dx, y + dy)
                # check if we are going out of bounds,
                # hitting the '42' pattern,
                # hitting a closed wall, or re-visiting an old cell
                if (
                    not grid_manager.is_inside(neighbour)
                    or neighbour in grid_manager.pattern_cells
                    or grid_manager.grid[y][x][direction]
                    or neighbour in visited
                ):
                    continue

                visited.add(neighbour)
                previous[neighbour] = (current, direction)
                queue.append(neighbour)

        # fail safe if somehow the maze is literally unsolvable
        if grid_manager.exit not in visited:
            raise ValueError("No valid path exists from ENTRY to EXIT.")

        path: list[str] = []
        current = grid_manager.exit

        # backtracking from exit to entry to build the path
        while current != grid_manager.entry:
            parent, direction = previous[current]
            path.append(direction)
            current = parent

        # because we backtracked, the path is backwards, so flip it
        path.reverse()
        return path

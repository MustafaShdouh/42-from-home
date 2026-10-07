from .models import WALL_BITS
from .grid import GridManager
from .solver import MazeSolver


class MazeExporter:
    """handles formatting and writing the maze to the output file."""

    @staticmethod
    def write_output(grid_manager: GridManager, filepath: str) -> None:
        """writes the hexadecimal maze string,
           entry/exit coords, and path string.

        args:
            grid_manager (GridManager): the generated maze grid.
            filepath (str): target output file path.
        """

        def cell_hex(x: int, y: int) -> str:
            """calculates the hex character for a
            single cell based on its walls."""
            value = 0
            # loop over N,E,S,W and bitwise OR
            # the value if the wall is closed (True)
            for direction, bit in WALL_BITS.items():
                if grid_manager.grid[y][x][direction]:
                    value |= bit
            return f"{value:X}"

        # build the hex string row by row
        rows = [
            "".join(cell_hex(x, y) for x in range(grid_manager.width))
            for y in range(grid_manager.height)
        ]

        path = MazeSolver.solve(grid_manager)
        path_line = "".join(path)
        entry_line = f"{grid_manager.entry[0]},{grid_manager.entry[1]}"
        exit_line = f"{grid_manager.exit[0]},{grid_manager.exit[1]}"

        # writing everything nicely to the file
        with open(filepath, "w", encoding="utf-8", newline="\n") as output:
            for row in rows:
                output.write(row + "\n")
            output.write("\n")
            output.write(entry_line + "\n")
            output.write(exit_line + "\n")
            output.write(path_line + "\n")

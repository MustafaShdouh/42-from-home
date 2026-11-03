"""
data structures and constants for the maze generator.
"""

# 3shan type hints shortcuts
Coord = tuple[int, int]
# 3shan walls list[rows[cells[walls, open(false) | close(True) ]]]
WallGrid = list[list[dict[str, bool]]]

# every directions has 3 things ex: if i move North(up) then
# "N": (0, -1, "S") -> mean x will stay 0 ,
# y will -1 , and the opposite is south(down)
DIRECTIONS: dict[str, tuple[int, int, str]] = {
    "N": (0, -1, "S"),
    "E": (1, 0, "W"),
    "S": (0, 1, "N"),
    "W": (-1, 0, "E"),
}

# hexadecimal output bitmasks
WALL_BITS: dict[str, int] = {
    "N": 1,
    "E": 2,
    "S": 4,
    "W": 8,
}

# these are the exact relative cell positions to draw the "42" pattern!
PATTERN_OFFSETS: tuple[Coord, ...] = (
    # "4"
    (0, 0),
    (2, 0),
    (0, 1),
    (2, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    # "2"
    (4, 0),
    (5, 0),
    (6, 0),
    (6, 1),
    (4, 2),
    (5, 2),
    (6, 2),
    (4, 3),
    (4, 4),
    (5, 4),
    (6, 4),
)

# bounding box of the pattern
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5

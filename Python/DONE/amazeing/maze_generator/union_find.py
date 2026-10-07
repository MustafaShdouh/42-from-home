class UnionFind:
    """disjoint-set data structure for Kruskal's algorithm.

    this class helps us track which cells are connected to each other
    so we don't accidentally create loops in our perfect maze.

    attributes:
        parent (list[int]): tracks the parent/root of each cell.
        rank (list[int]): tracks the depth of the tree to keep it flat.
    """

    def __init__(self, size: int) -> None:
        """initializes the UnionFind structure.

        args:
            size (int): total number of cells (width * height).
        """
        # initially every cell is its own root parent
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        """finds the root parent of a cell, using path compression.

        args:
            i (int): the cell ID to find.

        returns:
            int: The root cell ID.
        """
        # we use it in union to know which cell from any group
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """unites two disjoint sets into one.

        args:
            i (int): the first cell ID.
            j (int): the second cell ID.

        returns:
            bool: True if they were merged, False if they
            were already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        # if they have the same root, we skip to avoid making loops
        if root_i == root_j:
            return False

        # attach the smaller tree under the bigger tree (union by rank)
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

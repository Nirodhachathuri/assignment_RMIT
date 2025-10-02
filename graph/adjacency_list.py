# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT ADJACENCY LIST.
# Class for Adjacency List representation of Graph.
#
# __author__ = 'YOUR NAME HERE'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------

from typing import List, Dict, Tuple
from graph.graph import Graph
from graph.coordinate import Coordinate


class AdjacencyListGraph(Graph):
    """
    Graph implementation using an adjacency list.
    Vertices are Coordinates (rooms), and edges are weighted paths.
    A weight of 0 between adjacent cells means a wall; weight > 0 means traversable with cost.
    """

    def __init__(self, rows: int, cols: int):
        """
        Initializes the graph with empty adjacency lists.

        @param rows: Number of rows in the maze.
        @param cols: Number of columns in the maze.
        """
        self.rows = rows
        self.cols = cols
        self.size = rows * cols

        # Set of all vertices
        self.vertices: List[Coordinate] = []

        # Adjacency list: Coordinate → List[Tuple[Coordinate, weight]]
        self.adj_list: Dict[Coordinate, List[Tuple[Coordinate, int]]] = {}

    def addVertex(self, label: Coordinate):
        """
        Adds a vertex to the graph.

        @param label: Coordinate of the room.
        """
        if label not in self.adj_list:
            self.adj_list[label] = []
            self.vertices.append(label)

        # ------------------- Helper Methods -------------------

    def _get_edge(self, vert1: Coordinate, vert2: Coordinate) -> Tuple[Coordinate, int] | None:
        """
        Internal helper to find the edge between vert1 and vert2.
        Returns the tuple (vert2, weight) if exists, else None.
        """
        if vert1 not in self.adj_list:
            return None
        for v, w in self.adj_list[vert1]:
            if v == vert2:
                return (v, w)
        return None

    def _update_edge_in_list(self, vert1: Coordinate, vert2: Coordinate, weight: int) -> bool:
        """
        Internal helper to update the weight of an existing edge.
        Returns True if updated, False if edge does not exist.
        """
        if vert1 not in self.adj_list:
            return False
        for idx, (v, w) in enumerate(self.adj_list[vert1]):
            if v == vert2:
                self.adj_list[vert1][idx] = (v, weight)
                return True
        return False

    def _remove_edge_from_list(self, vert1: Coordinate, vert2: Coordinate) -> bool:
        """
        Internal helper to remove the edge from vert1 to vert2.
        Returns True if removed, False if edge did not exist.
        """
        if vert1 not in self.adj_list:
            return False
        original_len = len(self.adj_list[vert1])
        self.adj_list[vert1] = [(v, w) for v, w in self.adj_list[vert1] if v != vert2]
        return len(self.adj_list[vert1]) < original_len

    def addVertices(self, vertLabels: List[Coordinate]):
        """
        Adds multiple rooms to the graph.

        @param vertLabels: List of Coordinates.
        """
        for label in vertLabels:
            self.addVertex(label)

    def addEdge(self, vert1: Coordinate, vert2: Coordinate, weight: int = 1) -> bool:
        """
        Adds a traversable path between two rooms if:
        1) No edge already exists,
        2) Both rooms are in the graph,
        3) The rooms are adjacent (orthogonally).

        @param vert1: Source room.
        @param vert2: Destination room.
        @param weight: Movement cost. Default is 1.

        @returns True if edge added successfully, otherwise False.
        """
        # Condition 2: Both rooms must be in the graph
        if vert1 not in self.adj_list or vert2 not in self.adj_list:
            return False

        # Condition 3: must be adjacent
        if not vert1.isAdjacent(vert2):
            return False
            
        # Ensure weight is positive for a traversable path addition
        if weight <= 0:
            return False

        # Condition 1: No edge already exists
        if self._get_edge(vert1, vert2) is not None:
            return False

        # Add undirected edge
        self.adj_list[vert1].append((vert2, weight))
        self.adj_list[vert2].append((vert1, weight))
        return True

    def updateWall(self, vert1: Coordinate, vert2: Coordinate, hasWall: bool, weight: int = 1) -> bool:
        """
        Updates wall status between two rooms.

        @param vert1: First room.
        @param vert2: Second room.
        @param hasWall: True to add wall (weight = 0), False to remove wall (weight = 1).
        @param weight: if we are remove a wall, what is the edge weight?

        @returns True if update successful.
        """
        # Check for valid rooms and adjacency
        if (
                vert1 not in self.adj_list or
                vert2 not in self.adj_list or
                not vert1.isAdjacent(vert2)
        ):
            return False

        if hasWall:
            # Add wall: remove the edge from both lists
            self._remove_edge_from_list(vert1, vert2)
            self._remove_edge_from_list(vert2, vert1)
            # Edge is now absent, so wall status is correct
            return True 
        else: # hasWall is False, remove wall (add/update edge with positive weight)
            # Ensure weight is positive when removing a wall
            if weight <= 0:
                return False
                
            # Check if edge already exists
            if self._get_edge(vert1, vert2) is not None:
                # Edge exists, update weight
                updated_1 = self._update_edge_in_list(vert1, vert2, weight)
                updated_2 = self._update_edge_in_list(vert2, vert1, weight)
                return updated_1 and updated_2
            else:
                # Edge does not exist, add it
                self.adj_list[vert1].append((vert2, weight))
                self.adj_list[vert2].append((vert1, weight))
                return True

    def print(self):
        """
        Prints the adjacency list of the graph to the terminal. Like

        (0, 0) -> [(0, 1), 1; (1, 0), 2]
        (0, 1) -> [(0, 0), 1; (1, 1), 3]
        ...

        Useful for debugging.

        @returns None
        """
        for u in self.vertices:
            edges = self.adj_list.get(u, [])
            edge_strs = [f"({v.getRow()}, {v.getCol()}), {w}" for v, w in edges]
            print(f"({u.getRow()}, {u.getCol()}) -> [{'; '.join(edge_strs)}]")

    def removeEdge(self, vert1: Coordinate, vert2: Coordinate) -> bool:
        """
        Removes the path between two rooms.

        @param vert1: First room.
        @param vert2: Second room.

        @returns True if edge removed successfully.
        """
        # Removing an edge is equivalent to adding a wall
        return self.updateWall(vert1, vert2, hasWall=True)

    def hasVertex(self, label: Coordinate) -> bool:
        """
        Checks if a room exists in the graph.

        @param label: Coordinate of the room.

        @returns True if room exists.
        """
        return label in self.adj_list

    def hasEdge(self, vert1: Coordinate, vert2: Coordinate) -> bool:
        """
        Checks if a traversable path exists between two rooms.

        @param vert1: First room.
        @param vert2: Second room.

        @returns True if edge exists and is traversable.
        """
        edge = self._get_edge(vert1, vert2)
        # An edge is traversable if it is in the list AND the weight is positive.
        return edge is not None and edge[1] > 0

    def getWallStatus(self, vert1: Coordinate, vert2: Coordinate) -> bool:
        """
        Checks if a wall exists between two rooms.

        @param vert1: First room.
        @param vert2: Second room.

        @returns True if wall exists (weight = 0), False otherwise.
        """
        # A wall exists if there is NO edge in the list between two adjacent vertices.
        if not vert1.isAdjacent(vert2):
            return True # Not adjacent is considered a wall/impassable

        if vert1 not in self.adj_list or vert2 not in self.adj_list:
            return True # If a vertex is missing, it's impassable

        return self._get_edge(vert1, vert2) is None

    def getWeight(self, vert1: Coordinate, vert2: Coordinate) -> int:
        """
        Returns the weight between two coordinates if an edge exists.

        @returns positive integer if edge exists, 0 otherwise.
        """
        edge = self._get_edge(vert1, vert2)
        # Return weight if edge exists and is positive (traversable), else 0
        return edge[1] if edge is not None and edge[1] > 0 else 0

    def getVertices(self) -> List[Coordinate]:
        return self.vertices

    def neighbours(self, label: Coordinate) -> List[Coordinate]:
        """
        Retrieves all accessible adjacent rooms.

        @param label: Coordinate of the room.

        @returns List of neighbouring Coordinates.
        """
        if label not in self.adj_list:
            return []

        # Return only neighbors with a positive weight (traversable path)
        return [neighbor for neighbor, weight in self.adj_list[label] if weight > 0]
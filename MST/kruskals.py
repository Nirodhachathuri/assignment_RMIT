# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT KRUSKALS.
# Function turns a graph into a minimum spanning tree using Kruskal's.
#
# __author__ = 'YOUR NAME HERE'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------

from graph.graph import Graph


def kruskalMST(graph: Graph) -> Graph:
    """
    Constructs and returns the minimum spanning tree (MST) of the given graph using Kruskal's algorithm.
    The returned graph is of the same type (matrix or list) and contains only the MST edges.

    @param graph: A Graph object implementing the required interface.
    @returns A new Graph object representing the MST.
    """

    # just return an empty graph if the graph is empty
    if not graph.getVertices():
        return type(graph)(graph.rows, graph.cols)

    # We know the MST will have the same number of nodes as the original input graph
    mst = type(graph)(graph.rows, graph.cols)
    vertices = graph.getVertices()
    mst.addVertices(vertices)

    all_edges = []
    
    processed_edges = set()

    for u in vertices:
        
        for v in graph.neighbours(u):
            edge_key = frozenset([u, v])
            
            
            if edge_key in processed_edges:
                continue
            
           
            w = graph.getWeight(u, v)
            
            
            if w > 0:
                
                all_edges.append((w, u, v))
                processed_edges.add(edge_key)

    all_edges.sort(key=lambda x: x[0])

    parent = {v: v for v in vertices}

    for w, u, v in all_edges:
        
        if union(u, v, parent):
            mst.addEdge(u, v, w)

    return mst


def find(coord, parent):
    """
    Recursively finds the root of the set containing `coord` using path compression.

    @param coord: The coordinate whose set root is being queried.
    @param parent: A mapping from each coordinate to its parent in the disjoint set forest.

    @returns: The root coordinate of the set containing `coord`.
    """
    if parent[coord] != coord:
        parent[coord] = find(parent[coord], parent)
    return parent[coord]


def union(a, b, parent):
    """
    Attempts to unite the sets containing `a` and `b`.

    @param a: First coordinate.
    @param b: Second coordinate.
    @param parent: Disjoint set parent mapping.

    @returns: True if the union was successful (i.e., no cycle formed), False otherwise.
    """

    root_a = find(a, parent)
    root_b = find(b, parent)
    if root_a != root_b:
        parent[root_b] = root_a
        return True
    return False

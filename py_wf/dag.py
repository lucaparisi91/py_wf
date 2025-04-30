class Dag:
    """
    A graph implementation of a DAG using an adjacency map representation.
    This allows for O(1) edge lookup time.
    """
    
    class Node:
        """Inner class to represent a node with its outgoing edges."""
        
        def __init__(self, name: str):
            """Initialize a new node with the given ID."""
            self.id = node_name
            self.outgoing = {} 
            
        def __str__(self):
            """String representation of the node."""
            return f"Node({self.id})"
            
    class Edge:
        """Inner class to represent an edge with optional data."""
        
        def __init__(self, u, v):
            """Initialize an edge from node u to node v."""
            self.source = u
            self.destination = v
            
        def __str__(self):
            """String representation of the edge."""
            return f"Edge({self.source} -> {self.destination})"
            
    def __init__(self, directed=False):
        """Initialize an empty graph."""
        self.nodes = {}  # Maps node ID to Node instance
        self.edge_count = 0
        self.directed = directed
        
    def node_count(self):
        """Return the number of nodes in the graph."""
        return len(self.nodes)
    
    @property
    def nodes(self):
        """Return a list of all node IDs in the graph."""
        return list(self.nodes.keys())

    @property        
    def edges(self):
        """Return the number of edges in the graph."""
        return self.edges

    
    def add_node(self, node_name):
        """Add a new node with the given ID to the graph."""
        if node_name not in self.nodes:
            self.nodes[node_name] = self.Node(node_name)
        return self.nodes[node_name]
              
    def get_node(self, node_name):
        """Return the node with the given ID, or None if not found."""
        return self.nodes.get(node_name)
            
    def add_edge(self, u, v, data=None):
        """
        Add an edge from node with ID u to node with ID v.
        If nodes with given IDs don't exist, they are created.
        """
        # Ensure nodes exist
        if u not in self.nodes:
            self.add_node(u)
        if v not in self.nodes:
            self.add_node(v)
            
        # Create the edge
        e = self.Edge(u, v, data)
        
        # Add edge to the source node's outgoing edges
        self.nodes[u].outgoing[v] = e
        
        # If undirected, add the reverse edge as well
        if not self.directed and u != v:  # Avoid duplicate self-loops
            self.nodes[v].outgoing[u] = self.Edge(v, u, data)
            
        self.edge_count += 1
        return e
            
    def get_edge(self, u, v):
        """
        Return the edge from node u to node v, or None if no such edge.
        """
        if u in self.nodes:
            return self.nodes[u].outgoing.get(v)
        return None
            
    def neighbors(self, node_name):
        """Return a list of IDs of all neighbors of the given node."""
        if node_name in self.nodes:
            return list(self.nodes[node_name].outgoing.keys())
        return []
            
    def incident_edges(self, node_name):
        """Return a list of all outgoing edges from the given node."""
        if node_name in self.nodes:
            return list(self.nodes[node_name].outgoing.values())
        return []
        
    def remove_edge(self, u, v):
        """Remove edge from node u to node v if it exists."""
        if u in self.nodes and v in self.nodes[u].outgoing:
            del self.nodes[u].outgoing[v]
            if not self.directed and u != v and v in self.nodes:
                del self.nodes[v].outgoing[u]
            self.edge_count -= 1
            return True
        return False
        
    def remove_node(self, node_name):
        """Remove node and all its incident edges."""
        if node_name not in self.nodes:
            return False
            
        # Remove all edges pointing to this node
        for v in self.nodes:
            if node_name in self.nodes[v].outgoing:
                del self.nodes[v].outgoing[node_name]
                self.edge_count -= 1
                
        # For undirected graphs, we've already removed all edges
        # For directed, we need to subtract the outgoing edges too
        if self.directed:
            self.edge_count -= len(self.nodes[node_name].outgoing)
            
        # Remove the node
        del self.nodes[node_name]
        return True
    
    def __str__(self):
        """Return a string representation of the graph."""

        result = [f"Dag with {self.node_count()} nodes and {self.edge_count} edges:"]
        for node_name, node in self.nodes.items():
            edges = [f"{node_name} -> {dest}" for dest in node.outgoing.keys()]
            result.append(f"  {node_name}: {', '.join(edges) if edges else 'no outgoing edges'}")
        return "\n".join(result)
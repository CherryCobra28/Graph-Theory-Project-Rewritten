import numpy as np
from time import perf_counter

class graph_drawer:
    @staticmethod
    def test_generate_random_graph( num_nodes: int, edge_probability: float) -> np.ndarray:
        if num_nodes == 0:
            err = "Graphs need more than one node"
            raise ValueError(err)
        
        
        
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                if np.random.random() < edge_probability:
                    adjacency_matrix[i, j] = 1
                    adjacency_matrix[j, i] = 1
        
        return adjacency_matrix
    @staticmethod
    def generate_random_graph( num_nodes: int, edge_probability: float) -> np.ndarray:
        if num_nodes <= 1:
            raise ValueError("Graphs need more than one node")
        
        adjacency_matrix = np.triu(np.random.random((num_nodes, num_nodes)) < edge_probability, k=1).astype(int)
        adjacency_matrix += adjacency_matrix.T
        
        return adjacency_matrix
    @staticmethod
    def generate_wheel_graph( num_nodes: int) -> np.ndarray:
        if num_nodes == 0:
            err = "Graphs need more than one node"
            raise ValueError(err)
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        # Connect nodes in a cycle
        for i in range(num_nodes - 1):
            adjacency_matrix[i, i+1] = 1
            adjacency_matrix[i+1, i] = 1
        
        # Connect the last node with all others
        adjacency_matrix[num_nodes-1, 0] = 1
        adjacency_matrix[0, num_nodes-1] = 1
        
        return adjacency_matrix

    @staticmethod
    def generate_barabasi_albert_graph( num_nodes: int, num_edges_to_attach: int, existing_graph: np.ndarray)->np.ndarray:
        if num_nodes == 0:
            err = "Graphs need more than one node"
            raise ValueError(err)
        if num_nodes < num_edges_to_attach:
            raise ValueError("The number of edges added must be less than the number of nodes")
        
        if existing_graph is None:
            adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
            degrees = np.zeros(num_nodes, dtype=int)

            # Connect the first two nodes
            adjacency_matrix[0, 1] = 1
            adjacency_matrix[1, 0] = 1
            degrees[0] += 1
            degrees[1] += 1
        else:
            existing_size = existing_graph.shape[0]
            if num_nodes < existing_size:
                raise ValueError("Number of nodes cannot be smaller than the existing graph size.")

            adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
            adjacency_matrix[:existing_size, :existing_size] = existing_graph
            degrees = np.sum(adjacency_matrix, axis=0)

        # Attach the remaining nodes
        for new_node in range(existing_size, num_nodes):#type: ignore
            # Calculate the probability distribution based on node degrees
            probabilities = degrees[:new_node] / np.sum(degrees[:new_node])
            
            # Select nodes to attach to based on preferential attachment
            targets = np.random.choice(new_node, size=num_edges_to_attach, replace=False, p=probabilities)

            # Connect the new node to selected nodes
            adjacency_matrix[new_node, targets] = 1
            adjacency_matrix[targets, new_node] = 1

            # Update degrees of the new node and selected nodes
            degrees[new_node] += num_edges_to_attach
            degrees[targets] += 1

        return adjacency_matrix
    @staticmethod
    def generate_cycle_graph(num_nodes: int):
        if num_nodes == 0:
            raise ValueError("Need more than 0 nodes")
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        for i in range(num_nodes):
            adjacency_matrix[i, (i+1) % num_nodes] = 1
            adjacency_matrix[(i+1) % num_nodes, i] = 1
        
        return adjacency_matrix
    @staticmethod
    def generate_complete_graph(num_nodes: int):
        if num_nodes == 0:
            raise ValueError("Need more than 0 nodes")
        adjacency_matrix = np.ones((num_nodes, num_nodes), dtype=int) - np.eye(num_nodes, dtype=int)  # type: ignore
    @staticmethod
    def generate_star_graph( num_nodes: int):
        if num_nodes == 0:
            raise ValueError("Need more than 0 nodes")
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        # Connect all nodes to the central node (node 0)
        adjacency_matrix[1:, 0] = 1
        adjacency_matrix[0, 1:] = 1
        
        return adjacency_matrix


if __name__ == '__main__':
    time = perf_counter()
    print(graph_drawer.generate_random_graph(3000,0.5)) # type: ignore
    print(f'tool {perf_counter()-time}')
    time = perf_counter()
    print(graph_drawer.test_generate_random_graph(3000,0.5)) # type: ignore
    print(f'tool {perf_counter()-time}')
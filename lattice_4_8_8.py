import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def index_cells(shapes, pos, N, M):
    pass

def index_4_gon(vertices, idx, N, M, pos):
    # Squares will always have top and bottom neighbors
    faces = [
        {'adjacent_cell': idx+1, 'vertices': [vertices[0], vertices[2]]},
        {'adjacent_cell': idx-1, 'vertices': [vertices[1], vertices[3]]}
    ]
    # If the square's left neighbor exists on the lattice
    if idx-int((5.928571429*(N/4))-2.678571429) > 0:
        faces.append(
            {'adjacent_cell': idx-int((5.928571429*(N/4))-2.678571429),
             'vertices': [vertices[0], vertices[1]]}
        )
    # If the square's right neighbor exists on the lattice
    if int((5.928571429*(N/4))-2.678571429)+idx < N*M-N:
        faces.append(
            {'adjacent_cell': int((5.928571429*(N/4))-2.678571429)+idx,
             'vertices': [vertices[2], vertices[3]]}
        )
    # Create cell in format of pyvoro package
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[2]][0])/2,
            (pos[vertices[0]][1]+pos[vertices[1]][1])/2
        ]),
        'vertices': [pos[vertices[0]], pos[vertices[1]], pos[vertices[2]], pos[vertices[3]]],
        'volume': np.sqrt(3)/4,
        'adjacency': [
            [vertices[0], vertices[1]],
            [vertices[1], vertices[3]],
            [vertices[3], vertices[2]],
            [vertices[2], vertices[0]]
        ]
    }
    return cell

def index_8_gon(vertices, idx, N, M, pos):
    pass

def lattice_cells(n, m):
    G = nx.Graph()
    pos = {}
    polys = []
    shapes = {}
    M = m * 4
    N = int(4 * n)
    
    for col in range(0, M):
        pos[N*col] = np.array([col, 0]) # TODO
        if col > 0 and col % 4 == 2:
            G.add_edge(N*col, N*col-N)
        
        for row in range(0, N):
            idx = (N * col) + row
            if 1 < row % 4 < 3 and idx-1 in G.nodes:
                G.add_edge(idx, idx-1)
            
            pos[idx] = np.array([col, row])

            if col < M-1:
                if row % 4 == 0 and col % 4 == 2:
                    G.add_edge(idx, idx+N+1)
                if row % 4 == 1 and col % 4 == 0:
                    G.add_edge(idx, idx+N-1)
                if row % 4 == 2 and col % 4 == 0:
                    G.add_edge(idx, idx+N+1)
                if row % 4 == 3 and col % 4 == 2:
                    G.add_edge(idx, idx+N-1)
            
            if 0 < row % 4 < 3 and idx in G.nodes:
                if 0 < col % 4 < 3:
                    G.remove_node(idx)
                elif col % 4 == 3 and idx+N < N*M:
                    G.add_edge(idx, idx+N)
            
            if col % 4 == 2 and (row % 4 == 0 or row % 4 == 3):
                G.add_edge(idx, idx-N)
                if (idx + 1) % N > 0 :
                    G.add_edge(idx, idx+1)
                    
            if col % 4 == 1 and (row % 4 == 0 or row % 4 == 3):
                if (idx + 1) % N > 0:
                    G.add_edge(idx, idx+1)
            
            # if col % 4 == 1 and (row % 4 == 0 or row % 4 == 3):
            #     G.add_edge(idx, idx)
                
            
    # Show nodes and labels for debugging when necessary
    # nx.draw(G, pos=pos, with_labels=True)
    nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()

if __name__ == "__main__":
    lattice_cells(8, 8)
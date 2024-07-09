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
    M = m
    N = int(6 * n)
    
    for col in range(0, M):
        pos[N*col] = np.array([col, 0]) # TODO
        
        for row in range(1, N):
            idx = (N * col) + row
            G.add_edge(idx-1, idx)
            pos[idx] = np.array([col, row])
            
    # Show nodes and labels for debugging when necessary
    nx.draw(G, pos=pos, with_labels=True)
    # nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()

if __name__ == "__main__":
    print(lattice_cells(1, 5))
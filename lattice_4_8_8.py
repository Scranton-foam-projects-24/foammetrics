import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def index_cells(shapes, pos, N, M):
    cells = []
    for shape in shapes:
        if len(shapes[shape]) == 4:
            cells.append(index_4_gon(shapes[shape], shape, N, M, pos))
        else:
            cells.append(index_8_gon(shapes[shape], shape, N, M, pos))
    return cells

def index_4_gon(vertices, idx, N, M, pos):
    faces = []
    height = (2*int(N/4))-1
    if vertices[0] % N == 4:
        faces.append([
            {
                'adjacent_cell': idx+1,
                'vertices': [vertices[0], vertices[1]]
            },
            {
                'adjacent_cell': idx-1,
                'vertices': [vertices[2], vertices[3]]
            }
        ])
        if vertices[0] > N * 4:
            faces.append(
                {
                    'adjacent_cell': idx-1,
                    'vertices': [vertices[1], vertices[2]]
                }
            )
        if vertices[0] < (N*M)-(N*2):
            faces.append(
                {
                    'adjacent_cell': idx+height,
                    'vertices': [vertices[0], vertices[3]]
                }
            )
    elif vertices[0] % N == 2:
        faces.append([
            {
                'adjacent_cell': idx-height,
                'vertices': [vertices[1], vertices[2]]
            },
            {
                'adjacent_cell': idx+height,
                'vertices': [vertices[0], vertices[3]]
            }
        ])
        if vertices[0] % N == N-2:
            faces.append(
                {
                    'adjacent_cell': idx-1,
                    'vertices': [vertices[0], vertices[1]]
                }
            )
        elif vertices[0] % N == 2:
            faces.append(
                {
                    'adjacent_cell': idx+1, 
                    'vertices': [vertices[0], vertices[1]]
                }
            )
    else:
        faces.append([
            {
                'adjacent_cell': idx+1,
                'vertices': [vertices[0], vertices[1]]
            },
            {
                'adjacent_cell': idx-1,
                'vertices': [vertices[2], vertices[3]]
            },
        ])
        if idx-height-1 > 0:
            faces.append(
                {
                    'adjacent_cell': idx-height,
                    'vertices': [vertices[1], vertices[2]]
                }
            )
        if idx+height+1 < N*M:
            faces.append(
                {
                    'adjacent_cell': idx+height,
                    'vertices': [vertices[0], vertices[3]]
                }
            )

    # Create cell in format of pyvoro package
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[2]][0])/2,
            (pos[vertices[0]][1]+pos[vertices[1]][1])/2
        ]),
        'vertices': [
            pos[vertices[0]], 
            pos[vertices[1]], 
            pos[vertices[2]], 
            pos[vertices[3]]
        ],
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
    faces = []
    print(vertices[0])
    print(vertices[0]%M)
    height = (2*int(N/4))-1
    if vertices[0] % 4 == 0:
        faces.append([
            {
                'adjacent_cell': idx+height+1, 
                'vertices': [vertices[0], vertices[1]]
            },
            {
                'adjacent_cell': idx+1, 
                'vertices': [vertices[1], vertices[2]]
            },
            {
                'adjacent_cell': idx-height+1,
                'vertices': [vertices[2], vertices[3]]
            },
            {
                'adjacent_cell': idx-height,
                'vertices': [vertices[3], vertices[4]]
            },
            {
                'adjacent_cell': idx-height-1,
                'vertices': [vertices[4], vertices[5]]
            },
            {
                'adjacent_cell': idx-1,
                'vertices': [vertices[5], vertices[6]]
            },
            {
                'adjacent_cell': idx+height-1,
                'vertices': [vertices[6], vertices[7]]
            },
            {
                'adjacent_cell': idx+height,
                'vertices': [vertices[0], vertices[7]]
            },
        ])
    # TODO: account for other octagons which are delibarately made by vertex placement
    return {'faces': faces}

def lattice_cells(n, m):
    G = nx.Graph()
    pos = {}
    squares = []
    octagons = []
    shapes = {}
    M = m * 4
    N = n * 4
    
    for col in range(0, M):
        # Start every new column of points with an initial point
        pos[N*col] = np.array([col, 0])
        
        # If the point is part of the bottom edge of an octagon
        if col > 0 and col % 4 == 2:
            G.add_edge(N*col, N*col-N)
        
        # For every vertex going starting at the bottom of column and going up
        for row in range(0, N):
            idx = (N * col) + row
            
            # If the node added is the top of a vertical edge of an octagon
            if 1 < row % 4 < 3 and idx-1 in G.nodes:
                G.add_edge(idx, idx-1)
            
            pos[idx] = np.array([col, row])

            # Handle diagonal edges of octagons
            if col < M-1:
                # If vertex is right vertex of bottom flat edge ...
                if row % 4 == 0 and col % 4 == 2:
                    # ... make connection with vertex up 1 unit, right 1 unit
                    G.add_edge(idx, idx+N+1)
                # If vertex is bottom vertex of left vertical edge ...
                if row % 4 == 1 and col % 4 == 0:
                    # ... make connection with vertex down 1 unit, right 1 unit
                    G.add_edge(idx, idx+N-1)
                # If vertex is top vertex of left vertical edge ...
                if row % 4 == 2 and col % 4 == 0:
                    # ... make connection with vertex up 1 unit, right 1 unit
                    G.add_edge(idx, idx+N+1)
                # If vertex is right vertex of top flat edge ...
                if row % 4 == 3 and col % 4 == 2:
                    # ... make connection with vertex down 1 unit, right 1 unit
                    G.add_edge(idx, idx+N-1)
            
            # Add octagon (row, col)
            if col % 4 == 3 and col > 0 and idx in G.nodes and row % 4 == 2:
                octagons.append([
                    idx, 
                    idx-N+1, 
                    idx-(2*N)+1, 
                    idx-(3*N), 
                    idx-(3*N)-1, 
                    idx-(2*N)-2, 
                    idx-N-2, 
                    idx-1
                ])
            
            # Handle squares inside of and horizontally connecting octagons
            if 0 < row % 4 < 3 and idx in G.nodes:
                # Remove square inside octagon
                if 0 < col % 4 < 3:
                    G.remove_node(idx)
                # Connect octagon to right neighbor, also forming square
                elif col % 4 == 3 and idx+N < N*M:
                    G.add_edge(idx, idx+N)
                    if row % 4 == 2:
                        squares.append([
                            idx+N,
                            idx,
                            idx-1,
                            idx+N-1
                        ])
            
            # Handle squares vertically connecting octagons
            if col % 4 == 2 and (row % 4 == 0 or row % 4 == 3):
                # Make flat top and bottom edges of octagon
                G.add_edge(idx, idx-N)
                if (idx + 1) % N > 0 :
                    # Connect octagon to top neighbor, also forming square
                    G.add_edge(idx, idx+1)
                    if row % 4 == 0 and row > 0:
                        squares.append([
                            idx,
                            idx-N,
                            idx-N-1,
                            idx-1
                        ])
                        
            # Additional handling of squares vertically connecting octagons
            if col % 4 == 1 and (row % 4 == 0 or row % 4 == 3):
                # Make left edge of squares that vertically connect octagons
                if (idx + 1) % N > 0:
                    G.add_edge(idx, idx+1)
                    # Add octagon indirectly created by adjacent polygons
                    if row % 4 == 0 and row > 0 and col > 1:
                        octagons.append([
                            idx, 
                            idx-N+1, 
                            idx-(2*N)+1, 
                            idx-(3*N), 
                            idx-(3*N)-1, 
                            idx-(2*N)-2, 
                            idx-N-2, 
                            idx-1
                        ])
    
    # TODO: Loop will not trigger if function is called with (1, 1)
    for i in range((2 * len(octagons)) - 1):
        shapes[i] = octagons.pop(0) if i % 2 == 0 else squares.pop(0)
        
    # Show nodes and labels for debugging when necessary
    nx.draw(G, pos=pos, with_labels=True)
    # print(sorted(G.nodes))
    # nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()
    
    # print(shapes)
    return index_cells(shapes, pos, N, M)

if __name__ == "__main__":
    cells = lattice_cells(2, 3)
    for i, cell in enumerate(cells):
        if cell is not None:
            print(i, cell['faces'])
        pass
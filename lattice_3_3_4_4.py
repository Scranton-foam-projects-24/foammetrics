import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def index_cells(shapes, pos, N, M):
    cells = []
    for shape in shapes:
        if len(shapes[shape]) == 3:
            cells.append(index_3_gon(shapes[shape], shape, N, M, pos))
        else:
            cells.append(index_4_gon(shapes[shape], shape, N, M, pos))
    return cells

def index_3_gon(vertices, idx, N, M, pos):
    faces = []
    # If the polygon is a triangle on the bottom of the lattice
    if vertices[0] % N == 1 and vertices[1] % N == 1:
        faces.append(
            {'adjacent_cell': idx+1,
             'vertices': [vertices[1], vertices[2]]} 
        )
    # If the polygon is a triangle on the top of the lattice with even num rows
    elif (
         vertices[2] % N == N-2 and 
         vertices[1] % N == N-2 and 
         float.is_integer((N/4) % 2)   
    ):
        faces.append(
            {'adjacent_cell': idx-1,
             'vertices': [vertices[1], vertices[2]]} 
        )
    # If the polygon is a triangle on the top of the lattice with odd num rows
    elif (
        vertices[1] % N == N-2 and 
        vertices[0] % N == N-2 and 
        not float.is_integer((N/4) % 4)
    ):
        faces.append(
            {'adjacent_cell': idx-1,
             'vertices': [vertices[0], vertices[1]]} 
        )
    # If the flat edge of the triangle is formed by vertices[2] and vertices[1]
    elif vertices[2] - vertices[1] == N:
        # Tip of triangle is odd number and exists above flat edge
        if float.is_integer(pos[vertices[0]][0]):
            faces.append(
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[1], vertices[2]]} 
            )
            # If the triangle to its left (previous col) is on the lattice
            if idx-N-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-N-1,
                     'vertices': [vertices[0], vertices[1]]},    
                )
            # If the triangle to its right (proceeding poly) is on the lattice
            if idx+1 < N*M:
                faces.append(
                    {'adjacent_cell': idx+1,
                     'vertices': [vertices[0], vertices[2]]}
                )
        # Tip of triangle is even number and exists below flat edge
        else:
            faces.append(
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[0], vertices[1]]} 
            )
            # If the triangle to its left (previous poly) is on the lattice
            if idx-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[1], vertices[2]]},    
                )
            # If the triangle to its right (proceeding col) is on the lattice
            if idx+N < N*M-N:
                faces.append(
                    {'adjacent_cell': idx+N,
                     'vertices': [vertices[2], vertices[0]]}
                )
    # If the flat edge of the triangle is formed by vertices[1] and vertices[2]
    elif vertices[0] - vertices[1] == N:
        if vertices[1] % 2 == 0:
            # Unused???
            faces.append(
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[1], vertices[2]]} 
            )
            if idx-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[0], vertices[1]]},    
                )
            if idx-N > 0:
                faces.append(
                    {'adjacent_cell': idx+N,
                     'vertices': [vertices[1], vertices[2]]}
                )
        # Tip of triangle is even number and exists below flat edge
        else:
            faces.append(
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[1], vertices[0]]} 
            )
            # If the triangle to its right (previous poly) is on the lattice
            if idx-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[0], vertices[2]]},    
                )
            # If the triangle to its left (previous col) is on the lattice
            if idx-N-3 > 0:
                faces.append(
                    {'adjacent_cell': idx-N-3,
                     'vertices': [vertices[1], vertices[2]]}
                )
    # If the flat edge of the triangle is formed by vertices[0] and vertices[1]
    elif vertices[0] - vertices[2] == N:
        # Tip of triangle is odd number and exists above flat edge
        if vertices[1] % 2 == 0:
            faces.append(
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[1], vertices[2]]} 
            )
            # If the triangle to its left (proceeding poly) is on the lattice
            if idx+1 > 0:
                faces.append(
                    {'adjacent_cell': idx+1,
                     'vertices': [vertices[0], vertices[2]]},    
                )
            # If the triangle to its right (proceeding col) is on the lattice
            if 0 < idx+N+1 < N*M:
                faces.append(
                    {'adjacent_cell': idx+N+1,
                     'vertices': [vertices[1], vertices[0]]}
                )
        else:
            # Unused???
            faces.append(
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[1], vertices[0]]} 
            )
            if idx-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[0], vertices[2]]},    
                )
            if idx-N > 0:
                faces.append(
                    {'adjacent_cell': idx+N,
                     'vertices': [vertices[1], vertices[2]]}
                )
    # Create cell in format of pyvoro package
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[1]][0]+pos[vertices[2]][0])/3,
            (pos[vertices[0]][1]+pos[vertices[1]][1]+pos[vertices[2]][1])/3
        ]),
        'vertices': [pos[vertices[0]], pos[vertices[1]], pos[vertices[2]]],
        'volume': np.sqrt(3)/(4*M),
        'adjacency': [
            [vertices[0], vertices[1]],
            [vertices[0], vertices[2]],
            [vertices[1], vertices[2]]
        ]
    }
    return cell

def index_4_gon(vertices, idx, N, M, pos):
    # Squares will always have top and bottom neighbors
    faces = [
        {'adjacent_cell': idx+1, 'vertices': [vertices[1], vertices[0]]},
        {'adjacent_cell': idx-1, 'vertices': [vertices[2], vertices[3]]}
    ]
    # If the square's left neighbor exists on the lattice
    if idx-int((5.928571429*(N/4))-2.678571429) > 0:
        faces.append(
            {'adjacent_cell': idx-int((5.928571429*(N/4))-2.678571429),
             'vertices': [vertices[1], vertices[2]]}
        )
    # If the square's right neighbor exists on the lattice
    if int((5.928571429*(N/4))-2.678571429)+idx < N*M-N:
        faces.append(
            {'adjacent_cell': int((5.928571429*(N/4))-2.678571429)+idx,
             'vertices': [vertices[0], vertices[3]]}
        )
    # Create cell in format of pyvoro package
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[1]][0])/2,
            (pos[vertices[0]][1]+pos[vertices[2]][1])/2
        ]),
        'vertices': [
            pos[vertices[0]], 
            pos[vertices[1]], 
            pos[vertices[2]], 
            pos[vertices[3]]
        ],
        # TODO: Scale this down and correct it!!! *Fix scaling issue first
        'volume': ((pos[vertices[0]][0]+pos[vertices[1]][0])/M)**2,
        'adjacency': [
            [vertices[0], vertices[1]],
            [vertices[1], vertices[3]],
            [vertices[3], vertices[2]],
            [vertices[2], vertices[0]]
        ]
    }
    return cell

# TODO: Fix issue with squares that become rectangles, has something to do with
#       the scaling of the vertices, because the side lengths do not match
# Issue: polygons are scaled to fit within the unit canvas, and the scaling
#        results in the aspect ratio being changed to something != 1:1, when 
#        N != M
# TODO: lattice_cells(1.5, <3) produces unintended behavior
def lattice_cells(n, m):
    G = nx.Graph()
    pos = {}
    polys = []
    shapes = {}
    
    M = m
    N = int(4 * n)
    
    for col in range(0,M):
        # Initialize column with a vertex
        pos[N*col] = np.array([(col+0.5)/M,0])
        
        # Construct a column of vertices which are all connected according to
        # the 3^2, 4^2 Archimedian Lattice
        for row in range(1, N):
            # In this context, rows and columns are in reference to rows and
            # columns of tiles, not vertices unless otherwise specified
            
            # Plot vertex above prev vertex and connect it to previous vertex
            idx = (N * col) + row
            G.add_edge(idx-1, idx)
            
            # If the vertex is part of a tile on an even row
            if (row % 4 == 3 or row % 4 == 0) and 1 < row < N:
                # If plotting a polygon on the second or later column
                if idx > N and row < N-1:
                    # If the vertex is part of both a square and a downward
                    # facing triangle on an even row
                    if row % 4 == 3:
                        polys.append([idx, idx-1, idx-N])
                        polys.append([idx+1, idx-N+1, idx-N, idx])
                    # Otherwise, handle the vertex of the top right corner of
                    # each square on the even row
                    else:
                        polys.append([idx+1, idx-N, idx])
                    
                    # Connect current vertex to vertex on same row in prev col
                    G.add_edge(idx, idx-N)
                # Set position for vertices on even rows
                pos[idx] = np.array([(col+0.5)/M,row/N])
            else:
                # Set position for vertices on odd rows
                pos[idx] = np.array([col/M,row/N])
            
            # If the vertex is the bottom left corner of a square on an odd row
            if row % 4 == 1 and idx > N:
                if row != N - 1:
                    polys.append([idx, idx-N, idx-N-1])
                    polys.append([idx+1, idx-N+1, idx-N, idx])
                G.add_edge(idx, idx-N-1)
                # If the vertex is not in the first column
                if row < N-1:
                    G.add_edge(idx, idx-N)
            
            # If the vertex is the top left corner of a square on an odd row
            if row % 4 == 2 and idx > N:
                polys.append([idx-N+1, idx-N, idx])
                G.add_edge(idx, idx-N)
                G.add_edge(idx, idx-N+1)
    
    # Remove extraneous vertices
    if M*N % 4 == 0:
        G.remove_node(M*N-1)
    else:
        G.remove_node(N-1)
        
    G.remove_node(M*N-N)
    
    # Attach indices to each shape by incorporating it into a dictionary
    for i, poly in enumerate(polys):
        shapes[i] = poly
    
    # Show nodes and labels for debugging when necessary
    # nx.draw(G, pos=pos, with_labels=True)
    nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()
    
    # Convert dictionary of shapes to list of cells in same format as pyvoro
    return index_cells(shapes, pos, N, M)

if __name__ == "__main__":
    lattice_cells(3, 8)
    
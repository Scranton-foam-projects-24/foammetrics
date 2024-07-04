import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def index_cells(shapes, pos, N, M):
    cells = {}
    for shape in shapes:
        if len(shapes[shape]) == 3:
            cells[shape] = index_3_gon(shapes[shape], shape, N, M)
        else:
            cells[shape] = index_4_gon(shapes[shape], shape, N, M)
    return cells

def index_3_gon(vertices, idx, N, M):
    # TODO: Take a better look at the edge triangles
    #       - Find patterns between idxs and nodes
    #       - Write code to filter out edge triangles
    #           - One of the nodes is x%8 == 0 or x%8 == 1
    #       - Specify that the edge triangles have only 1 neighbor
    
    faces = []
    if vertices[2] % N == 1 and vertices[1] % N == 1:
        # print(f"{vertices[1]}-{vertices[2]} is flat side of edge triangle {idx}")
        faces.append(
            {'adjacent_cell': idx+1, 'vertices': [vertices[1], vertices[2]]} 
        )
    elif vertices[2] % N == N-2 and vertices[0] % N == N-2:
        # print(f"{vertices[0]}-{vertices[2]} is flat side of edge triangle {idx}")
        faces.append(
            {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[2]]} 
        )
    elif vertices[2] - vertices[0] == N:
        # print(f"{vertices[0]}-{vertices[2]} is flat")
        # print(f"{vertices[0]}-{vertices[1]} is slanted")
        # print(f"{vertices[1]}-{vertices[2]} is slanted")
        if vertices[2] % 2 == 0:
            faces.append(
                {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[2]]} 
            )
            if idx-N > 0:
                # print(f"Triangle {idx} shares an edge with {idx-N}")
                faces.append(
                    {'adjacent_cell': idx-N, 'vertices': [vertices[0], vertices[1]]},    
                )
            if idx+1 < N*M:
                # print(f"Triangle {idx} shares an edge with {idx+1}")
                faces.append(
                    {'adjacent_cell': idx+1, 'vertices': [vertices[1], vertices[2]]}
                )
        else:
            faces.append(
                {'adjacent_cell': idx+1, 'vertices': [vertices[0], vertices[2]]} 
            )
            if idx-1 > 0:
                # print(f"Triangle {idx} shares an edge with {idx-1}")
                faces.append(
                    {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[1]]},    
                )
            if idx+N < N*M-N:
                # print(f"Triangle {idx} shares an edge with {idx+N}")
                faces.append(
                    {'adjacent_cell': idx+N, 'vertices': [vertices[1], vertices[2]]}
                )
    elif vertices[2] - vertices[1] == N:
        # print(f"{vertices[1]}-{vertices[2]} is flat")
        # print(f"{vertices[0]}-{vertices[1]} is slanted")
        # print(f"{vertices[0]}-{vertices[2]} is slanted")
        if vertices[1] % 2 == 0:
            faces.append(
                {'adjacent_cell': idx-1, 'vertices': [vertices[1], vertices[2]]} 
            )
            if idx-1 > 0:
                # print(f"Triangle {idx} shares an edge with {idx-1}")
                faces.append(
                    {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[1]]},    
                )
            if idx-N > 0:
                # print(f"Triangle {idx} shares an edge with {idx-N}")
                faces.append(
                    {'adjacent_cell': idx+N, 'vertices': [vertices[1], vertices[2]]}
                )
        else:
            faces.append(
                {'adjacent_cell': idx+1, 'vertices': [vertices[1], vertices[2]]} 
            )
            if idx-1 > 0:
                # print(f"Triangle {idx} shares an edge with {idx-1}")
                faces.append(
                    {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[1]]},    
                )
            if idx-N-2 > 0:
                # print(f"Triangle {idx} shares an edge with {idx-N-2}")
                faces.append(
                    {'adjacent_cell': idx+N, 'vertices': [vertices[1], vertices[2]]}
                )
    elif vertices[1] - vertices[0] == N:
        # print(f"{vertices[0]}-{vertices[1]} is flat")
        # print(f"{vertices[0]}-{vertices[2]} is slanted")
        # print(f"{vertices[1]}-{vertices[2]} is slanted")
        if vertices[1] % 2 == 0:
            faces.append(
                {'adjacent_cell': idx-1, 'vertices': [vertices[1], vertices[0]]} 
            )
            if idx+1 > 0:
                # print(f"Triangle {idx} shares an edge with {idx+1}")
                faces.append(
                    {'adjacent_cell': idx+1, 'vertices': [vertices[0], vertices[2]]},    
                )
            if 0 < idx+N+2 < N*M:
                # print(f"Triangle {idx} shares an edge with {idx+N+2}")
                faces.append(
                    {'adjacent_cell': idx+N+2, 'vertices': [vertices[1], vertices[2]]}
                )
        else:
            faces.append(
                {'adjacent_cell': idx+1, 'vertices': [vertices[1], vertices[0]]} 
            )
            if idx-1 > 0:
                # print(f"Triangle {idx} shares an edge with {idx-1}")
                faces.append(
                    {'adjacent_cell': idx-1, 'vertices': [vertices[0], vertices[2]]},    
                )
            if idx-N > 0:
                # print(f"Triangle {idx} shares an edge with {idx-N}")
                faces.append(
                    {'adjacent_cell': idx+N, 'vertices': [vertices[1], vertices[2]]}
                )
    
    # TODO: Determine which two points are N away from each other
    #       Consider the edge between those two points as the flat side
    #       - Left and right neighbors will always be triangles
    #       - Determine if the triangle has a top neighbor or a bottom neighbor
    #           - Check if flat side vertices are even/odd
    #               - Even: has bottom neighbor
    #               - Odd: has top neighbor
    #       - Append faces accordingly
    # print(pos[vertices[0]])
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[1]][0]+pos[vertices[2]][0])/3,
            (pos[vertices[0]][1]+pos[vertices[1]][1]+pos[vertices[2]][1])/3
        ]),
        'vertices': vertices,
        'volume': np.sqrt(3)/4,
        'adjacency': [
            [vertices[0], vertices[1]],
            [vertices[0], vertices[2]],
            [vertices[1], vertices[2]]
        ]
    }
    # print(cell)
    return cell

def index_4_gon(vertices, idx, N, M):
    # print(f"{idx} is a square")
    # Squares always have top and bottom neighbors
    # Simple bounds check to determine existence of left/right neighbors
    # print(vertices)
    faces = [
        {'adjacent_cell': idx+1, 'vertices': [vertices[0], vertices[2]]},
        {'adjacent_cell': idx-1, 'vertices': [vertices[1], vertices[3]]}
    ]
    if idx-N > 0:
        faces.append(
            {'adjacent_cell': idx-N, 'vertices': [vertices[0], vertices[1]]}
        )
    # print(f"idx >>>>> {idx}")
    # print(f"N*M-N >>>>> {N*M-N}")
    # print(f"((5.9*(N/4))-1.5) >>>>> {((5.9*(N/4))-1.5)}")
    if int((5.9*(N/4))-1.5) < N*M-N:
        faces.append(
            {'adjacent_cell': int((5.928571429*(N/4))-1.678571429), 'vertices': [vertices[2], vertices[3]]}
        )
    # print(faces)
    # print(pos[vertices[0]])
    # print(pos[vertices[1]])
    # print(pos[vertices[2]])
    # print(pos[vertices[3]])
    cell = {
        'faces': faces,
        'original': np.array([
            (pos[vertices[0]][0]+pos[vertices[2]][0])/2,
            (pos[vertices[0]][1]+pos[vertices[1]][1])/2
        ]),
        'vertices': vertices,
        'volume': np.sqrt(3)/4,
        'adjacency': [
            [vertices[0], vertices[1]],
            [vertices[1], vertices[3]],
            [vertices[3], vertices[2]],
            [vertices[2], vertices[0]]
        ]
    }
    # print(cell)
    return cell

G = nx.Graph()
pos = {}
polys = []
shapes = {}
M = 5
N = int(4 * 3.5) # Change only the second number

for m in range(0,M):
    pos[N*m] = (m+0.5,0)
    for n in range(1, N):
        idx = (N * m) + n
        G.add_edge(idx-1, idx)
        
        if (n % 4 == 3 or n % 4 == 0) and 1 < n < N:
            if idx > N and n < N-1:    
                if n % 4 == 3:
                    polys.append(sorted([idx, idx-1, idx-N]))
                    polys.append(sorted([idx, idx-N, idx-N+1, idx+1]))
                else:
                    polys.append(sorted([idx, idx+1, idx-N]))
                    
                G.add_edge(idx, idx-N)
            pos[idx] = (m+0.5,n)
        else:
            pos[idx] = (m,n)
            
        if n % 4 == 1 and idx > N:
            polys.append(sorted([idx, idx-N, idx-N-1]))
            polys.append(sorted([idx, idx-N, idx-N+1, idx+1]))
            G.add_edge(idx, idx-N-1)
            if n < N-1:
                G.add_edge(idx, idx-N)
        
        if n % 4 == 2 and idx > N:
            polys.append(sorted([idx, idx-N, idx-N+1]))
            G.add_edge(idx, idx-N)
            G.add_edge(idx, idx-N+1)

if M*N % 4 == 0:
    G.remove_node(M*N-1)
else:
    G.remove_node(N-1)
G.remove_node(M*N-N)

for i, poly in enumerate(polys):
    shapes[i] = poly

# print(polys)

# TODO: Fix index_cells() for cases where N%4 != 0
#       - Top triangles are not treated as edge triangles in this case
cells = index_cells(shapes, pos, N, M)

for cell in cells:
    print(cell, cells[cell]['faces'])

# Show nodes and labels for debugging
# nx.draw(G, pos=pos, with_labels=True)
nx.draw(G, pos=pos, node_size=0)
plt.axis('scaled')
plt.show()

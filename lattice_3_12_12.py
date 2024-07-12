import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def index_cells(shapes, pos, N, M):
    cells = []
    for shape in shapes:
        if len(shapes[shape]) == 3:
            cells.append(index_3_gon(shapes[shape], shape, N, M, pos))
        else:
            cells.append(index_12_gon(shapes[shape], shape, N, M, pos))
    return cells

def index_3_gon(vertices, idx, N, M, pos):
    faces = []
    
def index_12_gon(vertices, idx, N, M, pos):
    faces = []
    
def lattice_cells(n, m):
    G = nx.Graph()
    pos = {}
    polys = []
    shapes = {}
    
    M = 7 * m
    N = 9 * n
    
    G.add_node(3)
    pos[3] = np.array([0, 3/N])
    G.add_node(5)
    pos[5] = np.array([0, 5/N])
    G.add_edge(3,5)
    col = 1
    
    # TODO: Create loop initializing first column with pairs of points
    # TODO: squash down each dodecagon by removing 1 from the top half of each one
    # TODO: Get the triangles on the top and bottom of the big polys to touch
    # TODO: Index the polys
    
    for i in range(0, N):
        if i % 9 == 3:
            G.add_node(i)
            pos[i] = np.array([0, i/N])
        elif i % 9 == 5:
            G.add_edge(i, i-2)
            pos[i] = np.array([0, i/N])
    
    while col < M: 
        pos[N*col] = np.array([(col-int(col/7))/M, 0])
        print(int(col / 7))
        for row in range(0,N):
            idx = (N * col) + row  
            
            # if idx-1 > -1 and idx % N != 0:
            #     G.add_edge(idx, idx-1)
            #     pos[idx] = np.array([(col-int(col/7))/M, row/N])
           
            if row % 9 == 5 and col % 7 == 6:
                G.add_edge(idx, idx-2)
                G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            elif ((row % 9 == 1 and col % 7 == 4) or
                  (row % 9 == 7 and col % 7 == 4)
            ):
                G.add_edge(idx, idx-(2*N))
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            elif row % 9 == 2 and col % 7 == 1:
                if idx < 2*N:
                    G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                if idx-(N*3) > 0:
                    G.add_edge(idx, idx-(N*3))
                    G.add_edge(idx, idx-(N*2)+1)
            elif ((row % 9 == 1 and col % 7 == 2) or
                  (row % 9 == 6 and col % 7 == 5)
            ):
                G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            elif row % 9 == 6 and col % 7 == 1:
                if idx < 2*N:
                    G.add_edge(idx, idx-N-1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                if idx-(N*3) > 0:
                    G.add_edge(idx, idx-(N*3))
                    G.add_edge(idx, idx-(N*2)-1)
            elif ((row % 9 == 7 and col % 7 == 2) or
                  (row % 9 == 2 and col % 7 == 5) or
                  (row % 9 == 3 and col % 7 == 6)
            ):
                G.add_edge(idx, idx-N-1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            elif row % 9 == 8 and col % 7 == 3:
                G.add_edge(idx, idx-N-1)
                G.add_edge(idx, idx+N-1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            elif row % 9 == 0 and col % 7 == 3:
                G.add_edge(idx, idx-N+1)
                G.add_edge(idx, idx+N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
        
        # TODO: Make the two side triangles become one larger triangle
        col += 1
    
    # Show nodes and labels for debugging when necessary
    # nx.draw(G, pos=pos, with_labels=True)
    nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()
    
if __name__ == "__main__":
    lattice_cells(2,2)

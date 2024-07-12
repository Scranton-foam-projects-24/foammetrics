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
    N = 8 * n
    
    col = 1
    
    # TODO: Index the polys
    
    for i in range(0, N):        
        if i % 8 == 3:
            G.add_node(i)
        elif i % 8 == 4:
            G.add_edge(i, i-1)
            
        # else:
        #     G.add_node(i)
        #     pos[i] = np.array([0, i/N])
            
        pos[i] = np.array([0, i/N])
    
    while col < M: 
        pos[N*col] = np.array([(col-int(col/7))/M, 0])
        for row in range(0,N):
            idx = (N * col) + row  
            
            # if idx-1 > -1 and idx % N != 0:
            #     G.add_edge(idx, idx-1)
            #     pos[idx] = np.array([(col-int(col/7))/M, row/N])
            
            # Draw right edge of dodecagon
            if row % 8 == 4 and col % 7 == 6:
                G.add_edge(idx, idx-1)
                G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                polys.append([
                    idx, 
                    idx-N+1, 
                    idx-(2*N)+2, 
                    idx-(4*N)+2, 
                    idx-(5*N)+1, 
                    idx-(6*N),
                    idx-(6*N)-1,
                    idx-(5*N)-2,
                    idx-(4*N)-3,
                    idx-(2*N)-3,
                    idx-N-2,
                    idx-1
                ])
            # Draw top and bottom edges of dodecagon
            elif ((row % 8 == 1 and col % 7 == 4) or
                  (row % 8 == 6 and col % 7 == 4)
            ):
                G.add_edge(idx, idx-(2*N))
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            # Draw edge under dodecagon's left edge
            elif row % 8 == 2 and col % 7 == 1:
                # If dodecagon lies on left edge, only connect to left edge
                if idx < 2*N:
                    G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                # Otherwise, draw edge to previous dodecagon, making triangle
                if idx-(N*3) > 0:
                    G.add_edge(idx, idx-(N*3))
                    G.add_edge(idx, idx-(N*2)+1)
                    polys.append([idx-(N*2)+1, idx-(N*3), idx])
            # Draw edge left of the bottom edge, and right of the top edge
            elif ((row % 8 == 1 and col % 7 == 2) or
                  (row % 8 == 5 and col % 7 == 5)
            ):
                G.add_edge(idx, idx-N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            # Draw edge on top of dodecagon's left edge
            elif row % 8 == 5 and col % 7 == 1:
                # If dodecagon lies on left edge, only connect to left edge
                if idx < 2*N:
                    G.add_edge(idx, idx-N-1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                # Otherwise, draw edge to previous dodecagon, making triangle
                if idx-(N*3) > 0:
                    G.add_edge(idx, idx-(N*3))
                    G.add_edge(idx, idx-(N*2)-1)
                    polys.append([idx-(N*2)-1, idx, idx-(N*3)])
            # Draw edge to left of the top edge, under the right edge, and
            # to the right of the bottom edge
            elif ((row % 8 == 6 and col % 7 == 2) or
                  (row % 8 == 2 and col % 7 == 5) or
                  (row % 8 == 3 and col % 7 == 6)
            ):
                G.add_edge(idx, idx-N-1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
            # Draw top triangle
            elif row % 8 == 7 and col % 7 == 3:
                G.add_edge(idx, idx-N-1)
                G.add_edge(idx, idx+N-1)
                # If dodecagon doesn't lie on top of lattice, connect to bottom
                # triangle of above dodecagon
                if row % N < N-1:
                    G.add_edge(idx, idx+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                polys.append([idx, idx-N-1, idx+N-1])
            # Draw bottom triangle
            elif row % 8 == 0 and col % 7 == 3:
                G.add_edge(idx, idx-N+1)
                G.add_edge(idx, idx+N+1)
                pos[idx] = np.array([(col-int(col/7))/M, row/N])
                polys.append([idx, idx+N+1, idx-N+1])
                
            # Add dodecagon indirectly created by adjacent polygons
            if row % 8 == 0 and col % 7 == 0 and row > 0 and col > 0:
                polys.append([
                    idx+(3*N), 
                    idx+(2*N)+1, 
                    idx+N+2, 
                    idx-(2*N)+2, 
                    idx-(3*N)+1, 
                    idx-(4*N),
                    idx-(4*N)-1,
                    idx-(3*N)-2,
                    idx-(2*N)-3,
                    idx+N-3,
                    idx+(2*N)-2,
                    idx+(3*N)-1
                ])
        
        col += 1
    
    print(polys)
    # Show nodes and labels for debugging when necessary
    # nx.draw(G, pos=pos, with_labels=True)
    nx.draw(G, pos=pos, node_size=0)
    plt.axis('scaled')
    plt.show()
    
if __name__ == "__main__":
    lattice_cells(2, 2)

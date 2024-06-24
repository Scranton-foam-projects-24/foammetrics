import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def odd_cell(G, m, n, pos, N):
    zero = (4*n)-4
    one = (4*n)-3
    two = (4*n)-2
    three = (4*n)-1
    four = 4*n
    five = (4*n)+1
    edge_list = [(zero,one), (one,two), (zero,two),
                 (two,three), (zero,five), (three,five),
                 (three,four), (five,four)]
    n *= 2
    scale = 2*N + 2
    pos[zero] = (1.0+m, (n-1)-(m*scale))
    pos[one] = (0.5+m, (n-2)-(m*scale))
    pos[two] = (0.0+m, (n-1)-(m*scale))
    pos[three] = (0.0+m, n-(m*scale))
    pos[four] = (0.5+m, (n+1)-(m*scale))
    pos[five] = (1.0+m, n-(m*scale))
    G.add_edges_from(edge_list)

def even_cell(G, m, n, pos, N):
    zero = (4*n)-4
    one = (4*n)-3
    two = (4*n)-2
    three = (4*n)-1
    four = 4*n
    five = (4*n)+1
    edge_list = [(zero,one), (one,two), (zero,two),
                 (two,three), (zero,five), (three,five),
                 (three,four), (five,four)]
    n *= 2
    scale = 2*N + 2
    pos[zero] = (0.5+m, (n-1)-(m*scale))
    pos[one] = (1.0+m, (n-2)-(m*scale))
    pos[two] = (1.5+m, (n-1)-(m*scale))
    pos[three] = (1.5+m, n-(m*scale))
    pos[four] = (1.0+m, (n+1)-(m*scale))
    pos[five] = (0.5+m, n-(m*scale))
    G.add_edges_from(edge_list)
    


G = nx.Graph()
pos = {}
M = 10
N = 7
for m in range(0,M):
    col = m * ( (N +1))
    for n in range(1, N+1):
        if n % 2 == 1:
            odd_cell(G, m, n+col, pos, N)
        else:
            even_cell(G, m, n+col, pos, N)

nx.draw(G, pos=pos, with_labels=False, node_size=0)
plt.axis('scaled')
plt.show()

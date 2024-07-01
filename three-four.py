import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

G = nx.Graph()
pos = {}
shapes = []
M = 5
N = 2 * 3
U = 1 # Unused basis factor
V = 1 # Unused basis factor

for m in range(0,M):
    pos[N*m] = (m+0.5,0)
    for n in range(1, N-1):
        idx = (N * m) + n
        G.add_edge(idx, idx-1)
        
        # print(f"idx % N = {idx%N}")
        if (idx % N == 1) and idx > N:
            G.add_edge(idx, idx-N-1)
        
        if idx-N > -1:
            G.add_edge(idx, idx-N)
            
        if (idx % N == 2 or idx % N == 5) and idx > N:
           G.add_edge(idx, idx-N+1)
        
        if (n % 3 == 0 or n % 3 == 1) and 1 < n < N-1:
            pos[idx] = (m+0.5,n)
        else:
            pos[idx] = (m,n)
    
    G.add_edge(N*(m+1)-1, N*(m+1)-2)
    # print(N*m-2)
    print(N*(m+1)-1)
    if N*m-2 > 0:
        G.add_edge(N*m-2, N*(m+1)-1)
    if pos[N*(m+1)-2][0] == m+0.5:
        pos[N*(m+1)-1] = (m,N-1)
    else:
        pos[N*(m+1)-1] = (m+0.5,N-1)
G.remove_node(N-1)
G.remove_node(N*(M-1))

# Show nodes and labels for debugging
nx.draw(G, pos=pos, with_labels=True)
# nx.draw(G, pos=pos, node_size=0)
plt.axis('scaled')
plt.show()

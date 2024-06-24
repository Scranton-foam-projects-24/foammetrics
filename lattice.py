import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def odd_cell(G, n, pos):
    zero = (4*n)-4
    one = (4*n)-3
    two = (4*n)-2
    three = (4*n)-1
    four = 4*n
    five = (4*n)+1
    edge_list = [(zero,one), (one,two), (zero,two),
                 (two,three), (zero,five), (three,five),
                 (three,four), (five,four)]
    pos[zero] = (1.0, (n-1)+((np.sqrt(3)*n)/2))
    pos[one] = (0.5, (n-1)+((n-1)*np.sqrt(3)))
    pos[two] = (0.0, (n-1)+((np.sqrt(3)*n)/2))
    pos[three] = (0.0, n+((np.sqrt(3)*n)/2))
    pos[four] = (0.5, n+(np.sqrt(3)))
    pos[five] = (1.0, n+((np.sqrt(3)*n)/2))
    G.add_edges_from(edge_list)

G = nx.Graph()
pos = {}
odd_cell(G, 1, pos)
odd_cell(G, 3, pos)
nx.draw(G, pos=pos, with_labels=True)
plt.show()

# def show_lattice(edge_list, pos):
#     G = nx.Graph()
#     G.add_edges_from(edge_list)
#     nx.draw(G, pos=pos, with_labels=True)
#     plt.show()
    
# def generate_tiles(edge_list, pos, n):
#     for i in range(13, (n*4)+5, 4):
#         edge_list.extend([(i-6, i-3),
#                           (i-6, i-2), (i-3, i-2),
#                           (i-5, i-1), (i-2, i-1),
#                           (i-5, i), (i-1, i)])
#         pos[i-3] = (pos[i-7][0]+1, pos[i-7][1])
#         pos[i-2] = (pos[i-6][0]+1, pos[i-6][1])
#         pos[i-1] = (pos[i-5][0]+1, pos[i-5][1])
#         pos[i] = (pos[i-4][0]+1, pos[i-4][1])

# def build_lattice(m, n):
#     graph_list = []
#     for i in range(m):
#         if m % 2 == 1:
#             graph_list.append(construct_row(n))
#         else:
#             graph_list.append(construct_row(n, offset=0.5))
    
#     G = nx.compose_all(graph_list)
#     pos = nx.get_node_attributes(G, 'pos')
#     for n, p in enumerate(pos):
#         print(n)
#         print(p)
#         G.nodes[n]['pos'] = p
#     # nx.draw(G, with_labels=True)
#     # plt.show()
#     return G

# def construct_row(n, offset=0.0):
#     edge_list = [(0,1), (0,4), (0,5),
#                  (1,3), (1,2),
#                  (2,3),
#                  (3,4),
#                  (4,5)]
#     pos = {
#             0: (0.0+offset, 1.0),
#             1: (0.0+offset, 0.0),
#             2: (0.5+offset, -1 * np.sqrt(3)/2),
#             3: (1.0+offset, 0.0),
#             4: (1.0+offset, 1.0),
#             5: (0.5+offset, 1 + np.sqrt(3)/2)
#             }
    
#     if n == 1:
#         show_lattice(edge_list, pos)
#         return
    
#     edge_list.extend([
#         (4,9), (4,8), (9,8),
#         (3,7), (3,6), (6,7),
#         (8,7)
#         ])
#     pos[6] = (1.5+offset,  -1 * np.sqrt(3)/2)
#     pos[7] = (2.0+offset, 0.0)
#     pos[8] = (2.0+offset, 1.0)
#     pos[9] = (1.5+offset, 1 + np.sqrt(3)/2)
    
    
#     if n == 2:
#         show_lattice(edge_list, pos)
#         return
        
#     generate_tiles(edge_list, pos, n)
    
#     G = nx.Graph()
#     G.add_edges_from(edge_list)
#     for n, p in enumerate(pos):
#         G.nodes[n]['pos'] = p
#     return G

# if __name__ == "__main__":
#     G = build_lattice(2, 3)
#     pos = nx.get_node_attributes(G, 'pos')
#     print(G)
#     print(pos)
#     nx.draw(G, pos=pos, with_labels=True)
#     plt.show()
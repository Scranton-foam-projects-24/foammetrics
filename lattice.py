import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# TODO: Remove duplicate vertices & edges

def even_cell(G, m, n, pos, shapes, N, M):
    n += 1
    zero = (4*n)-4+(2*m)
    one = (4*n)-3+(2*m)
    two = (4*n)-2+(2*m)
    three = (4*n)-1+(2*m)
    four = 4*n+(2*m)
    five = (4*n)+1+(2*m)
    edge_list = [(zero,one), (one,two), (zero,two),
                 (two,three), (zero,five), (three,five),
                 (three,four), (five,four)]
    xscale = m
    yscale = -1 * (N*2)*m
    pos[zero] = (1.0+xscale, ((2*n)-1)+(yscale))
    pos[one] = (0.5+xscale, ((2*n)-2)+(yscale))
    pos[two] = (0.0+xscale, ((2*n)-1)+(yscale))
    pos[three] = (0.0+xscale, (2*n)+(yscale))
    pos[four] = (0.5+xscale, ((2*n)+1)+(yscale))
    pos[five] = (1.0+xscale, (2*n)+(yscale))
    G.add_edges_from(edge_list)
    
    add_shapes(pos, shapes, n-1, N, M)

def odd_cell(G, m, n, pos, shapes, N, M):
    n += 1
    zero = (4*n)-4+(2*m)
    one = (4*n)-3+(2*m)
    two = (4*n)-2+(2*m)
    three = (4*n)-1+(2*m)
    four = 4*n+(2*m)
    five = (4*n)+1+(2*m)
    edge_list = [(zero,one), (one,two), (zero,two),
                 (two,three), (zero,five), (three,five),
                 (three,four), (five,four)]
    xscale = m
    yscale = -1 * (N*2)*m
    pos[zero] = (0.5+xscale, ((2*n)-1)+(yscale))
    pos[one] = (1.0+xscale, ((2*n)-2)+(yscale))
    pos[two] = (1.5+xscale, ((2*n)-1)+(yscale))
    pos[three] = (1.5+xscale, (2*n)+(yscale))
    pos[four] = (1.0+xscale, ((2*n)+1)+(yscale))
    pos[five] = (0.5+xscale, (2*n)+(yscale))
    G.add_edges_from(edge_list)
    
    add_shapes(pos, shapes, n-1, N, M)

def add_shapes(pos, shapes, n, N, M):
    # TODO: Only add valid adjacent cells. Negative cells should be removed.
    #       Also remove illegal adjacenies.
    n += 1
    zero = (4*n)-4+(2*m)
    one = (4*n)-3+(2*m)
    two = (4*n)-2+(2*m)
    three = (4*n)-1+(2*m)
    four = 4*n+(2*m)
    five = (4*n)+1+(2*m)
    
    # Bottom Triangle
    bottom = {'faces':
      [
        {'adjacent_cell': (n*3)-2, 'vertices': [zero, two]},
      ],
      'original': np.array([
          (pos[zero][0]+pos[one][0]+pos[two][0])/3,
          (pos[zero][1]+pos[one][1]+pos[two][1])/3
          ]),
      'vertices':
      [
        np.array([pos[one][0], pos[one][1]]),
        np.array([pos[zero][0], pos[zero][1]]),
        np.array([pos[two][0], pos[two][1]])
      ],
      'volume': np.sqrt(3)/4,
      'adjacency':[[one, zero], [zero, two], [two, one]]
      }
        
    # Square
    middle = {'faces':
      [
        {'adjacent_cell': (n*3)-1, 'vertices': [five, three]},
        {'adjacent_cell': (n*3)-3, 'vertices': [two, zero]},
      ],
      'original': np.array([(pos[zero][0]+pos[two][0])/2, (pos[zero][1]+pos[five][1])/2]),
      'vertices':
      [
        np.array([pos[zero][0], pos[zero][1]]),
        np.array([pos[five][0], pos[five][1]]),
        np.array([pos[three][0], pos[three][1]]),
        np.array([pos[two][0], pos[two][1]])
      ],
      'volume': 1,
      'adjacency':[[zero, five], [five, three], [three, two], [two, zero]]
      }
        
    # Top Triangle
    top = {'faces':
      [#                  (2*3)-2
        {'adjacent_cell': (n*3)-2, 'vertices': [three, five]},
      ],
      'original': np.array([
          (pos[three][0]+pos[four][0]+pos[five][0])/3,
          (pos[three][1]+pos[four][1]+pos[five][1])/3
          ]),
      'vertices':
      [
        np.array([pos[four][0], pos[four][1]]),
        np.array([pos[three][0], pos[three][1]]),
        np.array([pos[five][0], pos[five][1]])
      ],
      'volume': np.sqrt(3)/4,
      'adjacency':[[four, five], [five, three], [three, four]]
      }

    if (n-1) % N != 0: # Not bottom-most cell
        if ((n*3)-3) + ((N*3)-1) < N*3*M:
            bottom['faces'].append(
                {'adjacent_cell': ((n*3)-3) + ((N*3)-1), 'vertices': [one, zero]}
            )
        bottom['faces'].append(
            {'adjacent_cell': (n*3)-4, 'vertices': [two, one]}    
        )
    if (n-1) % N != N-1: # Not top-most cell
        if -1 < (n*3) + (N*3) < N*3*M:
            top['faces'].append(
                {'adjacent_cell': (n*3) + (N*3), 'vertices': [four, three]}    
            )
        if (n*3) < N*3*M:
            top['faces'].append(
                {'adjacent_cell': (n*3), 'vertices': [five, four]}
            )

    # if left square exists
    if (n*3)-2 - (N*3) >= 0:
        middle['faces'].append(
            {'adjacent_cell': (n*3)-2 - (N*3), 'vertices': [zero, five]}
        )
    
    # if right square exists
    if (n*3)-2 - (N*3) <= N*3*M:
        middle['faces'].append(
            {'adjacent_cell': (n*3)-2 - (N*3), 'vertices': [three, two]}
        )
    
    shapes.extend([bottom, middle, top])
    
G = nx.Graph()
S = nx.Graph()
pos = {}
shapes = []
M = 2
N = 2
U = 1 # Unused basis factor
V = 1 # Unused basis factor
for m in range(0,M):
    for n in range(0, N):
        idx = (N * m) + n
        if n % 2 == 0:
            even_cell(G, m, idx, pos, shapes, N, M)
        else:
            odd_cell(G, m, idx, pos, shapes, N, M)
# Show nodes and labels for debugging
nx.draw(G, pos=pos, with_labels=True)
# nx.draw(G, pos=pos, node_size=0)
print(shapes[5])
# print(shapes[1])
plt.axis('scaled')
plt.show()

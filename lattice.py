import networkx as nx
import matplotlib.pyplot as plt

def even_cell(G, m, n, pos, shapes, N):
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
    yscale = -1 * (2*N + 4) - 2*N*m
    pos[zero] = (1.0+xscale, ((2*n)-1)+(yscale))
    pos[one] = (0.5+xscale, ((2*n)-2)+(yscale))
    pos[two] = (0.0+xscale, ((2*n)-1)+(yscale))
    pos[three] = (0.0+xscale, (2*n)+(yscale))
    pos[four] = (0.5+xscale, ((2*n)+1)+(yscale))
    pos[five] = (1.0+xscale, (2*n)+(yscale))
    G.add_edges_from(edge_list)
    
    shapes[(n*3)-3] = [(one, zero), (zero, two), (two, one)]
    shapes[(n*3)-2] = [(zero, five), (five, three), (three, two), (two, zero)]
    shapes[(n*3)-1] = [(four, three), (three, five), (five, four)]

def odd_cell(G, m, n, pos, shapes, N):
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
    yscale = -1 * (2*N + 4) - 2*N*m
    pos[zero] = (0.5+xscale, ((2*n)-1)+(yscale))
    pos[one] = (1.0+xscale, ((2*n)-2)+(yscale))
    pos[two] = (1.5+xscale, ((2*n)-1)+(yscale))
    pos[three] = (1.5+xscale, (2*n)+(yscale))
    pos[four] = (1.0+xscale, ((2*n)+1)+(yscale))
    pos[five] = (0.5+xscale, (2*n)+(yscale))
    G.add_edges_from(edge_list)
    
    shapes[(n*3)-3] = [(one, two), (two, zero), (zero, one)]
    shapes[(n*3)-2] = [(zero, five), (five, three), (three, two), (two, zero)]
    shapes[(n*3)-1] = [(four, five), (five, three), (three, four)]
    
G = nx.Graph()
S = nx.Graph()
pos = {}
shapes = {}
M = 20
N = 20
for m in range(0,M):
    for n in range(0, N):
        idx = (N * m) + n
        print("idx:", idx)
        if n % 2 == 0:
            even_cell(G, m, idx, pos, shapes, N)
        else:
            odd_cell(G, m, idx, pos, shapes, N)
for shape in shapes:
    print(f"{shape}: {shapes[shape]}")
# nx.draw(G, pos=pos, with_labels=True, node_size=300)
nx.draw(G, pos=pos, with_labels=False, node_size=0)
plt.axis('scaled')
plt.show()

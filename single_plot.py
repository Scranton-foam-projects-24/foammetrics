# import pyvoro
import numpy as np
import matplotlib.pyplot as plt
import lattice_3_3_4_4 as lat

def swap_last(polygon):
    temp = polygon.pop() # take off old last
    new_last = polygon.pop() # take off second to last
    polygon.append(temp) # append old last
    polygon.append(new_last) # append new last

pts = 10
N = 3
M = 8

cells = lat.lattice_cells(N, M)

points = []
for i, cell in enumerate(cells):    
    polygon = cell['vertices']
    if len(polygon) == 4:
        swap_last(polygon)
    points.append(cell['original'].tolist())
    plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)

points = np.array(points)
plt.plot(points[:,0], points[:,1], 'ko')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

plt.show()
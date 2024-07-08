# import pyvoro
import numpy as np
import matplotlib.pyplot as plt
import three_four

def swap_last(polygon):
    temp = polygon.pop() # take off old last
    new_last = polygon.pop() # take off second to last
    polygon.append(temp) # append old last
    polygon.append(new_last) # append new last

pts = 10
N = 3
M = 8
# points = np.random.rand(pts, 2)
# colors = np.random.rand(pts, 3) 
# color_map = {tuple(coords):color for coords, color in zip(points, colors)}
# cells = pyvoro.compute_2d_voronoi(
#     points, # point positions, 2D vectors this time.
#     [[0.0, 1.0], [0.0, 1.0]], # box size
#     2.0, # block size
#     periodic = [True, True]
# )

# Work on scaling the box size to 1x1 grid
cells = three_four.lattice_cells(N, M)

points = []
for i, cell in enumerate(cells):    
    polygon = cell['vertices']
    if len(polygon) == 4:
        swap_last(polygon)
    points.append(cell['original'].tolist())
    plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)

# The plots are weird because the squares go:
    # bottom left, top left, bottom right, top right
    # instead of (counter)clockwise motion
points = np.array(points)
plt.plot(points[:,0], points[:,1], 'ko')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

plt.show()
# import pyvoro
import numpy as np
import matplotlib.pyplot as plt
# from archimedean.lattice_3_3_4_4 import Lattice
# from archimedean.lattice_4_8_8 import Lattice
from archimedean.lattice_3_12_12 import Lattice

N = 4
M = 4

# TODO: Cannot handle case where both N and M are 1, program refuses to load
cells = Lattice().lattice_cells(N, M)

# print(cells)
points = []
for i, cell in enumerate(cells):
    # print(cell)
    polygon = cell['vertices']
    # print(i, cell['vertices'])
    points.append(cell['original'].tolist())
    plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)

points = np.array(points)
plt.plot(points[:,0], points[:,1], 'ko')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

plt.show()
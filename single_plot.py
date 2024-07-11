# import pyvoro
import numpy as np
import matplotlib.pyplot as plt
import lattice_3_3_4_4 as lat3344
import lattice_4_8_8 as lat488

N = 3
M = 8

cells = lat3344.lattice_cells(N, M)
# cells = lat488.lattice_cells(N, M)

points = []
for i, cell in enumerate(cells):    
    polygon = cell['vertices']
    # print(i, cell['vertices'])
    points.append(cell['original'].tolist())
    plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)

points = np.array(points)
plt.plot(points[:,0], points[:,1], 'ko')
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)

plt.show()
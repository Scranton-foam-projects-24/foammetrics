import numpy as np
import pyvoro
import turning_function
import matplotlib.pyplot as plt

from polygon import Polygon

class Voronoi_Utils:
    def __init__(self):
        self.p = Polygon()
    
    def turn_dists(self, cells):
        turn_distances = []
        for i, cell in enumerate(cells):    
            polygon = cell['vertices']
            dist, _, _, _ = turning_function.distance(
                polygon, 
                self.p.regpoly(len(polygon)), 
                brute_force_updates=False
            )
            turn_distances.append(dist)
        return turn_distances
    
    def plot_diagram(self, points):        
        plt.plot(points[:,0], points[:,1], 'ko')
        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.1, 1.1)

        plt.show()
    
    def plot_turn_dists(self, x_vals, y_vals, N, yerr, start=0):
        plt.scatter(x_vals, y_vals)
        plt.xlabel("Number of cells")
        plt.ylabel("Mean average turning distance")
        plt.title("Average turning distance on Voronoi diagrams")
        plt.errorbar(x_vals, y_vals, yerr=yerr, fmt='o')
        plt.xticks(np.arange(start, N+1, step=1000))
        plt.show()
        
def avg_turn_dists(dots_num, step=50, rounds=30, init_num=50):
    init_num = dots_num-50
    v = Voronoi_Utils()
    x_vals = []
    means = []
    deviations = []
    N = dots_num
    step = step
    rounds = range(1, rounds+1)
    np.random.seed([1938430])
    for n in range(init_num, N+1, step):
        # print(n)
        dists = []
        for round in rounds:
            # print(f"dots_num = {n} --> round = {round}") 
            points = np.random.rand(n, 2)
            cells = pyvoro.compute_2d_voronoi(
                points, # point positions, 2D vectors this time.
                [[0.0, 1.0], [0.0, 1.0]], # box size
                2.0, # block size
                periodic = [True, True]
            )
            tds = v.turn_dists(cells)
            dists.append(np.mean(tds))
        deviations.append(np.std(dists) / np.sqrt(rounds[-1]))
        x_vals.extend([n])
        means.append(np.mean(dists))
        
    return (x_vals, means, N, deviations)
    # v.plot_turn_dists(x_vals, means, N, deviations)

if __name__ == "__main__":
    v = Voronoi_Utils()
    N = 20
    points = np.random.rand(N, 2)
    colors = np.random.rand(N, 3) 
    color_map = {tuple(coords):color for coords, color in zip(points, colors)}
    cells = pyvoro.compute_2d_voronoi(
        points, # point positions, 2D vectors this time.
        [[0.0, 1.0], [0.0, 1.0]], # box size
        2.0, # block size
        periodic = [True, True]
    )
    
    
    
    for i, cell in enumerate(cells):    
        polygon = cell['vertices']
        plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)
    
    v.plot_diagram(points)
    
    vertices = []
    fig = plt.figure()
    ax = fig.add_subplot()
    
    for i, cell in enumerate(cells[0:5]):    
        polygon = cell['vertices']
        vertices.extend(polygon)
        for i, edge in enumerate(np.array(polygon)):
            ax.annotate(i, edge, xytext=[edge[0]+0.01, edge[1]+0.01])
        plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)
        
    v.plot_diagram(np.array(vertices))


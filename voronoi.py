import numpy as np
import pyvoro
import turning_function
import matplotlib.pyplot as plt

from polygon import Polygon
# import winsound

class Voronoi_Utils:
    def __init__(self):
        self.p = Polygon()
    
    def turn_dists_n_gon(self, cells, n=-1, weight_by_volume=False):
        turn_distances = []
        comp_poly = self.p.regpoly(n) if n != -1 else None
        for i, cell in enumerate(cells): 
            polygon = cell['vertices']
            if n == -1:
                comp_poly = self.p.regpoly(len(polygon))
            dist, _, _, _ = turning_function.distance(
                polygon, 
                comp_poly, 
                brute_force_updates=False
            )
            if weight_by_volume:
                turn_distances.append(dist * cell['volume'])
            else:
                turn_distances.append(dist)
        return turn_distances
    
    def turn_dists_lattice_tile(self, cells, tile, weight_by_volume=False):
        turn_distances = []
        for i, cell in enumerate(cells): 
            polygon = cell['vertices']
            dist, _, _, _ = turning_function.distance(
                polygon, 
                tile, 
                brute_force_updates=False
            )
            if weight_by_volume:
                turn_distances.append(dist * cell['volume'])
            else:
                turn_distances.append(dist)
        return turn_distances
    
    def plot_diagram(self, points):        
        plt.plot(points[:,0], points[:,1], 'ko')
        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.1, 1.1)

        plt.show()
    
    def plot_turn_dists(self, x_vals, y_vals, N, yerr, start=0, log_scale=False, label_weighted=False, n_gon_sides=-1):
        data = np.array(list(zip(x_vals, y_vals)))
        x, y = np.transpose(data)
        colors = ['blue', 'orange']
        for value in np.unique(x):
            mask = (x == value)
            plt.scatter(x[mask], y[mask], color=colors)
        if label_weighted:
            plt.ylabel("Mean sum turning distance")
            plt.suptitle("Weighted average turning distance on Voronoi diagrams")
        else:
            plt.ylabel("Mean average turning distance")
            plt.suptitle("Average turning distance on Voronoi diagrams")
        plt.xlabel("Number of cells")
        if n_gon_sides == -1:
            plt.title("blue => k-gon, orange => n-gon")
        else:
            plt.title(f"blue => k-gon, orange => {n_gon_sides}-gon")
        plt.errorbar(x_vals, y_vals, yerr=yerr, fmt='None', ecolor=colors)
        with open("weighted_yerr.txt", "w+") as output:
            for i, val in enumerate(yerr):
                output.write(f"({x[i]}, {y[i]}) [{colors[i%2]}] " + str(val) + "\n")
        plt.xticks(np.arange(start, N+1, step=50))
        if log_scale:
            plt.yscale("log")
        plt.show()
        
    def plot_tile_turn_dists(self, x_vals, y_vals, N, yerr, start=0, log_scale=False, label_weighted=False):
        data = np.array(list(zip(x_vals, y_vals)))
        x, y = np.transpose(data)
        plt.scatter(x_vals, y_vals)
        if label_weighted:
            plt.ylabel("Mean sum turning distance")
            plt.suptitle("Weighted average turning distance on Voronoi diagrams")
        else:
            plt.ylabel("Mean average turning distance")
            plt.suptitle("Average turning distance on Voronoi diagrams")
        plt.title("Cells compared to Archimedian Tile")
        plt.xlabel("Number of cells")
        plt.errorbar(x_vals, y_vals, yerr=yerr, fmt='None')
        with open("weighted_yerr.txt", "w+") as output:
            for i, val in enumerate(yerr):
                output.write(f"({x[i]}, {y[i]}) " + str(val) + "\n")
        plt.xticks(np.arange(start, N+1, step=50))
        if log_scale:
            plt.yscale("log")
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
        dists = []
        for round in rounds:
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
        x_vals.append(n)
        means.append(np.mean(dists))
        
    return (x_vals, means, N, deviations)
    
def display_vertices_n_cells(n):
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
    
    for i, cell in enumerate(cells[0:n]):    
        polygon = cell['vertices']
        vertices.extend(polygon)
        for i, edge in enumerate(np.array(polygon)):
            ax.annotate(i, edge, xytext=[edge[0]+0.01, edge[1]+0.01])
        plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)
        
    v.plot_diagram(np.array(vertices))
    
def wtd_vs_unwtd_avg_turn_dists(dots_num, step=50, rounds=30, init_num=50, weighted=False):
    init_num = dots_num-50
    v = Voronoi_Utils()
    x_vals = []
    means = []
    deviations = []
    N = dots_num
    step = step
    rounds = range(1, rounds+1)
    np.random.seed([1938430])
    n_gon_sides = 1023
    for n in range(init_num, N+1, step):
        dists = [] # Contains r turning distances 
        dists_kgon = [] # Contains r turning distances
        for round in rounds:
            points = np.random.rand(n, 2)
            cells = pyvoro.compute_2d_voronoi(
                points, # point positions, 2D vectors this time.
                [[0.0, 1.0], [0.0, 1.0]], # box size
                2.0, # block size
                periodic = [True, True]
            )
            tds = v.turn_dists_n_gon(cells, weight_by_volume=weighted)
            kgon_tds = v.turn_dists_n_gon(cells, n=n_gon_sides, weight_by_volume=weighted)
            if weighted:
                dists.append(np.sum(tds))
                dists_kgon.append(np.sum(kgon_tds))
            else:
                dists.append(np.mean(tds))
                dists_kgon.append(np.mean(kgon_tds))
        deviations.append(np.std(dists) / np.sqrt(rounds[-1]))
        deviations.append(np.std(dists_kgon) / np.sqrt(rounds[-1]))
        x_vals.append(n)
        x_vals.append(n)
        means.append(np.mean(dists))
        means.append(np.mean(dists_kgon))
        
    v.plot_turn_dists(
        x_vals, 
        means, 
        N, 
        deviations, 
        label_weighted=weighted,
        n_gon_sides=n_gon_sides
    )

if __name__ == "__main__":
    tile = [(1.0, 1.0),
            (0.5, 0.0),
            (0.0, 1.0),
            (0.0, 2.0),
            (0.5, 3.0),
            (1.0, 2.0)]
    init_num = 50
    v = Voronoi_Utils()
    x_vals = []
    means = []
    deviations = []
    N = 100
    step = 50
    rounds = range(1, 31)
    np.random.seed([1938430])
    weighted=True
    for n in range(init_num, N+1, step):
        dists = [] # Contains r turning distances 
        # dists_kgon = [] # Contains r turning distances
        for round in rounds:
            points = np.random.rand(n, 2)
            cells = pyvoro.compute_2d_voronoi(
                points, # point positions, 2D vectors this time.
                [[0.0, 1.0], [0.0, 1.0]], # box size
                2.0, # block size
                periodic = [True, True]
            )
            tds = v.turn_dists_lattice_tile(cells, tile, weight_by_volume=weighted)
            # kgon_tds = v.turn_dists_n_gon(cells, n=n_gon_sides, weight_by_volume=weighted)
            if weighted:
                dists.append(np.sum(tds))
                # dists_kgon.append(np.sum(kgon_tds))
            else:
                dists.append(np.mean(tds))
                # dists_kgon.append(np.mean(kgon_tds))
        deviations.append(np.std(dists) / np.sqrt(rounds[-1]))
        # deviations.append(np.std(dists_kgon) / np.sqrt(rounds[-1]))
        x_vals.append(n)
        # x_vals.append(n)
        means.append(np.mean(dists))
        # means.append(np.mean(dists_kgon))
        
    v.plot_tile_turn_dists(
        x_vals, 
        means, 
        N, 
        deviations, 
        label_weighted=weighted
    )
    # winsound.MessageBeep()

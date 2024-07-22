import numpy as np
import turning_function
import matplotlib.pyplot as plt

from polygon import Polygon as poly
    
def turn_dists_n_gon(cells, n=-1, weight_by_volume=False):
    turn_distances = []
    comp_poly = poly.regpoly(n) if n != -1 else None
    for i, cell in enumerate(cells): 
        polygon = cell['vertices']
        if n == -1:
            comp_poly = poly.regpoly(len(polygon))
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

def turn_dists_lattice_tile(cells, tile, weight_by_volume=False):
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

def plot_diagram(points):        
    plt.plot(points[:,0], points[:,1], 'ko')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)

    plt.show()

def plot_turn_dists(x_vals, y_vals, N, yerr, start=0, log_scale=False, label_weighted=False, n_gon_sides=-1):
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
    
def plot_tile_turn_dists(x_vals, y_vals, N, yerr, start=0, log_scale=False, label_weighted=False):
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
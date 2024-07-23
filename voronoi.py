import numpy as np
import pyvoro
import matplotlib.pyplot as plt

import voronoi_utils as vu
        
def avg_turn_dists(dots_num, step=50, rounds=30, init_num=50):
    init_num = dots_num-50
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
            tds = vu.turn_dists(cells)
            dists.append(np.mean(tds))
        deviations.append(np.std(dists) / np.sqrt(rounds[-1]))
        x_vals.append(n)
        means.append(np.mean(dists))
        
    return (x_vals, means, N, deviations)
    
def display_vertices_n_cells(n):
    N = 20
    points = np.random.rand(N, 2)
    cells = pyvoro.compute_2d_voronoi(
        points, # point positions, 2D vectors this time.
        [[0.0, 1.0], [0.0, 1.0]], # box size
        2.0, # block size
        periodic = [True, True]
    )
    
    for i, cell in enumerate(cells):    
        polygon = cell['vertices']
        plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)
    
    vu.plot_diagram(points)
    
    vertices = []
    fig = plt.figure()
    ax = fig.add_subplot()
    
    for i, cell in enumerate(cells[0:n]):    
        polygon = cell['vertices']
        vertices.extend(polygon)
        for i, edge in enumerate(np.array(polygon)):
            ax.annotate(i, edge, xytext=[edge[0]+0.01, edge[1]+0.01])
        plt.fill(*zip(*polygon),  color = 'black', alpha=0.1)
        
    vu.plot_diagram(np.array(vertices))
    
def wtd_vs_unwtd_avg_turn_dists(dots_num, step=50, rounds=30, init_num=50, weighted=False):
    init_num = dots_num-50
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
            tds = vu.turn_dists_n_gon(cells, weight_by_volume=weighted)
            kgon_tds = vu.turn_dists_n_gon(cells, n=n_gon_sides, weight_by_volume=weighted)
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
        
    vu.plot_turn_dists(
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
    x_vals = []
    means = []
    deviations = []
    N = 100
    step = 50
    rounds = range(1, 31)
    np.random.seed([1938430])
    weighted=False
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
            tds = vu.turn_dists_lattice_tile(cells, tile, weight_by_volume=weighted)
            # kgon_tds = vu.turn_dists_n_gon(cells, n=n_gon_sides, weight_by_volume=weighted)
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
        
    vu.plot_tile_turn_dists(
        x_vals, 
        means, 
        N, 
        deviations, 
        label_weighted=weighted
    )

from multiprocessing import Pool
from voronoi import avg_turn_dists
from voronoi import Voronoi_Utils

if __name__ == '__main__':
    v = Voronoi_Utils()
    results = []
    with Pool(12) as p:
        # v.plot_turn_dists(x_vals, y_vals, N, yerr)
        results = p.map(avg_turn_dists, range(7000, 8001, 100))
    
    accum_x_vals = []
    accum_y_vals = []
    accum_N = []
    accum_yerr = []
    #  x_vals, y_vals, N, yerr
    for x_vals, y_vals, N, yerr in results:
        # v.plot_turn_dists(x_vals, y_vals, N, yerr)
        accum_x_vals.extend(x_vals)
        accum_y_vals.extend(y_vals)
        accum_N.append(N)
        accum_yerr.extend(yerr)
    
    # print("x", accum_x_vals)
    # print("y", accum_y_vals)
    # print("N", accum_N)
    # print("e", accum_yerr)
    
    v.plot_turn_dists(accum_x_vals, accum_y_vals, accum_N[-1], accum_yerr, start=6000)
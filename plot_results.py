import matplotlib.pyplot as plt
import numpy as np
import csv
import sympy as sp

x_vals = []
y_vals = []
yerr = []
N = 8000

with open("results.txt") as input:
    reader = csv.reader(input)
    for x, y, e in reader:
        x_vals.append(float(x))
        y_vals.append(float(y))
        yerr.append(float(e))

plt.scatter(x_vals, y_vals, color="blue", zorder=1, label="Average")
plt.plot(
    x_vals, 
    np.poly1d(np.polyfit(x_vals, y_vals, 1))(x_vals), 
    color="red", 
    zorder=3, 
    label=np.poly1d(np.polyfit(x_vals, y_vals, 1))
)
plt.xlabel("Number of cells")
plt.legend()
plt.ylabel("Mean average turning distance")
plt.title("Average turning distance on Voronoi diagrams")
plt.errorbar(x_vals, y_vals, yerr=yerr, fmt='o')
plt.xticks(np.arange(0, N+1, step=1000))
plt.show()
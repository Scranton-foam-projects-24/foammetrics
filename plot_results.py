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

less_x_vals = []
less_y_vals = []
less_yerr = []
for i in range(4, len(x_vals), 5):
    print(i)
    less_x_vals.append(x_vals[i])
    less_y_vals.append(y_vals[i])
    less_yerr.append(yerr[i])
    
print(less_x_vals)

plt.scatter(less_x_vals, less_y_vals, color="black")
plt.plot(
    less_x_vals, 
    less_y_vals,
    color="blue",
    linestyle='dashed'
)
plt.xlabel("Number of cells")
plt.ylabel("Mean average turning distance")
plt.title("Average turning distance on Voronoi diagrams")
plt.errorbar(less_x_vals, less_y_vals, yerr=less_yerr, fmt='o')
plt.xticks(np.arange(0, N+1, step=1000))
plt.show()
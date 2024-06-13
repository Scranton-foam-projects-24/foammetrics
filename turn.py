import turning_function
import statistics as stat
from polygon import Polygon
import matplotlib.pyplot as plt

p = Polygon()
shape_a = p.regpoly(10)
shape_b = p.randpoly(10)

def turning_distance(shape_a, shape_b):
    distance, _, _, _ = turning_function.distance(shape_a, shape_b, brute_force_updates=False)
    return distance

def multi_turning(regpoly, normpoly, iterations=1):
    return [turning_distance(regpoly, normpoly) for _ in range(iterations)]

if __name__ == "__main__":
    p = Polygon()
    sides = []
    turn_dist = []
    prevpoly = p.regpoly(2)
    for i in range(3, 1000):
        print(i)
        sides.append(i)
        newpoly = p.regpoly(i)
        turn_dist.append(stat.fmean(multi_turning(prevpoly, newpoly, iterations=10)))
        prevpoly = newpoly
        
    fig = plt.figure()
    ax = fig.add_subplot()
    # ax.set_yscale('log')
    
    plt.plot(sides, turn_dist)
        
    plt.title("N versus Turning Distance T(R_{n-1}, R_{n})")
    plt.xlabel("Number of Sides")
    plt.ylabel("Turning Distance")
    
    plt.show()

import turning_function
import statistics as stat
import matplotlib.pyplot as plt

from polygon import Polygon

def multi_turning(regpoly, normpoly, iterations=1):
    return [turning_function.distance(regpoly, normpoly, brute_force_updates=False)[0] for _ in range(iterations)]

if __name__ == "__main__":
    p = Polygon()
    sides = []
    turn_dist = []
    prevpoly = p.regpoly(2)
    for i in range(3, 100):
        print(i)
        sides.append(i)
        newpoly = p.regpoly(i)
        turn_dist.append(stat.fmean(multi_turning(prevpoly, newpoly, iterations=10)))
        prevpoly = newpoly
        
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_yscale('log')
    
    plt.plot(sides, turn_dist)
        
    plt.title("N versus Turning Distance T(R_{n-1}, R_{n})")
    plt.xlabel("Number of Sides")
    plt.ylabel("Turning Distance")
    
    plt.show()

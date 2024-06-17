from threading import Thread
from voronoi import foo, avg_turn_dists

threads = [None] * 10
results = [None] * 10

for i in range(len(threads)):
    threads[i] = Thread(target=avg_turn_dists, args=(results, i, 1000))
    threads[i].start()

# do some other stuff

for i in range(len(threads)):
    threads[i].join()

print (" ".join(results))  # what sound does a metasyntactic locomotive make?

# t1 = threading.Thread(voronoi.avg_turn_dists(2000))
# t2 = threading.Thread(voronoi.avg_turn_dists(4000, init_num=2001))
# t3 = threading.Thread(voronoi.avg_turn_dists(5000, init_num=4001))
# t4 = threading.Thread(voronoi.avg_turn_dists(6000, init_num=5001))
# t5 = threading.Thread(voronoi.avg_turn_dists(7000, init_num=6001))
# t6 = threading.Thread(voronoi.avg_turn_dists(8000, init_num=7001))
# t7 = threading.Thread(voronoi.avg_turn_dists(9000, init_num=8001))
# t8 = threading.Thread(voronoi.avg_turn_dists(10000, init_num=9001))

# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()
# t7.join()
# t8.join()
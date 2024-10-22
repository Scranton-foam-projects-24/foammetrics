# Foam Metrics

This repository consists of most of the work I did during from May to August 2024. My research primarily investigated the shape of cells in two-dimensional foams. To quantify the disorder of the foam, each cell is individually considered as an n-sided polygon and compared to the corresponding n-sided regular polygon.

The files with primary functionality in this repository are `turning_distance_formula.py` and `voronoi.py`.
---
# `turning_distance_formula.py`

A function which takes in two `int` arguments, `n` and `k`, where `n` is the total number of sides of a polygon, and `k` is an index variable. It returns a fraction of two integers representing the turning distance between `n` and `k`.

# `voronoi.py`

This file contains several methods used to compute the average turning distance of every cell in randomized voronoi diagrams. The different functions in this file compute the average turning distance with varying conditions, namely weighting each turning distance by the area of that cell.

# Measuring Disorder of Dynamic Polygonal Networks
Please navigate to [https://github.com/Scranton-foam-projects-24/t1moves/tree/turn_dist](https://github.com/Scranton-foam-projects-24/t1moves/tree/turn_dist) to see the code used to generate the graph displaying the network disorder vs. T1-moves.

To reproduce the graph found in the poster, run the main function of `t1_move_with_gif.py`, and the result will be a mathplotlib plot showing the relationship between network disorder and the number of T1 moves the diagram underwent.
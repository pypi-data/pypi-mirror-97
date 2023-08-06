neataco is an Ant Colony Optimization algorithm written in pure python. The intention is
to use this package with PyPy. The hot loops in the algorithm are perfect for PyPy's
just-in-time compilation and results in very fast performance.

To run create an instance of AntColonyOptimization and call run(). The output is a 
list with the optimized sequence of input items.

The input items can be a list of anything, because the distance function also
has to be provided. The distance function must be able to calculate the distance
between any items in the input list.

An example:
```python
from neataco import AntColonyOptimization
items = [10, 20, 15, 5, 100, 2, 30, 50]
distance_fn = lambda a, b: abs(b - a)

aco = AntColonyOptimization(
    items,
    distance_fn,
    ant_count=1024,
    alpha=1,
    beta=20,
    evaporation=0.2,
)
optimal_path = aco.run()
print(optimal_path)
```

This will print the shortest path between all of the numbers; in this case ordering them.

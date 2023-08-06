import logging
import random
from typing import List, Optional, Dict, TypeVar, Generic

from .distance import distance_matrix, DistanceFn

log = logging.getLogger(__name__)


T = TypeVar("T")


class AntColonyOptimization(Generic[T]):

    _alpha: int
    # Each element is a list of visited city indexes.
    _ants: List[List[int]]
    _ant_ratio: float = 0.8
    _beta: int
    _cities: List[T]
    _distances: Dict[int, Dict[int, float]]
    _evaporation: float
    _optimal_trail: List[int]
    _optimal_length: Optional[float]
    _trails: Dict[int, Dict[int, float]]
    _q: int

    def __init__(
        self,
        cities: List[T],
        distance_fn: DistanceFn,
        ant_count: int = None,
        alpha=1,
        beta=5,
        evaporation=0.5,
        q=500,
    ):
        self._cities = cities
        self.initialize(
            ant_count=ant_count, alpha=alpha, beta=beta, evaporation=evaporation, q=q
        )
        self._distances = distance_matrix(self._cities, distance_fn)

    def initialize(self, ant_count=None, alpha=1, beta=5, evaporation=0.2, q=500):
        """
        Initialize the ants, pheromone trails, and optimal trail.

        This can be called after run() to re-use the same set of distances and cities with
        new parameters.
        """
        if ant_count is None:
            ant_count = round(self._city_count * self._ant_ratio)
        self._alpha = alpha
        self._beta = beta
        self._evaporation = 1.0 - evaporation
        self._q = q
        self._ants = [
            [random.randint(0, self._city_count - 1)] for _ in range(ant_count)
        ]
        self._trails = {
            i: {j: 1.0 for j in range(self._city_count)}
            for i in range(self._city_count)
        }

        self._optimal_trail = []
        self._optimal_length = None

    def run(self) -> List[T]:
        """Run algorithm and return best trail."""
        log.debug("Starting Ant Colony Optimization.")
        log_every = round(self._city_count / 10)
        for i in range(self._city_count - 1):
            if i % log_every == 0:
                log.debug("Completed: %s percent.", round(i / self._city_count * 100))
            self._iterate()
        return [self._cities[i] for i in self._optimal_trail]

    @property
    def _city_count(self):
        return len(self._cities)

    def _city_probabilities(self, ant_cities: List[int]) -> List[float]:
        """Calculate probabilities for each city as the next city to visit."""
        alpha = self._alpha
        beta = self._beta
        trails = self._trails
        current_city = ant_cities[-1]
        current_trail = trails[current_city]
        current_distances = self._distances[current_city]
        pheromone = 0.0
        unvisited = []

        for city in range(self._city_count):
            if city in ant_cities:
                continue
            pheromone += (current_trail[city] ** alpha) * (
                (1.0 / current_distances[city]) ** beta
            )
            unvisited.append(city)

        if pheromone == 0:
            probs: List[float] = [int(i in unvisited) for i in range(self._city_count)]
        else:
            probs: List[float] = [0 for _ in range(self._city_count)]

            for city in unvisited:
                numerator = (current_trail[city] ** alpha) * (
                    (1.0 / current_distances[city]) ** beta
                )
                probs[city] = numerator / pheromone

        return probs

    def _evaporate(self):
        """Remove some pheromones from trails."""
        evaporation = self._evaporation
        trails = self._trails
        for i in range(self._city_count):
            for j in range(self._city_count):
                trails[i][j] *= evaporation

    def _find_next_city(self, ant_cities: List[int]) -> int:
        """Return the next city index to visit."""

        if random.random() < 0.01:
            # Occasionally get a random city
            next_city = random.choice(
                list(filter(lambda el: el not in ant_cities, range(self._city_count)))
            )
        else:
            # Choose the next city based on probabilities
            probs = self._city_probabilities(ant_cities)
            next_city = random.choices([i for i in range(self._city_count)], probs)[0]
        return next_city

    def _iterate(self):
        self._move_ants()
        self._evaporate()
        self._scent_trails()

    def _move_ants(self):
        """Move every ant to a new city."""

        for ant_cities in self._ants:
            next_city = self._find_next_city(ant_cities)
            ant_cities.append(next_city)

            if len(ant_cities) == self._city_count:
                dist = self._trail_distance(ant_cities)
                if self._optimal_length is None or dist < self._optimal_length:
                    self._optimal_length = dist
                    self._optimal_trail = ant_cities[:]

    def _scent_trails(self):
        """Lay down pheromones according to current ant trails."""
        q = self._q
        for ant_cities in self._ants:
            contribution = q / self._trail_distance(ant_cities)
            prev_i = None
            for i in ant_cities:
                if prev_i is None:
                    prev_i = i
                    continue

                self._trails[prev_i][i] += contribution
                prev_i = i

    def _trail_distance(self, ant_cities: List[int]):
        """Return total distance travelled by this ant."""
        prev_city = None
        distance = 0
        distances = self._distances
        for city in ant_cities:
            if prev_city is None:
                prev_city = city
                continue
            distance += distances[prev_city][city]
            prev_city = city
        return distance

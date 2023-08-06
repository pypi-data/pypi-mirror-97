import logging
from typing import List, Dict, TypeVar, Callable

log = logging.getLogger(__name__)

T = TypeVar("T")
DistanceFn = Callable[[T, T], float]


def distance_matrix(
    items: List[T], distance_fn: DistanceFn, scale: float = 1
) -> Dict[T, Dict[T, float]]:
    """Return a dict of all combinations of items and their distance."""
    log.debug("Calculating all distances.")
    distances = {}
    for i, item in enumerate(items):
        for j, other_item in enumerate(items):
            if i == j:
                continue
            try:
                distance = distances[j][i]
            except KeyError:
                distance = distance_fn(item, other_item) * scale
            distances.setdefault(i, {})[j] = distance
    return distances

import random
from typing import TypeVar, Generic, List
from .distance import distance_matrix, DistanceFn

T = TypeVar("T")


class NearestNeighbour(Generic[T]):
    def __init__(self, neighbours: List[T], distance_fn: DistanceFn):
        self._neighbours = neighbours
        self._distances = distance_matrix(neighbours, distance_fn)

    def run(self):
        neighbours = self._neighbours
        distances = self._distances
        picked = []
        neigh = random.choice(range(len(neighbours)))

        picked.append(neigh)
        yield neighbours[neigh]

        neighbour_count = len(neighbours)
        while len(picked) < neighbour_count:
            shortest_dist = None
            shortest_bour = None
            for bour, dist in distances[neigh].items():
                if bour in picked:
                    continue
                if shortest_dist is None or dist < shortest_dist:
                    shortest_bour = bour
                    shortest_dist = dist

            picked.append(shortest_bour)
            yield neighbours[shortest_bour]
            neigh = bour

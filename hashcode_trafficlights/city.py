import parsing
import copy
import networkx as nx
from collections import deque
from typing import Iterator

class City:
    def __init__(self, streets: Iterator[dict]):
        self.plan = nx.MultiDiGraph()
        self.build_streets(streets)
        self.build_street_map()

    def build_streets(self, streets: Iterator[dict]):
        for street in streets:
            self.plan.add_node(street['begin'])
            self.plan.add_node(street['end'])
            self.plan.add_edge(
                street['begin'], street['end'],
                id=street['id'],
                name=street['name'],
                crossing_time=street['crossing_time'],
            )
    
    def build_street_map(self):
        """
        Builds a map linking the street name with the graph primary indexes.
        This should facilitate searching through the graph.
        """
        self.street_map = {}
        for source, dest, street_data in self.plan.edges(data=True):
            self.street_map[ street_data['name'] ] = (source, dest)

    def get_edge(self, edge):
        if isinstance(edge, tuple):
            return self.plan.edges[edge]
        elif isinstance(edge, str):
            edge_ix = self.street_map[edge]
            return self.plan.edges[edge_ix[0], edge_ix[1], 0]

    @property
    def intersections(self):
        return self.plan.nodes(data=True)

    @property
    def streets(self):
        return self.plan.edges(data=True)

    @property
    def num_streets(self):
        return len(self.plan.edges)
    
    @property
    def num_intersections(self):
        return len(self.plan)

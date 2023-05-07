from random import choice


class Graph():
    def __init__(self):
        self.map = {}
        self.size = 0

    def add(self, token):
        """
        add a lone vertex to this Graph
        """
        self.map[token] = []
        self.size += 1

    def link(self, u, v, weight=None):
        """
        created a directed edge (u,v) in this graph
        with optional edge weight
        If a weight is specified, a tuple (v, weight)
        will be added to the adjacency list of u

        if a directed edge is desired this method must 
        be called twice
        """
        if u not in self.map:
            self.add(u)
        if v not in self.map:
            self.add(v)

        if weight is None:
            self.map[u].append(v)
        else:
            self.map[u].append((v, weight))

    def remove(self, data, default=None):
        """
        remove a node and all of its outgoing edges in this graph
        returns a list of edges removed as a result of this call

        it is not required for 'data' to already exist in the graph
        default value will be returned in this case
        """

        return self.map.pop(data, default)

    def random_selection(self):
        """
        randomly generate tokens from this graph
        based on edges 

        if a state without edges is reached, the process repeats
        """

        keys = list(self.map)
        while True:
            start = choice(keys)
            yield from start
            while True:
                if not self.map[start]:
                    break
                start = choice(self.map[start])
                yield start[-1]

    def __contains__(self, key):
        """
        return true if key is a node in this Graph
        """
        return key in self.map

    def __len__(self):
        """
        number of nodes in this Graph
        """
        return len(map)

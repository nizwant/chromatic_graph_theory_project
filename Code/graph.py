class Graph:
    __slots__ = ["size", "data"]

    def __init__(self, data, stored_in_matrix=True) -> None:
        self.size = len(data)
        self.data = data

    def number_of_nodes(self):
        return self.size

    def nodes_iter(self):
        pass

    def all_neighbors(self):
        pass

    def common_neighbors(self):
        pass

    def non_neighbors(self):
        pass

    def nodes(self):
        pass

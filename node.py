class Node:
    def __init__(self, x, y, score=0, neighbors=None):
        self.x = x
        self.y = y
        self.score = score
        self.neighbors = neighbors or []

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def get_position(self):
        return self.x, self.y

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

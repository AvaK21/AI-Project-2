"""A game given by an explicit tree. Do not modify."""
import json
from collections import deque

from game import Game


class TreeGame(Game):
    def __init__(self, root, children, utilities, reverse=False):
        super().__init__()
        self.initial = root
        self.children = {k: list(v) for k, v in children.items()}
        self.utilities = dict(utilities)
        self.reverse = reverse
        self.depth = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for child in self.children.get(node, []):
                self.depth[child] = self.depth[node] + 1
                queue.append(child)

    @classmethod
    def from_json(cls, path, reverse=False):
        with open(path) as f:
            data = json.load(f)
        return cls(data["root"], data["children"], data["utilities"], reverse)

    def to_move(self, state):
        return "MAX" if self.depth[state] % 2 == 0 else "MIN"

    def actions(self, state):
        kids = self.children.get(state, [])
        return kids[::-1] if self.reverse else list(kids)

    def result(self, state, action):
        return action

    def _is_terminal(self, state):
        return state in self.utilities

    def _utility(self, state, player):
        value = self.utilities[state]
        return value if player == "MAX" else -value

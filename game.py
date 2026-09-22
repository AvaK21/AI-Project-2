"""Game interface from AIMA 4th ed., Section 5.1. Do not modify."""


class Game:
    def __init__(self):
        self.reset_counters()

    def reset_counters(self):
        self.nodes_visited = 0
        self.terminals_evaluated = 0

    def to_move(self, state):
        raise NotImplementedError

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_terminal(self, state):
        self.nodes_visited += 1
        return self._is_terminal(state)

    def utility(self, state, player):
        self.terminals_evaluated += 1
        return self._utility(state, player)

    def _is_terminal(self, state):
        raise NotImplementedError

    def _utility(self, state, player):
        raise NotImplementedError

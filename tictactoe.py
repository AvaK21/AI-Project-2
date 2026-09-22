"""Tic-tac-toe. Do not modify."""
from game import Game

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(board):
    for a, b, c in LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


class TicTacToe(Game):
    def __init__(self):
        super().__init__()
        self.initial = ((None,) * 9, "X")

    def to_move(self, state):
        return state[1]

    def actions(self, state):
        return [i for i, c in enumerate(state[0]) if c is None]

    def result(self, state, action):
        board, player = state
        board = board[:action] + (player,) + board[action + 1:]
        return board, "O" if player == "X" else "X"

    def _is_terminal(self, state):
        return winner(state[0]) is not None or None not in state[0]

    def _utility(self, state, player):
        w = winner(state[0])
        return 0 if w is None else (1 if w == player else -1)

    @staticmethod
    def from_string(text, to_move):
        return tuple(None if c == "." else c for c in text), to_move

    @staticmethod
    def display(state):
        cells = [c or str(i) for i, c in enumerate(state[0])]
        return "\n---+---+---\n".join(
            " " + " | ".join(cells[r:r + 3]) for r in (0, 3, 6))

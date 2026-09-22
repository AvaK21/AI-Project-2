import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
if os.environ.get("SEARCH_DIR"):
    sys.path.insert(0, os.path.abspath(os.environ["SEARCH_DIR"]))

import adversarial_search as search  # noqa: E402
from tictactoe import TicTacToe      # noqa: E402
from tree_game import TreeGame       # noqa: E402

HINT = " Check the Requirements section of the README."


def tree(name, reverse=False):
    return TreeGame.from_json(os.path.join(ROOT, "trees", name + ".json"), reverse)


def run(fn, game, state):
    game.reset_counters()
    move = fn(game, state)
    return move, game.nodes_visited, game.terminals_evaluated


class SearchTest(unittest.TestCase):
    longMessage = False

    def check(self, fn, game, state=None, move=None, nodes=None, terminals=None, where=""):
        got, n, t = run(fn, game, game.initial if state is None else state)
        where = f" on {where}" if where else ""
        if move is not None:
            ok = got in move if isinstance(move, set) else got == move
            want = " or ".join(map(str, sorted(move))) if isinstance(move, set) else repr(move)
            self.assertTrue(ok, f"{fn.__name__} returned {got!r}{where}; expected {want}.")
        if nodes is not None:
            self.assertEqual(n, nodes, f"{fn.__name__} visited {n} states{where}; "
                                       f"expected {nodes}." + HINT)
        if terminals is not None:
            self.assertEqual(t, terminals, f"{fn.__name__} evaluated {t} terminal states{where}; "
                                           f"expected {terminals}." + HINT)


class TestMinimaxOnTrees(SearchTest):

    def test_figure_5_2_move(self):
        self.check(search.minimax_search, tree("figure_5_2"), move="B", where="Figure 5.2")

    def test_figure_5_2_examines_every_terminal(self):
        self.check(search.minimax_search, tree("figure_5_2"), nodes=13, terminals=9,
                   where="Figure 5.2")

    def test_worksheet_move(self):
        self.check(search.minimax_search, tree("worksheet"), move="B", where="the worksheet tree")

    def test_worksheet_examines_every_terminal(self):
        self.check(search.minimax_search, tree("worksheet"), nodes=31, terminals=16,
                   where="the worksheet tree")

    def test_ordering_does_not_change_minimax(self):
        self.check(search.minimax_search, tree("worksheet", reverse=True), move="B",
                   terminals=16, where="the worksheet tree, right to left")


class TestAlphaBetaOnTrees(SearchTest):

    def test_figure_5_2_move(self):
        self.check(search.alpha_beta_search, tree("figure_5_2"), move="B", where="Figure 5.2")

    def test_figure_5_2_prunes(self):
        self.check(search.alpha_beta_search, tree("figure_5_2"), nodes=11, terminals=7,
                   where="Figure 5.2")

    def test_worksheet_move(self):
        self.check(search.alpha_beta_search, tree("worksheet"), move="B",
                   where="the worksheet tree")

    def test_worksheet_prunes(self):
        self.check(search.alpha_beta_search, tree("worksheet"), nodes=24, terminals=10,
                   where="the worksheet tree")

    def test_worksheet_right_to_left(self):
        self.check(search.alpha_beta_search, tree("worksheet", reverse=True), move="B",
                   terminals=14, where="the worksheet tree, right to left")

    def test_figure_5_2_right_to_left_prunes_nothing(self):
        self.check(search.alpha_beta_search, tree("figure_5_2", reverse=True), terminals=9,
                   where="Figure 5.2, right to left")

    def test_same_move_as_minimax(self):
        for name in ["figure_5_2", "worksheet"]:
            for rev in [False, True]:
                g = tree(name, rev)
                where = f"{name}{', right to left' if rev else ''}"
                m1 = run(search.minimax_search, g, g.initial)[0]
                m2 = run(search.alpha_beta_search, g, g.initial)[0]
                self.assertEqual(m1, m2, f"on {where}, alpha_beta_search returned {m2!r} "
                                         f"but minimax_search returned {m1!r}.")


POSITIONS = {
    "take the win":       ("XX.OO....", "X", {2}),
    "block the diagonal": ("X.O.O....", "X", {6}),
    "win as O":           ("XX.OO.X..", "O", {5}),
    "answer the fork":    ("X...O...X", "O", {1, 3, 5, 7}),
}


class TestTicTacToe(SearchTest):

    def check_positions(self, fn):
        for name, (board, to_move, best) in POSITIONS.items():
            self.check(fn, TicTacToe(), TicTacToe.from_string(board, to_move), move=best,
                       where=f"position '{name}' ({board}, {to_move} to move)")

    def test_minimax_positions(self):
        self.check_positions(search.minimax_search)

    def test_alpha_beta_positions(self):
        self.check_positions(search.alpha_beta_search)

    def test_minimax_full_game(self):
        self.check(search.minimax_search, TicTacToe(), move=0, nodes=549946,
                   terminals=255168, where="the empty board")

    def test_alpha_beta_full_game(self):
        self.check(search.alpha_beta_search, TicTacToe(), move=0, nodes=18297,
                   terminals=7330, where="the empty board")


if __name__ == "__main__":
    unittest.main()

import argparse

import adversarial_search as search
from tictactoe import TicTacToe
from tree_game import TreeGame

ALGORITHMS = {"minimax": search.minimax_search,
              "alphabeta": search.alpha_beta_search}


def run_tree(args):
    for name, fn in ALGORITHMS.items():
        game = TreeGame.from_json(args.path, args.reverse)
        move = fn(game, game.initial)
        print(f"{name:10} move {move!s:4} nodes {game.nodes_visited:4} "
              f"terminals {game.terminals_evaluated:4}")


def play(args):
    game, state = TicTacToe(), TicTacToe().initial
    fn = ALGORITHMS[args.algorithm]
    while not game.is_terminal(state):
        print(TicTacToe.display(state), "\n")
        if game.to_move(state) == args.human:
            legal, move = game.actions(state), None
            while move not in legal:
                raw = input(f"Your move {legal}: ").strip()
                move = int(raw) if raw.isdigit() else None
        else:
            move = fn(game, state)
            print(f"Computer plays {move}\n")
        state = game.result(state, move)
    print(TicTacToe.display(state), "\n")
    print({1: "You win.", 0: "Draw.", -1: "Computer wins."}
          [game._utility(state, args.human)])


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    t = sub.add_parser("tree")
    t.add_argument("path")
    t.add_argument("--reverse", action="store_true")
    p = sub.add_parser("play")
    p.add_argument("--algorithm", choices=ALGORITHMS, default="alphabeta")
    p.add_argument("--human", choices=["X", "O"], default="X")
    args = parser.parse_args()
    run_tree(args) if args.command == "tree" else play(args)


if __name__ == "__main__":
    main()

# Minimax and Alpha-Beta Pruning

Implement minimax and alpha-beta search from AIMA 4th edition, Figures 5.3 and 5.7, then measure how much alpha-beta prunes.

## Setup

```
conda env create -f environment.yml
conda activate ai-search
```

## Files

| File | |
| --- | --- |
| `adversarial_search.py` | Your code. The only file you edit. |
| `main.py` | Runs your search on a tree, or plays tic-tac-toe. |
| `tests/` | The grading tests. |
| `environment.yml` | The course environment. |
| `trees/` | The class worksheet tree, and AIMA Figure 5.2. |
| `game.py`, `tree_game.py`, `tictactoe.py` | The games. Do not modify. |

## Tasks

1. Implement `minimax_search`.
2. Implement `alpha_beta_search`.
3. Play tic-tac-toe against your program with `python main.py play`. It should never lose.

## Game interface

Use only these methods:

| Method | Returns |
| --- | --- |
| `game.to_move(state)` | the player to move |
| `game.actions(state)` | the legal moves, in order |
| `game.result(state, action)` | the state after a move |
| `game.is_terminal(state)` | whether the game is over |
| `game.utility(state, player)` | the final score for `player` |

In the trees, states and actions are node names. In tic-tac-toe, an action is a cell from 0 to 8, numbered left to right, top to bottom.

## Pseudocode

From AIMA 4th edition.

```
function MINIMAX-SEARCH(game, state) returns an action
    player ← game.TO-MOVE(state)
    value, move ← MAX-VALUE(game, state)
    return move

function MAX-VALUE(game, state) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← −∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MIN-VALUE(game, game.RESULT(state, a))
        if v2 > v then
            v, move ← v2, a
    return v, move

function MIN-VALUE(game, state) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← +∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MAX-VALUE(game, game.RESULT(state, a))
        if v2 < v then
            v, move ← v2, a
    return v, move
```

*Figure 5.3* An algorithm for calculating the optimal move using minimax—the move that leads to a terminal state with maximum utility, under the assumption that the opponent plays to minimize utility. The functions MAX-VALUE and MIN-VALUE go through the whole game tree, all the way to the leaves, to determine the backed-up value of a state and the move to get there.

```
function ALPHA-BETA-SEARCH(game, state) returns an action
    player ← game.TO-MOVE(state)
    value, move ← MAX-VALUE(game, state, −∞, +∞)
    return move

function MAX-VALUE(game, state, α, β) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← −∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MIN-VALUE(game, game.RESULT(state, a), α, β)
        if v2 > v then
            v, move ← v2, a
            α ← MAX(α, v)
        if v ≥ β then return v, move
    return v, move

function MIN-VALUE(game, state, α, β) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← +∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MAX-VALUE(game, game.RESULT(state, a), α, β)
        if v2 < v then
            v, move ← v2, a
            β ← MIN(β, v)
        if v ≤ α then return v, move
    return v, move
```

*Figure 5.7* The alpha–beta search algorithm. Notice that these functions are the same as the MINIMAX-SEARCH functions in Figure 5.3, except that we maintain bounds in the variables α and β, and use them to cut off search when a value is outside the bounds.

## Requirements

The tests count the states your search visits, so follow the pseudocode exactly:

- Keep `player` in scope for `MAX-VALUE` and `MIN-VALUE`. Nested functions are simplest.
- Return utility for `player`, the player to move at the root.
- Use non-strict cutoffs, `≥` and `≤`.
- Call `is_terminal` once per state and `utility` once per terminal state.
- Examine moves in the order `actions` returns them.
- Use `math.inf` for infinity.

## Testing

```
pytest                              # all tests
pytest -k TestMinimaxOnTrees        # one part: also TestAlphaBetaOnTrees, TestTicTacToe
python main.py tree trees/worksheet.json            # move and counts on a tree
python main.py tree trees/worksheet.json --reverse
```

## Playing tic-tac-toe

Your search chooses the computer's moves, so implement it first.

```
python main.py play                         # you are X and move first
python main.py play --human O               # the computer moves first
python main.py play --algorithm minimax     # use minimax instead of alpha-beta
```

The board shows each empty cell's number. Type a number from the list in the prompt and press Enter.

## Submission

Submit `adversarial_search.py`.

## Grading

| Component | Points |
| --- | --- |
| Minimax on trees | 30 |
| Alpha-beta on trees | 45 |
| Tic-tac-toe | 25 |
| **Total** | **100** |

Code that special-cases a tree or position earns no credit for that part.
import math
from game import Game as game

def minimax_search(game, state):
    """Implement minimax from pseudocode.
    returns an action (move)
    """
    def max_value(game,state):
        """Implement the max_value function for minimax.
        returns a tuple (utility, move)
        """
        if game.is_terminal(state):
            return (game.utility(state,player), None)
        max = -math.inf
        move = None
        for a in game.actions(state):
            value, act = min_value(game, game.result(state,a))
            if value > max:
                max = value
                move = a
        return (max, move)


    #----------------
    def min_value(game,state):
        """Implement the min_value function for minimax.
        returns a tuple (utility, move)
        """
        if game.is_terminal(state):
            return (game.utility(state,player), None)
        min = math.inf
        move = None
        for a in game.actions(state):
            value, act = max_value(game, game.result(state,a))
            if value < min:
                min = value
                move = a
        return (min,move)




    #---------------
    player = game.to_move(state) # declare the player variable so the functions implemented later can call it when in use
    (value, move) = max_value(game, state)
    return move





#-----
def alpha_beta_search(game, state):
    """Implement alpha beta pruning from pseudocode.
    returns an action
    """
    def max_value_ab(game, state, alpha, beta):
        """Implement the max_value function for alpha beta pruning."""
        if game.is_terminal(state):
            return (game.utility(state,player), None)
        max_value = -math.inf
        move = None
        for a in game.actions(state):
            value, act = min_value_ab(game, game.result(state,a),alpha,beta)
            if value > max_value:
                max_value = value
                move = a
                alpha = max(alpha,max_value)
            #pruning
            if max_value >= beta:
                return ( value, move)
        return (max_value, move)
    #---
    def min_value_ab(game, state, alpha, beta):
        """Implement the min_value function for alpha beta pruning.
        returns a tuple (utility, move)
        """
        if game.is_terminal(state):
            return (game.utility(state,player), None)
        min_value = math.inf
        move = None
        for a in game.actions(state):
            value, act = max_value_ab(game, game.result(state,a), alpha, beta)
            if value < min_value:
                min_value = value
                move = a
                beta = min(beta, min_value)
            if min_value <= alpha:
                return (min_value, move)
        return (min_value,move)
    #---

        
    player = game.to_move(state)
    value, move = max_value_ab(game,state, -math.inf, math.inf)
    return move



#null in psuedocode = None

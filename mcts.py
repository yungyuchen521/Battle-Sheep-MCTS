from math import sqrt, log
from copy import deepcopy
# from queue import Queue
from random import choice
from time import time as clock
from meta import GameMeta, MCTSMeta
from state import State, Move


class Node:
    """
    Node for the MCTS. Stores the move applied to reach this node from its parent,
    stats for the associated game position, children, parent and outcome
    (outcome==none unless the position ends the game).
    Args:
        move:
        parent:
        N (int): times this position was visited
        Q (int): average reward (wins-losses) from this position
        Q_RAVE (int): times this move has been critical in a rollout
        N_RAVE (int): times this move has appeared in a rollout
        children (dict): dictionary of successive nodes
        outcome (int): If node is a leaf, then outcome indicates
                       the winner, else None
    """

    def __init__(self, move: Move = None, parent: object = None):
        """
        Initialize a new node with optional move and parent and initially empty
        children list and rollout statistics and unspecified outcome.

        """
        self.move = move
        self.parent = parent
        self.children = []
        self.N = 0       # times this position was visited
        self.Q = []      # total points of all players from this node
        self.Q_RAVE = 0  # times this move has been critical in a rollout
        self.N_RAVE = 0  # times this move has appeared in a rollout

        # =========== define gameover in State 1st ===========

        # self.outcome = GameMeta.PLAYERS['none']

        # ====================================================

    # def add_children(self, children: dict) -> None:
    #     """
    #     Add a list of nodes to the children of this node.

    #     """
    #     for child in children:
    #         self.children[child.move] = child

    @property
    def value(self, explore: float = MCTSMeta.EXPLORATION):
        """
        Calculate the UCT value of this node relative to its parent, the parameter
        "explore" specifies how much the value should favor nodes that have
        yet to be thoroughly explored versus nodes that seem to have a high win
        rate.
        Currently explore is set to 0.5.

        """
        # if the node is not visited, set the value as infinity. Nodes with no visits are on priority
        # (lambda: print("a"), lambda: print("b"))[test==true]()
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)  # exploitation + exploration


class UctMctsAgent:
    """
    Basic no frills implementation of an agent that preforms MCTS for hex.
    Attributes:
        root_state (GameState): Game simulator that helps us to understand the game situation
        root (Node): Root of the tree search
        run_time (int): time per each run
        node_count (int): the whole nodes in tree
        num_rollouts (int): The number of rollouts for each search
        EXPLORATION (int): specifies how much the value should favor
                           nodes that have yet to be thoroughly explored versus nodes
                           that seem to have a high win rate.
    """

    def __init__(self, state):
        self.root_state = deepcopy(state)
        self.root = Node()
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def search(self, time_budget: int) -> None:
        """
        Search and update the search tree for a
        specified amount of time in seconds.

        """
        start_time = clock()
        num_rollouts = 0

        # do until we exceed our time budget
        while clock() - start_time < time_budget:
            node, state = self.select()
            # turn = state.turn()
            self.simulate(state) # random play until gameover
            self.backpropagate(node, state.get_points())
            num_rollouts += 1
        run_time = clock() - start_time
        node_count = self.tree_size() # ======= remember to delete =======
        self.run_time = run_time
        self.node_count = node_count  # ======= remember to delete =======
        self.num_rollouts = num_rollouts

    def select(self) -> tuple:
        """
        Select a node in the tree to preform a single simulation from.

        """
        node = self.root
        state = deepcopy(self.root_state)

        # stop if we find reach a leaf node
        while len(node.children) != 0:
            # descend to the maximum value node, break ties at random
            # max_value = max(children, key=lambda n: n.value).value
            # max_nodes = [n for n in node.children.values() if n.value == max_value]
            max_value = max(node.children, key=lambda n: n.value).value
            max_nodes = [n for n in node.children if n.value == max_value]
            
            node = choice(max_nodes)
            state.play(node.move)

            # if some child node has not been explored select it before expanding others
            if node.N == 0:
                return node, state

        # if we reach a leaf node generate its children and return one of them
        # if the node is terminal, just return the terminal node
        if self.expand(node, state):
            node = choice(list(node.children))
            node = choice(node.children)
            state.play(node.move)
        
        return node, state

    @staticmethod
    def expand(parent: Node, state: State) -> bool:
        """
        Generate the children of the passed "parent" node based on the available
        moves in the passed gamestate and add them to the tree.

        Returns:
            bool: returns false If node is leaf (the game has ended).
        """
        
        # children = []

        # ========== complete gameover in State 1st ==========

        if state.gameover():
            # game is over at this node so nothing to expand
            return False

        # ====================================================

        for move in state.get_valid_moves():
            parent.children.append(Node(move, parent))

        # parent.add_children(children)
        return True

    @staticmethod
    def simulate(state: State) -> list:
        """
        Simulate an entirely random game from the passed state and return the winning
        player.

        Args:
            state: game state
        """

        while not state.gameover():
            # ============= to-dos: no need to call get_valid_moves in every iteration ============= 
            move = choice(state.get_valid_moves())
            # ======================================================================================
            state.play(move)

    @staticmethod
    def backpropagate(node: Node, points: list) -> None:
        """
        Update the node statistics on the path from the passed node to root to reflect
        the outcome of a randomly simulated playout.

        Args:
            node:
            points: outcome of the rollout

        Returns:
            object:

        """
        # Careful: The reward is calculated for player who just played
        # at the node and not the next player to play

        while node is not None:
            node.N += 1
            node.Q += points
            node = node.parent

    def get_best_child(self) -> tuple:
        """
        Return the best move according to the current tree.
        Returns:
            best move in terms of the most simulations number unless the game is over
        """
        if self.root_state.gameover():
            return None

        # choose the move of the most simulated node breaking ties randomly
        max_value = max(self.root.children, key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children if n.N == max_value]
        bestchild = choice(max_nodes)
        return bestchild

    def move_to(self, child: Node):
        """
        Make the passed move and update the tree appropriately. It is
        designed to let the player choose an action manually (which might
        not be the best action).
        Args:
            move:
        """
        
        child.parent = None
        self.root = child
        self.root_state.play(child.move)
        # return

        # if for whatever reason the move is not in the children of
        # the root just throw out the tree and start over
        # self.root_state.play(move)
        # self.root = Node()

    # def set_gamestate(self, state: State) -> None:
    #     """
    #     Set the root_state of the tree to the passed gamestate, this clears all
    #     the information stored in the tree since none of it applies to the new
    #     state.

    #     """
    #     self.root_state = deepcopy(state)
    #     self.root = Node()

    # def statistics(self) -> tuple:
    #     return self.num_rollouts, self.node_count, self.run_time

    # def tree_size(self) -> int:
    #     """
    #     Count nodes in tree by BFS.
    #     """
    #     Q = Queue()
    #     count = 0
    #     Q.put(self.root)
    #     while not Q.empty():
    #         node = Q.get()
    #         count += 1
    #         for child in node.children.values():
    #             Q.put(child)
    #     return count
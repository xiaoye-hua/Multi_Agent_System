import numpy as np
from collections import defaultdict
from abc import ABC, abstractmethod


class MonteCarloTreeSearchNode(ABC):

    def __init__(self, state, parent=None, **kwargs):
        """
        Parameters
        ----------
        state : mctspy.games.common.TwoPlayersAbstractGameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.parent = parent
        self.children = []

    @property
    @abstractmethod
    def untried_actions(self):
        """

        Returns
        -------
        list of mctspy.games.common.AbstractGameAction

        """
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def is_terminal_node(self):
        pass

    @abstractmethod
    def rollout(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]


class OnePlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):
    def __init__(self, state, c_param, parent=None):
        super().__init__(state, parent)
        self._number_of_visits = 0.
        # self._results = defaultdict(int)
        self._results = 0
        self._untried_actions = None
        self.c_params = c_param

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        # wins = self._results[self.parent.state.next_to_move]
        # loses = self._results[-1 * self.parent.state.next_to_move]
        # return wins - loses
        return self._results

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = OnePlayersGameMonteCarloTreeSearchNode(
            next_state, parent=self
            , c_param=self.c_params
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1.
        # self._results[result] += 1.
        self._results += result
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, c_param=None):
        if c_param is not None:
            choices_weights = [
                (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
                for c in self.children
            ]
        else:
            choices_weights = [
                (c.q / c.n) + self.c_params * np.sqrt((2 * np.log(self.n) / c.n))
                for c in self.children
            ]
        return self.children[np.argmax(choices_weights)]


# class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):
#
#     def __init__(self, state, parent=None):
#         super().__init__(state, parent)
#         self._number_of_visits = 0.
#         self._results = defaultdict(int)
#         self._untried_actions = None
#
#     @property
#     def untried_actions(self):
#         if self._untried_actions is None:
#             self._untried_actions = self.state.get_legal_actions()
#         return self._untried_actions
#
#     @property
#     def q(self):
#         wins = self._results[self.parent.state.next_to_move]
#         loses = self._results[-1 * self.parent.state.next_to_move]
#         return wins - loses
#
#     @property
#     def n(self):
#         return self._number_of_visits
#
#     def expand(self):
#         action = self.untried_actions.pop()
#         next_state = self.state.move(action)
#         child_node = TwoPlayersGameMonteCarloTreeSearchNode(
#             next_state, parent=self
#         )
#         self.children.append(child_node)
#         return child_node
#
#     def is_terminal_node(self):
#         return self.state.is_game_over()
#
#     def rollout(self):
#         current_rollout_state = self.state
#         while not current_rollout_state.is_game_over():
#             possible_moves = current_rollout_state.get_legal_actions()
#             action = self.rollout_policy(possible_moves)
#             current_rollout_state = current_rollout_state.move(action)
#         return current_rollout_state.game_result
#
#     def backpropagate(self, result):
#         self._number_of_visits += 1.
#         self._results[result] += 1.
#         if self.parent:
#             self.parent.backpropagate(result)

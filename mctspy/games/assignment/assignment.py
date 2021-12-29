import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction


class AssignmentMove(AbstractGameAction):
    def __init__(self, value):
        assert value in ["L", 'R'], value
        # self.x_coordinate = x_coordinate
        # self.y_coordinate = y_coordinate
        self.action = value

    # def __repr__(self):
    #     return "x:{0} y:{1} v:{2}".format(
    #         self.x_coordinate,
    #         self.y_coordinate,
    #         self.value
    #     )


class AssignmentGameState:
    def __init__(self, tree_terminate_depth: int, target_node_address: str, current_depth=0, current_node_address=''):
        self.current_depth = current_depth
        self.current_node_address = current_node_address
        self.tree_terminate_depth = tree_terminate_depth
        self.target_node_address = target_node_address

    @property
    def game_result(self):
        if len(self.target_node_address) != len(self.current_node_address):
            return None
        else:
            B = 5
            tao = 3
            distance = self.get_distance(add1=self.target_node_address, add2=self.current_node_address)
            x = B*np.exp(-distance/tao)
            return x

    def get_distance(self, add1: str, add2: str):
        assert len(add1) == len(add1), f"{add1}; {add2}"
        res = 0
        for e1, e2 in zip(list(add1), list(add2)):
            if e1 != e2:
                res += 1
        return res

    def is_game_over(self):
        if self.current_depth == self.tree_terminate_depth:
            return True
        return False

    # def update_state(self, move: str):
    #     self.current_depth += 1
    #     self.current_node_address += move

    # def is_move_legal(self, move):
    #     # check if correct player moves
    #     if move.value != self.next_to_move:
    #         return False
    #
    #     # check if inside the board on x-axis
    #     x_in_range = (0 <= move.x_coordinate < self.board_size)
    #     if not x_in_range:
    #         return False
    #
    #     # check if inside the board on y-axis
    #     y_in_range = (0 <= move.y_coordinate < self.board_size)
    #     if not y_in_range:
    #         return False
    #
    #     # finally check if board field not occupied yet
    #     return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move: AssignmentMove):
        # if not self.is_move_legal(move):
        #     raise ValueError(
        #         "move {0} on board {1} is not legal". format(move, self.board)
        #     )
        # new_board = np.copy(self.board)
        # new_board[move.x_coordinate, move.y_coordinate] = move.value
        # if self.next_to_move == AssignmentGameState.x:
        #     next_to_move = AssignmentGameState.o
        # else:
        #     next_to_move = AssignmentGameState.x

        return AssignmentGameState(tree_terminate_depth=self.tree_terminate_depth,
                                   target_node_address=self.target_node_address,
                                   current_depth=self.current_depth+1,
                                   current_node_address=self.current_node_address+move.action)

    def get_legal_actions(self):
        return [AssignmentMove(value='L'), AssignmentMove(value="R")]
        # indices = np.where(self.board == 0)
        # return [
        #     AssignmentMove(coords[0], coords[1], self.next_to_move)
        #     for coords in list(zip(indices[0], indices[1]))
        # ]

import numpy as np

B = 10
tao = 10


class AssignmentMove():
    def __init__(self, value):
        assert value in ["L", 'R'], value
        self.action = value


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


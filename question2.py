import numpy as np
import pandas as pd
from mctspy.games.assignment.assignment import AssignmentGameState, AssignmentMove
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.tree.nodes import OnePlayersGameMonteCarloTreeSearchNode

# Config
epoch = 10 # 同一个target_address, 实验epoch次，然后取平均
tree_depth = 12
c_param = 0.1
mcts_iteration_num = 50
snowcap_iteration_num = 1

def generate_target_address(depth: int):
    lst = ["L", "R"]
    res = np.random.choice(a=lst, size=depth)
    return ''.join(res)

target_node_address = generate_target_address(depth=tree_depth)


# if tree_depth == 3:
#     target_node_address = "LRL"

distance_lst = []
game_result_lst = []
for _ in range(epoch):
    current_state = AssignmentGameState(tree_terminate_depth=tree_depth, target_node_address=target_node_address)
    action_lst = []
    while not current_state.is_game_over():
        search_begin_node = OnePlayersGameMonteCarloTreeSearchNode(state=current_state, c_param=c_param)
        best_child_node = MonteCarloTreeSearch(node=search_begin_node).best_action(simulations_number=mcts_iteration_num)
        best_move = AssignmentMove(value=best_child_node.state.current_node_address[-1])
        action_lst.append(best_move.action)
        current_state = current_state.move(move=best_move)
    distance = current_state.get_distance(current_state.target_node_address, current_state.current_node_address)
    game_result = current_state.game_result
    print(f"target: {current_state.target_node_address}")
    print(f"current: {current_state.current_node_address}")
    print(f"distance: {distance}")
    print(f"Game result: {game_result}")
    distance_lst.append(distance)
    game_result_lst.append(game_result)

def get_stats(lst):
    res = {}
    res['mean'] = np.mean(lst)
    res['min'] = np.min(lst)
    res['max'] = np.max(lst)
    return res
df = {}
lst_lst = [distance_lst, game_result_lst]
lst_name = ['distance', 'game_result']

for name, lst in zip(lst_name, lst_lst):
    stats = get_stats(lst)
    df[name] = stats
df = pd.DataFrame(df)
print(df)




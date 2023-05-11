import numpy as np
from helpers import piece_states_initializer

board_size = 14

state_init = np.zeros([board_size, board_size], dtype=int)

piece_list_init = [
    {"id": 1, "size": 5, "value": [[1, 1, 0], [0, 1, 1], [0, 0, 1]]},
    {"id": 2, "size": 5, "value": [[1, 1, 0], [0, 1, 0], [0, 1, 1]]},
    {"id": 3, "size": 5, "value": [[1, 0, 0], [1, 0, 0], [1, 1, 1]]},
    {"id": 4, "size": 5, "value": [[1, 1, 1, 1], [1, 0, 0, 0]]},
    {"id": 5, "size": 5, "value": [[1, 1], [1, 0], [1, 1]]},
    {"id": 6, "size": 5, "value": [[0, 1, 0], [1, 1, 1], [0, 1, 0]]},
    {"id": 7, "size": 5, "value": [[1, 0, 0], [1, 1, 1], [1, 0, 0]]},
    {"id": 8, "size": 5, "value": [[1, 1, 0, 0], [0, 1, 1, 1]]},
    {"id": 9, "size": 5, "value": [[1, 1, 1, 1, 1]]},
    {"id": 10, "size": 5, "value": [[1, 1, 1, 1], [0, 0, 1, 0]]},
    {"id": 11, "size": 5, "value": [[1, 1, 0], [0, 1, 1], [0, 1, 0]]},
    {"id": 12, "size": 5, "value": [[1, 1, 0], [1, 1, 1]]},
    {"id": 13, "size": 4, "value": [[1, 1, 1], [1, 0, 0]]},
    {"id": 14, "size": 4, "value": [[1, 1, 1], [0, 1, 0]]},
    {"id": 15, "size": 4, "value": [[0, 1, 1], [1, 1, 0]]},
    {"id": 16, "size": 4, "value": [[1, 1], [1, 1]]},
    {"id": 17, "size": 4, "value": [[1, 1, 1, 1]]},
    {"id": 18, "size": 3, "value": [[1, 1, 1]]},
    {"id": 19, "size": 3, "value": [[1, 1], [1, 0]]},
    {"id": 20, "size": 2, "value": [[1, 1]]},
    {"id": 21, "size": 1, "value": [[1]]},
]
piece_list_init = [{k: np.array(v) if k == 'value' else v for k,v in d.items()} for d in piece_list_init]

piece_states_init = piece_states_initializer(piece_list_init)

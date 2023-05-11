import numpy as np
from collections import Counter

board = np.zeros([8, 8], dtype=int)
piece = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])

print(board.shape)

board[3:(3 + piece.shape[0]), 3:(3 + piece.shape[1])] = piece

positions = np.transpose(np.where(board != 0))

valid_positions = []
invalid_positions = []

corner_positions = []
all_positions = []

for piece in positions:
    corner_positions.extend([(piece[0]+i, piece[1]+j) for i in (-1, 1) for j in (-1, 1)])
    all_positions.extend([(piece[0]+i, piece[1]+j) for i in range(-1, 2) for j in range(-1, 2)])

counter = Counter(all_positions)
single_positions = [k for k, v in counter.items() if v == 1]

for position in single_positions:
    if position in corner_positions:
        valid_positions.append(position)

invalid_positions = list(set(all_positions) - set(valid_positions))

for position in invalid_positions:
    board[position] = -1

for position in valid_positions:
    board[position] = 1

print(board)

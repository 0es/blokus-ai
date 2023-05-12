import numpy as np
from constant import state_init, piece_list_init, board_size
from helpers import piece_states_initializer
import matplotlib.pyplot as plt
import time
import copy
import random
from collections import Counter

def plt_draw(board):
    plt.cla()
    plt.imshow(board, cmap='binary', interpolation='nearest')
    plt.draw()
    plt.pause(1)

# 棋盘逻辑控制
class Board(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.last_state = copy.deepcopy(state_init)
        self.state = copy.deepcopy(state_init)

        self.piece_set = set(range(1, len(piece_list_init) + 1))
        self.piece_states = piece_states_initializer(copy.deepcopy(piece_list_init), game_id)

    # 获取棋子的全部状态
    def piece_states_by_id(self, piece_id):
        return self.piece_states[piece_id]

    # 判断落子位置是否合法
    def is_valid(self, piece, point):
        piece_value = piece['value']

        # 超界
        if point[0] + piece_value.shape[0] > board_size:
            return False
        if point[1] + piece_value.shape[1] > board_size:
            return False

        # 规则判断
        piece_sim_state = self.sim_fall(piece, point)
        positions = np.transpose(np.where(piece_sim_state != 0)) # 拿到待落子位置集合

        valid_positions = []
        invalid_positions = []

        # 中间数据
        corner_positions = []
        all_positions = []
        single_positions = []

        for piece in positions:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # 如果扩展位超出棋盘则跳过
                    if piece[0] + i < 0 or piece[1] + j < 0 or piece[0] + i >= board_size or piece[1] + j >= board_size:
                        continue

                    position = (piece[0] + i, piece[1] + j)

                    if i != 0 and j != 0:
                        corner_positions.append(position)

                    all_positions.append(position)

        counter = Counter(all_positions)
        single_positions = [k for k, v in counter.items() if v == 1] # 需要去除某棋子角位置为其他棋子行位置的情况

        for position in single_positions:
            if position in corner_positions:
                valid_positions.append(position)

        invalid_positions = list(set(all_positions) - set(valid_positions))

        # 无效位置不能有棋子
        for position in invalid_positions:
            if self.state[position] != 0:
                return False

        # 有效位置必须有棋子
        for position in valid_positions:
            if self.state[position] != 0:
                return True

        return False

    # 起手
    def go_hand(self):
        piece_state_list = []

        for piece_id in self.piece_set:
            piece_state_list.extend(list(filter(lambda x: x['value'][0][0] == self.game_id, self.piece_states_by_id(piece_id))))

        piece = random.choice(piece_state_list)
        self.fall(piece, [0, 0])

    # 后手随机落子
    def random_hand(self):
        piece_state_list = []

        # 遍历棋子状态
        for piece_id in self.piece_set:
            piece_state_list.extend(self.piece_states_by_id(piece_id))

        valid_fall_list = []

        # 将所有合理下法遍历
        # 遍历落子位置
        for point_x in range(board_size):
            for point_y in range(board_size):
                for piece_state in piece_state_list:
                    point = (point_x, point_y)

                    # 判断是否合法
                    if self.is_valid(piece_state, point):
                        valid_fall_list.append({ 'piece': piece_state, 'point': point })

        print(f'合理下法数量: {len(valid_fall_list)}')

        if len(valid_fall_list) == 0:
            return

        # 随机一种下法
        valid_fall = random.choice(valid_fall_list)
        self.fall(valid_fall['piece'], valid_fall['point'])


    # 落子
    def fall(self, piece, point):
        piece_value = piece['value']

        self.last_state = copy.deepcopy(self.state)
        self.state[point[0]:(point[0] + piece_value.shape[0]), point[1]:(point[1] + piece_value.shape[1])] = piece_value

        # 删除该棋子
        self.piece_set.remove(piece['id'])

    # 模拟落子棋盘
    def sim_fall(self, piece, point):
        piece_value = piece['value']
        state = copy.deepcopy(state_init)

        state[point[0]:(point[0] + piece_value.shape[0]), point[1]:(point[1] + piece_value.shape[1])] = piece_value
        return state

class Game(object):
    def __init__(self, game_id):
        self.id = game_id
        self.board = Board(self.id)
        self.game_start = False
        self.winner = None

    def graphic(self):
        plt_draw(self.board.state)

    # 游戏进行 需要互传局面
    def goon(self):
        if self.game_start == False:
            self.board.go_hand()
            self.game_start = True
        else:
            self.board.random_hand()

        self.graphic()

        return self.board.state



if __name__ == '__main__':
    plt.ion()
    game1 = Game(1)
    # game2 = Game(2)
    state_buffer = []

    # 模拟20步
    for i in range(20):
        state_buffer = game1.goon()
        # state_buffer = game2.goon()

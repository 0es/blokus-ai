import numpy as np
from constant import state_init, piece_list_init, board_size
from helpers import piece_states_initializer, flip180
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
        self.last_state = []
        self.state = []

        self.piece_set = set(range(1, len(piece_list_init) + 1))
        self.piece_states = piece_states_initializer(copy.deepcopy(piece_list_init), game_id)

        self.piece_state_point_invalid = {}

    # 获取棋子的全部状态
    def piece_states_by_id(self, piece_id):
        return self.piece_states[piece_id]

    def piece_size_by_id(self, piece_id):
        return self.piece_states[piece_id][0]['size']

    # 判断落子位置是否合法
    def is_valid(self, piece, point):
        state_id = piece['state_id']
        piece_value = piece['value']

        def set_invalid_cache():
            if state_id not in self.piece_state_point_invalid:
                self.piece_state_point_invalid[state_id] = set()

            self.piece_state_point_invalid[state_id].add(point)

        # 超界
        if point[0] + piece_value.shape[0] > board_size or point[1] + piece_value.shape[1] > board_size:
            set_invalid_cache()
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
                    # 如果扩展位超出棋盘则跳过该位置
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

        # 开始判断
        # 分离局面
        _state = self.state
        state_mine = np.where(_state == self.game_id, _state, 0)
        state_other = np.where(_state == self.game_id, 0, _state)

        # 不能覆盖别人的棋子
        for position in positions:
            if state_other[position[0]][position[1]] != 0:
                set_invalid_cache()
                return False

        # 无效位置不能有自己的棋子
        for position in invalid_positions:
            if state_mine[position] != 0:
                set_invalid_cache()
                return False

        # 有效位置必须有自己的棋子
        for position in valid_positions:
            if state_mine[position] != 0:
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
                    state_id = piece_state['state_id']

                    # 先取缓存
                    if state_id in self.piece_state_point_invalid and point in self.piece_state_point_invalid[state_id]:
                        continue

                    # 判断是否合法
                    if self.is_valid(piece_state, point):
                        valid_fall_list.append({ 'piece': piece_state, 'point': point })

        print(f'[player{self.game_id}] 合理下法: {len(valid_fall_list)}')

        if len(valid_fall_list) != 0:
            # 随机一种下法
            valid_fall = random.choice(valid_fall_list)
            self.fall(valid_fall['piece'], valid_fall['point'])

        return len(valid_fall_list)

    # 保存局面
    def save_state(self, state):
        self.last_state = copy.deepcopy(self.state)
        self.state = copy.deepcopy(state)

    # 落子
    def fall(self, piece, point):
        piece_value = piece['value']

        self.last_state = copy.deepcopy(self.state)
        self.state[point[0]:(point[0] + piece_value.shape[0]), point[1]:(point[1] + piece_value.shape[1])] = piece_value

        # 删除该棋子
        self.piece_set.remove(piece['id'])

    # 模拟空白棋盘落子
    def sim_fall(self, piece, point):
        piece_value = piece['value']
        state = copy.deepcopy(state_init)

        state[point[0]:(point[0] + piece_value.shape[0]), point[1]:(point[1] + piece_value.shape[1])] = piece_value
        return state

class Game(object):
    def __init__(self, game_id, player_num=1):
        self.id = game_id
        self.player_num = player_num
        self.board = Board(self.id)
        self.game_start = False

    def graphic(self):
        state = self.board.state

        if self.id == 2:
            state = flip180(state)

        plt_draw(state)

    # 游戏进行 需要互传局面
    def goon(self, state):
        # 先设置局面
        if self.player_num == 2:
            state = flip180(state)

        self.board.save_state(state)
        self.graphic()

        if self.game_start == False:
            self.board.go_hand()
            self.game_start = True
        else:
            if self.board.random_hand() == 0:
                # 计算剩余棋子 last_size少的获胜
                last_size = 0

                for piece_id in self.board.piece_set:
                    last_size += self.board.piece_size_by_id(piece_id)

                return (self.board.state, 1, last_size)

        self.graphic()

        return (self.board.state, 0, 0)



if __name__ == '__main__':
    plt.ion()

    players = (1, 2)
    state_buffer = copy.deepcopy(state_init)
    games = []
    scores = {}

    for player in players:
        games.append(Game(player, len(players)))

    # 开始模拟
    class Getoutofloop(Exception):
        pass

    try:
        while 1:
            for game in games:
                (state_buffer, end, last_size) = game.goon(state_buffer)

                if end != 0:
                    scores[game.id] = last_size

                    if len(scores) == len(players):
                        raise Getoutofloop()
    except Getoutofloop:
        for player in players:
            print(f'[player{player}] 剩余棋子数: {scores[player]}')

        min_value = min(scores.values())
        min_players = [k for k, v in scores.items() if v == min_value]

        if len(min_players) == 1:
            print(f'获胜者为player{min_players[0]}')
        else:
            print(f'平局')

        pass
    finally:
        print('游戏结束')

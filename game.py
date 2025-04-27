import numpy as np
import random
from collections import Counter
from constrain import rule

class ChineseDarkChessEnv:
    def __init__(self):
        self.board_size = (rule.height, rule.width)
        self.num_cells = rule.num_cell
        self.rank = rule.rank
        self.reset()

    def reset(self):
        red_pieces = rule.red_pieces
        black_pieces = rule.black_pieces
        pieces = red_pieces + black_pieces
        assert len(pieces) == 32
        random.shuffle(pieces)

        self.board = np.array(pieces)
        self.revealed = np.array([0] * self.num_cells)
        self.red_player = None
        self.current_player = 0
        self.no_flip_or_capture_steps = 0  

        return self._get_obs()

    def step(self, action):
        src, dst = action

        reward = 0
        done = False
        info = {}

        if src == dst:
            if self.revealed[src] == 0:
                self.revealed[src] = 1
                self.no_flip_or_capture_steps = 0
                if self.red_player is None:
                    if self.board[src].isupper():
                        self.red_player = self.current_player
                    else:
                        self.red_player = 1 - self.current_player
            else:
                raise ValueError("Cannot flip an already revealed piece.")
        else:
            if self.revealed[src] != 1:
                raise ValueError("Source piece not revealed.")

            if not self._is_legal_move(src, dst):
                raise ValueError("Illegal move.")

            if self.revealed[dst] == 1:
                reward = 1
                self.no_flip_or_capture_steps = 0
            else:
                self.no_flip_or_capture_steps += 1

            self.board[dst] = self.board[src]
            self.revealed[dst] = 1
            self.board[src] = '*'
            self.revealed[src] = -1

        self.current_player = 1 - self.current_player

        done, winner = self._check_winner()
        if done:
            reward = 1 if winner == self.current_player else -1
            info['winner'] = winner

        return self._get_obs(), reward, done, info

    def _get_obs(self):
        return (self.board.copy(), self.revealed.copy())

    def get_legal_actions(self):
        actions = []
        for idx in range(self.num_cells):
            if self.revealed[idx] == 0:
                actions.append((idx, idx))
            elif self.revealed[idx] == 1:
                for neighbor in self._get_neighbors(idx):
                    if self._is_legal_move(idx, neighbor):
                        actions.append((idx, neighbor))
        return actions

    def _get_neighbors(self, idx):
        h, w = self.board_size
        neighbors = []
        row, col = divmod(idx, w)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < h and 0 <= nc < w:
                neighbors.append(nr*w + nc)
        return neighbors

    def _is_legal_move(self, src, dst):
        if self.revealed[src] != 1 or self.board[src] == '*':
            return False
        if self.revealed[dst] == 0:
            return False
        if self._is_same_side(src, dst):
            return False
        if self.board[dst] == '*':
            return True

        src_piece = self.board[src]
        dst_piece = self.board[dst]

        if src_piece.lower() == 'c':  
            if not self._can_cannon_capture(src, dst):
                return False
        else:
            if not self._can_normal_capture(src_piece, dst_piece):
                return False

        return True

    def _is_same_side(self, src, dst):
        piece_src = self.board[src]
        piece_dst = self.board[dst]
        if piece_src == '*' or piece_dst == '*':
            return False
        return (piece_src.isupper() and piece_dst.isupper()) or (piece_src.islower() and piece_dst.islower())

    def _can_normal_capture(self, attacker, defender):
        attacker_rank = self.rank[attacker]
        defender_rank = self.rank[defender]

        if attacker.lower() == 'p' and defender.lower() == 'k':
            return True
        if attacker.lower() == 'k' and defender.lower() == 'p':
            return False

        return attacker_rank >= defender_rank

    def _can_cannon_capture(self, src, dst):
        h, w = self.board_size
        row_src, col_src = divmod(src, w)
        row_dst, col_dst = divmod(dst, w)

        if row_src != row_dst and col_src != col_dst:
            return False

        count = 0
        if row_src == row_dst:
            step = 1 if col_src < col_dst else -1
            for c in range(col_src + step, col_dst, step):
                if self.revealed[row_src * w + c] == 1:
                    count += 1
        else:
            step = 1 if row_src < row_dst else -1
            for r in range(row_src + step, row_dst, step):
                if self.revealed[r * w + col_src] == 1:
                    count += 1

        return count == 1

    def _check_winner(self):
        counter = Counter()
        for idx in range(self.num_cells):
            if self.revealed[idx] == 1:
                piece = self.board[idx]
                if piece.isupper():
                    counter['red'] += 1
                elif piece.islower():
                    counter['black'] += 1
            elif self.revealed[idx] == 0:
                counter['*'] += 1

        if counter['red'] == 0 and counter['*'] == 0:
            return True, 1 
        if counter['black'] == 0 and counter['*'] == 0:
            return True, 0 

        if self.no_flip_or_capture_steps >= 50:
            return True, -1 

        return False, None

    def render(self):
        h, w = self.board_size
        for r in range(h):
            row = ''
            for c in range(w):
                idx = r*w + c
                if self.revealed[idx] == 1:
                    row += f'{self.board[idx]:>2} '
                elif self.revealed[idx] == 0:
                    row += ' ? '
                else:
                    row += ' . '
            print(row)
        print()

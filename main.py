from random import choice
import time

board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
valid_move = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def show_board(board):
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])


class Board:
    def __init__(self, board, valid_moves, side, winner=None, last_move=None):
        self.board = board
        self.valid_moves = valid_moves
        self.side = side
        self.winner = winner
        self.last_move = last_move

    def check_winner(self):
        if self.board[0] == self.board[1] == self.board[2] != '-':
            self.winner = self.board[0]
        elif self.board[3] == self.board[4] == self.board[5] != '-':
            self.winner = self.board[3]
        elif self.board[6] == self.board[7] == self.board[8] != '-':
            self.winner = self.board[6]
        elif self.board[0] == self.board[3] == self.board[6] != '-':
            self.winner = self.board[0]
        elif self.board[1] == self.board[4] == self.board[7] != '-':
            self.winner = self.board[1]
        elif self.board[2] == self.board[5] == self.board[8] != '-':
            self.winner = self.board[2]
        elif self.board[0] == self.board[4] == self.board[8] != '-':
            self.winner = self.board[0]
        elif self.board[2] == self.board[4] == self.board[6] != '-':
            self.winner = self.board[2]


class Node:
    def __init__(self, position, parent=None):
        self.position = position

        self.parent = parent
        self.children = []

        self.win_x = 0
        self.win_y = 0
        self.draw = 0

    def generate_tree(self):
        for move in self.position.valid_moves:
            global counter
            new_valid_moves = self.position.valid_moves.copy()
            new_board = self.position.board.copy()
            new_side = 'x' if self.position.side == 'o' else 'o'

            new_board[move] = self.position.side
            new_valid_moves.remove(move)

            new_position = Board(new_board, new_valid_moves, new_side, last_move=move)
            new_position.check_winner()

            if new_position.winner is not None:
                counter += 1
                print(counter)
                # Monte-Carlo
                continue
            elif not new_valid_moves:
                counter += 1
                print(counter)
                # show_board(new_board)
                continue
            # show_board(new_board)

            new_node = Node(new_position, self)
            self.children.append(new_node)
            new_node.generate_tree()


start_time = time.time()
counter = 0
b1 = Board(board, valid_move, 'x')
root = Node(b1)
root.generate_tree()
end_time = time.time()

print(end_time - start_time)

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
            new_valid_moves = self.position.valid_moves.copy()
            new_board = self.position.board.copy()
            new_side = 'x' if self.position.side == 'o' else 'o'

            new_board[move] = self.position.side
            new_valid_moves.remove(move)

            new_position = Board(new_board, new_valid_moves, new_side, last_move=move)
            new_position.check_winner()
            new_node = Node(new_position, self)
            self.children.append(new_node)

            if new_position.winner is not None:
                new_node.update_grade(new_position.winner)
                continue
            elif new_valid_moves == []:
                new_node.update_grade(new_position.winner)
                continue

            new_node.generate_tree()

    def update_grade(self, winner):
        if winner == 'x':
            self.win_x += 1
        elif winner == 'o':
            self.win_y += 1
        else:
            self.draw += 1

        if self.parent is not None:
            self.parent.update_grade(winner)


start_time = time.time()

b1 = Board(board, valid_move, 'x')
root = Node(b1)

root.generate_tree()

end_time = time.time()

print("?????????? x: ", root.win_x)
print("?????????? o: ", root.win_y)
print("????????????:  ", root.draw)
print("?????????? ????????????????: ", round(end_time - start_time, 2), '??????')

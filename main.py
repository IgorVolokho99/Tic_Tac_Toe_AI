from random import choice
import time


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
        self.win_move = None
        self.best_move = None

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
        counter = 0
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
                counter += 1
                self.children[-1].win_move = True
                if counter == 2:
                    self.parent.position.best_move = True

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


board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
valid_move = [0, 1, 2, 3, 4, 5, 6, 7, 8]

start_time = time.time()

b1 = Board(board, valid_move, 'x')
root = Node(b1)

root.generate_tree()

end_time = time.time()

print("Побед x: ", root.win_x)
print("Побед o: ", root.win_y)
print("Ничьих:  ", root.draw)
print("Время подсчета: ", round(end_time - start_time, 2), 'сек')

# start = root
# show_board(start.position.board)
# while True:
#     move = int(input('Введите клетку куда вы хотите походить: ')) - 1
#     for child in start.children:
#         if move == child.position.last_move:
#             start = child
#             break
#     show_board(start.position.board)
#     best_percent = 0
#     best_child = None
#     for child in start.children:
#         percent = child.win_y / (child.win_x + child.win_y + child.draw)
#         if child.position.win_move:
#             best_move = child
#             break
#         elif percent > best_percent:
#             best_percent = percent
#             best_child = child
#             continue
#     start = best_child
#     print()
#     show_board(start.position.board)

start = root
while True:
    best_percent = 0
    best_child = None
    for child in start.children:
        percent = child.win_x / (child.win_x + child.win_y + child.draw)
        if child.position.win_move:
            best_move = child
            break
        elif percent > best_percent:
            best_percent = percent
            best_child = child
            continue

    start = best_child
    print()
    show_board(start.position.board)
    move = int(input('Введите клетку куда вы хотите походить: ')) - 1
    for child in start.children:
        if move == child.position.last_move:
            start = child
            break
    show_board(start.position.board)

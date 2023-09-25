from random import choice
import time


class Game:
    def __init__(self, board, valid_moves):
        self.board = board
        self.valid_moves = valid_moves
        self.b1 = Board(self.board, self.valid_moves, 'x')
        self.root = Node(self.b1)
        self.root.generate_tree()
        start_time = time.time()
        self.root.generate_tree()
        end_time = time.time()

        print("Побед x: ", self.root.win_x)
        print("Побед o: ", self.root.win_y)
        print("Ничьих:  ", self.root.draw)
        print("Время подсчета: ", round(end_time - start_time, 2), 'сек')
        self.run()

    def run(self):
        choice = input("Привет, выбери за кого ты будешь играть: \n1-X\n2-0\n")
        if choice == 'X':
            self.playerx()
        elif choice == '0':
            self.player0()
        else:
            self.run()

    def playerx(self):
        start = self.root
        print()
        show_board(start.position.board)
        while not start.position.winner and start.position.valid_moves:
            print()
            move = int(input('Введите клетку куда вы хотите походить: ')) - 1
            for child in start.children:
                if move == child.position.last_move:
                    start = child
                    break

            if not start.position.valid_moves or start.position.winner:
                break

            show_board(start.position.board)
            print()
            best_percent = -1
            best_child = None
            for child in start.children:
                percent = child.win_y / (child.win_x + child.win_y + child.draw)
                if child.position.win_move:
                    print('Тут')
                    best_child = child
                    break
                elif percent >= best_percent:
                    deffend = False
                    for childd in child.children:
                        if childd.position.win_move:
                            deffend = True
                    if deffend:
                        continue
                    flag = False
                    for childd in child.children:

                        if childd.position.best_move:
                            print('Тута')
                            for childdd in childd.children:
                                if childdd.position.win_move:
                                    flag = True
                                    break
                            if flag:
                                best_percent = percent
                                best_child = child
                                break
                    else:
                        best_percent = percent
                        best_child = child
                    if flag:
                        break

            start = best_child
            show_board(start.position.board)
            print("Побед X: ", start.win_x)
            print("Побед O: ", start.win_y)
            print("Ничьих : ", start.draw)
            print(f"Бот походил на клетку: {start.position.last_move}")

        print()
        show_board(start.position.board)
        print()
        show_result(start)

    def player0(self):
        start = self.root
        while not start.position.winner and start.position.valid_moves:
            best_percent = -1
            best_child = None
            for child in start.children:
                percent = child.win_x / (child.win_x + child.win_y + child.draw)
                if child.position.win_move:
                    best_child = child
                    break
                elif percent > best_percent:
                    best_percent = percent
                    best_child = child
                    continue

            start = best_child
            if not start.position.valid_moves or start.position.winner:
                break
            print()
            print(f"Бот походил на клетку: {start.position.last_move}")
            show_board(start.position.board)
            print()
            move = int(input('Введите клетку куда вы хотите походить: ')) - 1
            for child in start.children:
                if move == child.position.last_move:
                    start = child
                    break
            show_board(start.position.board)

        print()
        show_board(start.position.board)
        print()
        show_result(start)


def show_board(board):
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])


def show_result(node):
    if not node.position.winner:
        print("Победила дружба!")
    else:
        print(f"Победитель: {node.position.winner}!")


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
                self.children[-1].position.win_move = True
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


g = Game(['-'] * 9, list(range(9)))

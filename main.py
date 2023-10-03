from random import choice
import time


class Game:
    def __init__(self, board, valid_moves):
        self.board = board
        self.valid_moves = valid_moves
        self.b1 = Board(self.board, self.valid_moves, 'X')
        self.root = Node(self.b1)
        self.root.generate_tree()
        start_time = time.time()
        self.root.generate_tree()
        end_time = time.time()

        print("Побед X: ", self.root.win_x)
        print("Побед 0: ", self.root.win_y)
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

            for child in start.children:
                if self.find_best_0(child, 10):
                    start = child

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
            for child in start.children:
                if self.find_best_x(child, 10):
                    start = child
                    break

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

    def find_best_0(self, node, d):
        if d > 0:
            if node.position.winner == '0':
                return True
            elif node.position.winner is None and node.position.valid_moves == []:
                return True
            elif node.position.winner == 'X':
                return False
            elif node.children is []:
                return True
            else:
                if node.position.side == '0':
                    answers = []
                    for child in node.children:
                        answers.append(self.find_best_0(child, d - 1))
                    return any(answers)
                else:
                    answers = []
                    for child in node.children:
                        answers.append(self.find_best_0(child, d - 1))
                    return all(answers)
        else:
            return True

    def find_best_x(self, node, d):
        if d > 0:
            if node.position.winner == 'X':
                return True
            elif node.position.winner is None and node.position.valid_moves == []:
                return True
            elif node.position.winner == '0':
                return False
            elif node.children is []:
                return True
            else:
                if node.position.side == 'X':
                    answers = []
                    for child in node.children:
                        answers.append(self.find_best_x(child, d - 1))
                    return any(answers)
                else:
                    answers = []
                    for child in node.children:
                        answers.append(self.find_best_x(child, d - 1))
                    return all(answers)
        else:
            return True


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
            new_side = 'X' if self.position.side == '0' else '0'

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
        if winner == 'X':
            self.win_x += 1
        elif winner == '0':
            self.win_y += 1
        else:
            self.draw += 1

        if self.parent is not None:
            self.parent.update_grade(winner)


g = Game(['-'] * 9, list(range(9)))

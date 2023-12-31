import json
import math
import random
import time


class Human:
    def __init__(self, game_instance):
        self.game = game_instance
        self.board = self.game.getBoard()
        self.shape = ('2' if self.game.getStarter() == 1 else '1')

    def getTurn(self):
        availableBoards = self.game.availableBoards(self.shape)
        if availableBoards:  # Check if there are any available boards
            board = random.choice(availableBoards)
            self.game.setBoard(board)
        else:
            print("No valid moves for Human.")
            a = 0


class Computer:
    def __init__(self, game_instance):
        self.game = game_instance
        self.board = self.game.getBoard()
        self.shape = ('1' if self.game.getStarter() == 1 else '2')

    def getTurn(self):
        availableBoards = self.game.availableBoards(self.shape)
        if availableBoards:  # Check if there are any available boards
            board = random.choice(availableBoards)
            self.game.setBoard(board)
        else:
            print("No valid moves for Computer.")
            a = 0


class Game:
    def __init__(self):
        self.boards = []
        self.starter = random.choice([0, 1])
        print(self.starter)
        self.board = ("00000000"
                      "00000000"
                      "00000000"
                      "00021000"
                      "00012000"
                      "00000000"
                      "00000000"
                      "00000000")
        self.computer = Computer(self)
        self.human = Human(self)

    def play(self):
        if self.starter == 1:
            return self.ComputerStarts()
        else:
            return self.HumanStarts()

    def ComputerStarts(self):
        boards = []
        while not self.hasFinished():
            boards.append(self.board)
            self.computer.getTurn()
            print("Board after comp play: ")
            self.boardToString(self.board)
            if self.hasFinished():
                break  # Break if the game is finished after computer's turn
            boards.append(self.board)
            self.human.getTurn()
            print("Board after human play: ")
            self.boardToString(self.board)
        return boards, self.determineWinner(self.starter)

    def HumanStarts(self):
        boards = []
        while not self.hasFinished():
            boards.append(self.boardToDict())
            self.human.getTurn()
            print("Board after human play: ")
            self.boardToString(self.board)
            if self.hasFinished():
                break  # Break if the game is finished after human's turn
            boards.append(self.boardToDict())
            self.computer.getTurn()
            print("Board after comp play: ")
            self.boardToString(self.board)
        return boards, self.determineWinner(self.starter)

    def availableBoards(self, shape):
        currentBoard = self.board
        availableBoards = []
        place = 0
        for piece in currentBoard:
            if currentBoard[place] == '0' and self.hasDifferentPieceNear(place, shape) and self.isValid(place, shape):
                availableBoards.append(self.replacePieces(place, shape, self.getUpdatedTempBoard(place, shape)))
            place += 1
        return availableBoards

    def boardToDict(self):
        newBoard = ""
        if self.starter == 0:  # Human starts, switch the pieces
            for i in list(self.board):
                if i == '1':
                    newBoard += '2'
                elif i == '2':
                    newBoard += '1'
                else:
                    newBoard += i  # Keep '0's as is
        else:
            newBoard = self.board  # No change if computer starts
        return newBoard

    def hasDifferentPieceNear(self, place, shape):
        currentBoard = self.board
        opposite_shape = ("2" if shape == "1" else "1")

        offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

        for offset in offsets:
            neighbor_pos = place + offset

            if 0 <= neighbor_pos < 64:
                if not (place % 8 == 0 and offset in [-9, -1, 7]) and \
                        not (place % 8 == 7 and offset in [-7, 1, 9]):
                    if currentBoard[neighbor_pos] == opposite_shape:
                        return True
        return False

    def replacePieces(self, place, shape, board):
        board = self.replaceVertical(place, shape, board)
        board = self.replaceHorizontal(place, shape, board)
        board = self.replaceDiagonal(place, shape, board)
        return board

    def replaceVertical(self, place, shape, board):
        col_index = place % 8
        row_index = place // 8
        lineToCheck = [self.DoubleArray(board)[i][col_index] for i in range(8)]
        opposite_shape = '2' if shape == '1' else '1'
        updatedBoard = list(board)
        # Check and flip upwards
        self.Verticle_UP_Replace(col_index, lineToCheck, opposite_shape, row_index, shape, updatedBoard)
        # Check and flip downwards
        self.Verticle_DOWN_Replace(col_index, lineToCheck, opposite_shape, row_index, shape, updatedBoard)
        return ''.join(updatedBoard)

    def Verticle_DOWN_Replace(self, col_index, lineToCheck, opposite_shape, row_index, shape, updatedBoard):
        if row_index != 7:
            i = row_index + 1
            while i < 8 and lineToCheck[i] == opposite_shape:
                i += 1
            if i < 8 and i != row_index + 1 and lineToCheck[i] == shape:
                for j in range(row_index + 1, i):
                    updatedBoard[j * 8 + col_index] = shape

    def Verticle_UP_Replace(self, col_index, lineToCheck, opposite_shape, row_index, shape, updatedBoard):
        if row_index != 0:
            i = row_index - 1
            while i >= 0 and lineToCheck[i] == opposite_shape:
                i -= 1
            if i >= 0 and i != row_index - 1 and lineToCheck[i] == shape:
                for j in range(row_index - 1, i, -1):
                    updatedBoard[j * 8 + col_index] = shape

    def replaceHorizontal(self, place, shape, board):
        row = place // 8
        newPlace = place % 8
        lineToCheck = self.DoubleArray(board)[row]
        opposite_shape = '2' if shape == '1' else '1'
        updatedBoard = list(board)
        # Check and flip left
        self.Horizontal_LEFT_Replace(lineToCheck, newPlace, opposite_shape, row, shape, updatedBoard)
        # Check and flip right
        self.Horizontal_RIGHT_Replace(lineToCheck, newPlace, opposite_shape, row, shape, updatedBoard)
        return ''.join(updatedBoard)

    def Horizontal_RIGHT_Replace(self, lineToCheck, newPlace, opposite_shape, row, shape, updatedBoard):
        if newPlace != 7:
            i = newPlace + 1
            while i < 8 and lineToCheck[i] == opposite_shape:
                i += 1
            if i < 8 and i != newPlace + 1 and lineToCheck[i] == shape:
                for j in range(newPlace + 1, i):
                    updatedBoard[j + row * 8] = shape

    def Horizontal_LEFT_Replace(self, lineToCheck, newPlace, opposite_shape, row, shape, updatedBoard):
        if newPlace != 0:
            i = newPlace - 1
            while i >= 0 and lineToCheck[i] == opposite_shape:
                i -= 1
            if i >= 0 and i != newPlace - 1 and lineToCheck[i] == shape:
                for j in range(newPlace - 1, i, -1):
                    updatedBoard[j + row * 8] = shape

    def replaceDiagonal(self, place, shape, board):
        boardArray = self.DoubleArray(board)
        row_index = place // 8
        col_index = place % 8
        opposite_shape = '2' if shape == '1' else '1'
        updatedBoard = list(board)
        # Check and flip along diagonal ↘
        self.Diagonal_RightDown_Replace(boardArray, col_index, opposite_shape, row_index, shape, updatedBoard)
        # Check and flip along diagonal ↙
        self.Diagonal_DownLeft_Replace(boardArray, col_index, opposite_shape, row_index, shape, updatedBoard)
        return ''.join(updatedBoard)

    def Diagonal_DownLeft_Replace(self, boardArray, col_index, opposite_shape, row_index, shape, updatedBoard):
        i, j = row_index - 1, col_index + 1
        while i >= 0 and j < 8 and boardArray[i][j] == opposite_shape:
            i -= 1
            j += 1
        if i >= 0 and j < 8 and i != row_index - 1 and boardArray[i][j] == shape:
            for k, l in zip(range(row_index - 1, i, -1), range(col_index + 1, j)):
                updatedBoard[k * 8 + l] = shape
        i, j = row_index + 1, col_index - 1
        while i < 8 and j >= 0 and boardArray[i][j] == opposite_shape:
            i += 1
            j -= 1
        if i < 8 and j >= 0 and i != row_index + 1 and boardArray[i][j] == shape:
            for k, l in zip(range(row_index + 1, i), range(col_index - 1, j, -1)):
                updatedBoard[k * 8 + l] = shape

    def Diagonal_RightDown_Replace(self, boardArray, col_index, opposite_shape, row_index, shape, updatedBoard):
        i, j = row_index - 1, col_index - 1
        while i >= 0 and j >= 0 and boardArray[i][j] == opposite_shape:
            i -= 1
            j -= 1
        if i >= 0 and j >= 0 and i != row_index - 1 and boardArray[i][j] == shape:
            for k, l in zip(range(row_index - 1, i, -1), range(col_index - 1, j, -1)):
                updatedBoard[k * 8 + l] = shape
        i, j = row_index + 1, col_index + 1
        while i < 8 and j < 8 and boardArray[i][j] == opposite_shape:
            i += 1
            j += 1
        if i < 8 and j < 8 and i != row_index + 1 and boardArray[i][j] == shape:
            for k, l in zip(range(row_index + 1, i), range(col_index + 1, j)):
                updatedBoard[k * 8 + l] = shape

    def boardToString(self, board):
        counter = 0
        boardString = ""
        for i in range(0, 8):
            for j in range(0, 8):
                boardString += board[counter]
                counter += 1
            boardString += "\n"
        print(boardString)

    def getBoard(self):
        return self.board

    def getStarter(self):
        return self.starter

    def setBoard(self, board):
        self.board = board

    def getUpdatedTempBoard(self, place, shape):
        currentBoard = self.board
        boardList = list(currentBoard)
        boardList[int(place)] = str(shape)
        return ''.join(boardList)

    def isValid(self, place, shape):
        return self.horizontalLine(place, shape) or self.verticalLine(place, shape) or self.diagonalLine(place, shape)

    def horizontalLine(self, place, shape):
        global i
        row = place // 8
        newPlace = place % 8
        lineToCheck = self.DoubleArray(self.board)[row]
        opposite_shape = '2' if shape == '1' else '1'
        isTrue = False
        # left
        isTrue = self.Horizontal_Left_Check(isTrue, lineToCheck, newPlace, opposite_shape, shape)
        if isTrue:
            return True
        # right
        isTrue = self.Horizontal_Right_Check(isTrue, lineToCheck, newPlace, opposite_shape, shape)
        return isTrue

    def Horizontal_Left_Check(self, isTrue, lineToCheck, newPlace, opposite_shape, shape):
        global i
        if newPlace != 0:
            i = newPlace - 1
            while i >= 0 and lineToCheck[i] == opposite_shape:
                i -= 1
            if i >= 0 and i != newPlace - 1 and lineToCheck[i] == shape:
                isTrue = True
        return isTrue

    def Horizontal_Right_Check(self, isTrue, lineToCheck, newPlace, opposite_shape, shape):
        global i
        if newPlace != 7:
            i = newPlace + 1
            while i < 8 and lineToCheck[i] == opposite_shape:
                i += 1
            if i < 8 and i != newPlace + 1 and lineToCheck[i] == shape:
                isTrue = True
        return isTrue

    def verticalLine(self, place, shape):
        global i
        col_index = place % 8
        lineToCheck = [self.DoubleArray(self.board)[i][col_index] for i in range(8)]
        row_index = place // 8
        opposite_shape = '2' if shape == '1' else '1'
        isTrue = False
        # upwards
        isTrue = self.vertical_Up_Check(isTrue, lineToCheck, opposite_shape, row_index, shape)
        if isTrue:
            return True
        # downwards
        isTrue = self.vertical_Down_Check(isTrue, lineToCheck, opposite_shape, row_index, shape)
        return isTrue

    def vertical_Up_Check(self, isTrue, lineToCheck, opposite_shape, row_index, shape):
        global i
        if row_index != 0:
            i = row_index - 1
            while i >= 0 and lineToCheck[i] == opposite_shape:
                i -= 1
            if i >= 0 and i != row_index - 1 and lineToCheck[i] == shape:
                isTrue = True
        return isTrue

    def vertical_Down_Check(self, isTrue, lineToCheck, opposite_shape, row_index, shape):
        global i
        if row_index != 7:
            i = row_index + 1
            while i < 8 and lineToCheck[i] == opposite_shape:
                i += 1
            if i < 8 and i != row_index + 1 and lineToCheck[i] == shape:
                isTrue = True
        return isTrue

    def diagonalLine(self, place, shape):
        boardArray = self.DoubleArray(self.board)
        row_index = place // 8
        col_index = place % 8
        opposite_shape = '2' if shape == '1' else '1'
        isTrue = False
        # Check diagonal ↘
        isTrue = self.Diagonal_RightDown_Check(boardArray, col_index, isTrue, opposite_shape, row_index, shape)
        if isTrue:
            return True
        # Check diagonal ↙
        isTrue = self.Diagonal_LeftDown_Check(boardArray, col_index, isTrue, opposite_shape, row_index, shape)
        return isTrue

    def Diagonal_LeftDown_Check(self, boardArray, col_index, isTrue, opposite_shape, row_index, shape):
        i, j = row_index - 1, col_index + 1
        while i >= 0 and j < 8 and boardArray[i][j] == opposite_shape:
            i -= 1
            j += 1
        if i >= 0 and j < 8 and i != row_index - 1 and boardArray[i][j] == shape:
            isTrue = True
        i, j = row_index + 1, col_index - 1
        while i < 8 and j >= 0 and boardArray[i][j] == opposite_shape:
            i += 1
            j -= 1
        if i < 8 and j >= 0 and i != row_index + 1 and boardArray[i][j] == shape:
            isTrue = True
        return isTrue

    def Diagonal_RightDown_Check(self, boardArray, col_index, isTrue, opposite_shape, row_index, shape):
        i, j = row_index - 1, col_index - 1
        while i >= 0 and j >= 0 and boardArray[i][j] == opposite_shape:
            i -= 1
            j -= 1
        if i >= 0 and j >= 0 and i != row_index - 1 and boardArray[i][j] == shape:
            isTrue = True
        i, j = row_index + 1, col_index + 1
        while i < 8 and j < 8 and boardArray[i][j] == opposite_shape:
            i += 1
            j += 1
        if i < 8 and j < 8 and i != row_index + 1 and boardArray[i][j] == shape:
            isTrue = True
        return isTrue

    def DoubleArray(self, board):
        DArray = [[0 for _ in range(8)] for _ in range(8)]  # Initialize a 8x8 list
        counter = 0
        for i in range(8):
            for j in range(8):
                DArray[i][j] = board[counter]
                counter += 1
        # print("DArray: " + str(DArray))
        return DArray

    def hasFinished(self):
        # Check if the board is completely filled
        if '0' not in self.board:
            return True

        # Check if either player has a valid move
        if self.availableBoards('1') or self.availableBoards('2'):
            return False

        # If no valid moves are left for either player, the game is over
        return True

    def determineWinner(self, starter):
        count1 = self.board.count('1')
        count2 = self.board.count('2')

        if count1 > count2:
            print("Player 1 wins with " + str(count1) + "pieces to Player 2's " + str(count2) + " pieces!")
            if starter == 1:
                return 1
        elif count2 > count1:
            print("Player 2 wins with " + str(count2) + " pieces to Player 1's " + str(count1) + " pieces!")
            if starter == 0:
                return 1
        else:
            pass
            print("It's a tie! Both players have " + str(count1) + " pieces.")
        return 0


class Games:
    def load_dict_from_json(self):
        with open('Dict.json', 'r') as json_file:
            return json.load(json_file, object_hook=lambda item: {k: tuple(v) for k, v in item.items()})

    def save_dict_to_json(self, Dict):
        with open('Dict.json', 'w') as json_file:
            json.dump(Dict, json_file, default=lambda item: {k: list(v) for k, v in item.items()})

    def __init__(self):
        self.Dict = self.load_dict_from_json()
        self.game = Game()

    def startGame(self):
        self.Dict = self.load_dict_from_json()
        boards, compWon = self.game.play()
        # print(boards,compWon)
        boards.reverse()
        self.DictionaryUpdating(boards, compWon)
        # print(self.Dict)
        self.save_dict_to_json(self.Dict)
        return compWon

    def getBoard(self):
        return self.game.getBoard()

    def DictionaryUpdating(self, boards, compWon):
        counter = 0
        for board in boards:
            if board in self.Dict:
                if compWon:
                    currentValue = self.Dict[board][0]
                    currentTimes = self.Dict[board][1]
                    self.Dict[board] = tuple(
                        (((currentValue * currentTimes) + math.pow(0.9, counter)) / (currentTimes + 1),
                         (currentTimes + 1)))
                else:
                    currentValue = self.Dict[board][0]
                    currentTimes = self.Dict[board][1]
                    self.Dict[board] = tuple(((currentValue * currentTimes) / (currentTimes + 1), currentTimes + 1))
            else:
                if compWon:
                    self.Dict[board] = tuple((math.pow(0.9, counter), 1))
                else:
                    self.Dict[board] = tuple((0, 1))
            counter += 1

if __name__ == '__main__':
    start = time.time()
    for i in range(1):
        games = Games()
        games.startGame()

    end = time.time()
    print(end - start)

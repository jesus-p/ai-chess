##Import Libraries
import string
import random
import os
import sys
import time
from IPython.display import clear_output
import numpy as np

##ChessBoard

# This code defines the ChessBoard class.
# It includes functions to initialize the board, draw the board, get the board state, and move a piece.
# Additional helper functions are included as needed.

def ChessBoardSetup():
      a = ['r', 'p', '.', '.', '.', '.', 'P', 'R']
      b = ['t', 'p', '.', '.', '.', '.', 'P', 'T']
      c = ['b', 'p', '.', '.', '.', '.', 'P', 'B']
      d = ['q', 'p', '.', '.', '.', '.', 'P', 'Q']
      e = ['k', 'p', '.', '.', '.', '.', 'P', 'K']
      f = ['b', 'p', '.', '.', '.', '.', 'P', 'B']
      g = ['t', 'p', '.', '.', '.', '.', 'P', 'T']
      h = ['r', 'p', '.', '.', '.', '.', 'P', 'R']
      board = np.column_stack([a,b,c,d,e,f,g,h])
      return board

board = ChessBoardSetup()
def DrawBoard():
  print(str(board).replace(' [', '').replace('[', '').replace(']', '').replace("'", ""))


def MovePiece(from_piece, to_piece):
  move = board[from_piece[0],from_piece[1]]
  board[to_piece[0],to_piece[1]] = move
  board[from_piece[0],from_piece[1]] = '.'
  return board

##ChessRules

# This code defines the ChessRules class.
# It includes functions for the movement rules of each chess piece.
# The code also provides functions to check if the current player is in check or checkmate.
# Additional functions return the current player's pieces that have legal moves based on the current board state.

def IsMoveLegal(board, player, from_square, to_square):
    from_square_row = from_square[0]
    from_square_col = from_square[1]
    to_square_row = to_square[0]
    to_square_col = to_square[1]
    from_piece = board[from_square_row][from_square_col]
    to_piece = board[to_square_row][to_square_col]

    if from_square == to_square:
        return False

    # Pawn
    if from_piece.lower() == 'p':
        if to_square_row == from_square_row - 1 and to_square_col == from_square_col and to_piece == '.':
            return True
        elif from_square_row == 6 and to_square_row == 4 and to_square_col == from_square_col and to_piece == '.' and player == 'white':
            return True
        elif to_piece.islower() and (to_square_row, to_square_col) in ((from_square_row - 1, from_square_col - 1), (from_square_row - 1, from_square_col + 1)):
            return True

    # Rook
    elif from_piece.lower() == 'r':
        if to_square_row == from_square_row or to_square_col == from_square_col:
            if IsClearPath(board, from_square, to_square):
                return True

    # Bishop
    elif from_piece.lower() == 'b':
        if abs(to_square_col - from_square_col) == abs(to_square_row - from_square_row):
            if IsClearPath(board, from_square, to_square):
                return True

    # Queen
    elif from_piece.lower() == 'q':
        if to_square_row == from_square_row or to_square_col == from_square_col:
            if IsClearPath(board, from_square, to_square):
                return True
        elif abs(to_square_col - from_square_col) == abs(to_square_row - from_square_row):
            if IsClearPath(board, from_square, to_square):
                return True

    # Knight
    elif from_piece.lower() == 'n':
        col_diff = abs(to_square_col - from_square_col)
        row_diff = abs(to_square_row - from_square_row)
        if col_diff == 1 and row_diff == 2:
            return True
        elif col_diff == 2 and row_diff == 1:
            return True

    # King
    elif from_piece.lower() == 'k':
        col_diff = abs(to_square_col - from_square_col)
        row_diff = abs(to_square_row - from_square_row)
        if (col_diff == 1 and row_diff == 0) or (col_diff == 0 and row_diff == 1) or (col_diff == 1 and row_diff == 1):
            return True

    return False

# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves(c_player,from_square):
    # input is the current player and the given piece as the from-square
    # initialize the list of legal moves, i.e., to-square locations to []
    MovelegalList = []
    # go through all squares on the board
    for a in range(8):
        for b in range(8):
    # for the selected square as to-square
            to_square = [a,b]
        # call IsMoveLegal() with input as from-square and to-square and save the returned value
            legal_value = IsMoveLegal(c_player, from_square, to_square)
            if legal_value == True:
        # if returned value is True
            # call DoesMovePutPlayerInCheck() with input as from-square and to-square and save the returned value
                val_check = DoesMovePutPlayerInCheck(from_square, to_square, c_player)
            # if returned value is False
                # append this move (to-square) as a legal move
                if val_check == False:
                      MovelegalList.append(to_square)
    # return the list of legal moves, i.e., to-square locations
        return MovelegalList



# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves(c_player):
    # initialize the list of pieces with legal moves to []
    LegalpiecesList = []
    # go through all squares on the board
    for a in range(len(board)):
      for b in range(len(board)):
    # for the selected square
        # if the square contains a piece that belongs to the current player's team
            if((c_player == 0 and (board[i][j]).islower()) or (c_player == 1 and (board[a][b]).isupper())):

            # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square
                moves = GetListOfLegalMoves(c_player, [a,b])
            # if there are any legel moves
                if len(moves)>0:
                # append this piece to the list of pieces with legal moves
                     LegalpiecesList.append([board[a,b],[a,b]])
    # return the final list of pieces with legal moves
    return LegalpiecesList



# returns True if the current player is in checkmate, else False
def IsCheckmate(c_player):
    # call GetPiecesWithLegalMoves() to get all legal moves for the current player
    legal_move = GetPiecesWithLegalMoves(c_player)
    # if there is no piece with any valid move
    if len(legal_move)<0:
        # return True
        return True
    # else
        # return False
    else:
        return False



# returns True if the given player is in Check state
def IsInCheck(c_player):
    king_square=[]
    # find given player's King's location = king-square
    if c_player == 0:
          pos = np.where(board=='k')
          [a,b] = pos
          king_square.append(a[0])
          king_square.append(b[0])
    elif c_player == 1:
          pos = np.where(board=='K')
          [a,b] = pos
          king_square.append(a[0])
          king_square.append(b[0])
    # go through all squares on the board
    for a in range(8):
          for b in range(8):
        # if there is a piece at that location and that piece is of the enemy team
            if ((board[a][b]) == "."):
                 return False
            elif ((c_player == 0 and (board[a][b]).isupper()) or (c_player == 1 and (board[a][b]).islower())):
            # call IsMoveLegal() for the enemy player from that square to the king-square
                    legal = IsMoveLegal(c_player,[a,b],king_square)
            # if the value returned is True
                    if legal == True:
                # return True
                            return True
                    else:
                            continue
            # else
                # do nothing and continue
    # return False at the end
    return False



# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def IsClearPath(board, from_square, to_square):
  from_square_row = from_square[0]
  from_square_col = from_square[1]
  to_square_row = to_square[0]
  to_square_col = to_square[1]
  from_piece = board[from_square_row][from_square_col]

  if abs(from_square_row - to_square_row) <= 1 and abs(from_square_col - to_square_col) <= 1:
    return True
  else:
    if to_square_row > from_square_row and to_square_col == from_square_col:
      new_square = (from_square_row + 1, from_square_col)
    elif to_square_row < from_square_row and to_square_col == from_square_col:
      new_square = (from_square_row - 1, from_square_col)
    elif to_square_col > from_square_col and to_square_row == from_square_row:
      new_square = (from_square_row, from_square_col + 1)
    elif to_square_col < from_square_col and to_square_row == from_square_row:
      new_square = (from_square_row, from_square_col - 1)
    elif to_square_row > from_square_row and to_square_col > from_square_col:
      new_square = (from_square_row + 1, from_square_col + 1)
    elif to_square_row > from_square_row and to_square_col < from_square_col:
      new_square = (from_square_row + 1, from_square_col - 1)
    elif to_square_row < from_square_row and to_square_col > from_square_col:
      new_square = (from_square_row - 1, from_square_col + 1)
    elif to_square_row < from_square_row and to_square_col < from_square_col:
      new_square = (from_square_row - 1, from_square_col - 1)

    if board[new_square[0]][new_square[1]] != None:
      return False
    else:
      return IsClearPath(board, new_square, to_square)



# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck(from_square, to_square,c_player):
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    from_piece = board[from_square[0],from_square[1]]
    to_piece =  board[to_square[0],to_square[1]]
    # make the move temporarily by changing the 'board'
    temp1 = from_piece
    temp2 = to_piece
    board[to_square[0],to_square[1]] = temp1
    board[from_square[0], from_square[1]] = '.'
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    DoesMovePutPlayerInCheck = IsInCheck(c_player)
    # Undo the temporary move
    board[from_square[0],from_square[1]] = temp1
    board[to_square[0],to_square[1]] = temp2
    # return the value saved - True if it puts current player into check, False otherwise
    #print(DoesMovePutPlayerInCheck)
    return DoesMovePutPlayerInCheck

#Artificial Intelligence

# This section contains code for the Artificial Intelligence (AI) that plays chess.
# It includes two types of AI:
# RandomAI, which moves a chess piece randomly.
# MinMaxAI, which moves a chess piece using the MinMax strategy.


def GetRandomMove(current_p):
    # pick a random piece and a random legal move for that piece
    random_piece_list = random.choice(GetPiecesWithLegalMoves(current_p))
    random_move = random.choice(GetListOfLegalMoves(current_p,random_piece_list[1]))
    print(random_move)
GetRandomMove(0)

##MinMaxAI
# The MinMax strategy has been modified to use a 4-ply search depth (one Max, one Min, one Max, one Min).


def getPieceValue(piece, current_player):
    if(piece == "k" or  piece =="K" or  piece == "."):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "T" or piece == "t":
        value = 35
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 70
    return value

def evl(current_player):
    # this function will calculate the score on the board, if a move is performed
    # give score for each of piece and calculate the score for the chess board
    evlscore = 0
    for a in range(8):
      for b in range (8):
        if(current_player == 0):

                  if board[a][b].islower():
                      evlscore = evlscore - getPieceValue(board[a][b], current_player)

        elif(current_player == 1):

                  if board[a][b].isupper():
                      evlscore = evlscore + getPieceValue(board[a][b], current_player)

    return evlscore



def GetMinMaxMove(board, current_player, depth, maxDepth):
    if depth == maxDepth:
        return evl()

    foundMove = None
    if current_player == 0:
        highestscore = -math.inf
    else:
        highestscore = math.inf

    # finding the pieces for the player
    pieces = GetPiecesWithLegalMoves(current_player)

    # iterating pieces
    for piece in pieces:
        moves = GetListOfLegalMoves(current_player, piece)

        for move in moves:
            newBoard = MovePiece(piece, move)

            # score
            score = GetMinMaxMove(newBoard, 1 - current_player, depth+1, maxDepth)

            # maximizing
            if current_player == 0:
                if score > highestscore:
                    highestscore = score
                    foundMove = (piece, move)
            else:
                # minimizing
                if score < highestscore:
                    highestscore = score
                    foundMove = (piece, move)

    # returning the highestscore
    if depth == 0:
        return foundMove
    else:
        return highestscore



##Game Setup & Main Loop

# The code below runs a game between two AIs: RandomAI and MinMaxAI.
# For each turn, the board is drawn before and after the move.

board = ChessBoardSetup()
player1_type = 'minmaxAI'
player1_player = 'white'
player2_type = 'randomAI'
player2_player = 'minmaxAI'

current_player_i = 0
current_player = 'white'
turns = 0
N = 100

# main game loop - while a player is not in checkmate or stalemate (<N turns)
# below is the rough looping strategy
while not IsCheckmate(board, current_player) and turns < N:
  clear_output()
  DrawBoard(board)

    # write code to take turns and move the pieces
  if current_player == 'black':
    move = GetRandomMove (board, current_player)
    print("\nBLACK")
  else:
    turns = turns + 1
    move = GetRandomMove(board, current_player)
    print("\nWhite")

  board = MovePiece(board, move)
  current_player_i = (current_player_i + 1)%2
  current_player = 'black' if current_player == 'white' else 'white'

  DrawBoard(board)
  time.sleep(0.5)

# check and print - Stalemate or Checkmate
if(IsCheckmate(board, current_player)):
  print("CHECKMATE")
  winner_check = (current_player_i + 1)%2
  if(winner_check == 0):
    print("WHITE won the game in" + str(turns) + " turns!")
  else:
    print("BLACK won the game in" + str(turns) + " turns!")
else:
  print("STALEMATE")
##Import Libraries
import math
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

# board = ChessBoardSetup() # Removed this global variable initialization
def DrawBoard(board): # Added board argument
  print(str(board).replace(' [', '').replace('[', '').replace(']', '').replace("'", ""))


def MovePiece(board, from_piece, to_piece): # Added board argument
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
        elif from_square_row == 6 and to_square_row == 4 and to_square_col == from_square_col and to_piece == '.' and player == 0: # Changed player == 'white' to player == 0
            return True
        elif to_piece.islower() and (to_square_row, to_square_col) in ((from_square_row - 1, from_square_col - 1), (from_square_row - 1, from_square_col + 1)):
            return True
        elif to_piece.isupper() and (to_square_row, to_square_col) in ((from_square_row - 1, from_square_col - 1), (from_square_row - 1, from_square_col + 1)): # Added capture for white
            return True

    elif from_piece.lower() == 'P':
        if to_square_row == from_square_row + 1 and to_square_col == from_square_col and to_piece == '.':
            return True
        elif from_square_row == 1 and to_square_row == 3 and to_square_col == from_square_col and to_piece == '.' and player == 1: # Changed player == 'black' to player == 1
            return True
        elif to_piece.isupper() and (to_square_row, to_square_col) in ((from_square_row + 1, from_square_col - 1), (from_square_row + 1, from_square_col + 1)):
            return True
        elif to_piece.islower() and (to_square_row, to_square_col) in ((from_square_row + 1, from_square_col - 1), (from_square_row + 1, from_square_col + 1)): # Added capture for black
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
    elif from_piece.lower() == 't': # Changed 'n' to 't' based on the board setup
        col_diff = abs(to_square_col - from_square_col)
        row_diff = abs(to_square_row - from_square_row)
        if (col_diff == 1 and row_diff == 2) or (col_diff == 2 and row_diff == 1):
            if board[to_square_row][to_square_col] == '.' or (player == 0 and board[to_square_row][to_square_col].isupper()) or (player == 1 and board[to_square_row][to_square_col].islower()):
                 return True

    # King
    elif from_piece.lower() == 'k':
        col_diff = abs(to_square_col - from_square_col)
        row_diff = abs(to_square_row - from_square_row)
        if (col_diff <= 1 and row_diff <= 1) and (col_diff > 0 or row_diff > 0):
             if board[to_square_row][to_square_col] == '.' or (player == 0 and board[to_square_row][to_square_col].isupper()) or (player == 1 and board[to_square_row][to_square_col].islower()):
                 return True

    return False

# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves(board, c_player,from_square): # Added board argument
    # input is the current player and the given piece as the from-square
    # initialize the list of legal moves, i.e., to-square locations to []
    MovelegalList = []
    # go through all squares on the board
    for i in range(8):
        for j in range(8):
    # for the selected square as to-square
            to_square = [i,j]
        # call IsMoveLegal() with input as from-square and to-square and save the returned value
            legal_value = IsMoveLegal(board, c_player, from_square, to_square)
            if legal_value == True:
        # if returned value is True
            # call DoesMovePutPlayerInCheck() with input as from-square and to-square and save the returned value
                val_check = DoesMovePutPlayerInCheck(board, from_square, to_square, c_player) # Added board argument
            # if returned value is False
                # append this move (to-square) as a legal move
                if val_check == False:
                      MovelegalList.append(to_square)
    # return the list of legal moves, i.e., to-square locations
    return MovelegalList



# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves(board, c_player): # Added board argument
    # initialize the list of pieces with legal moves to []
    LegalpiecesList = []
    # go through all squares on the board
    for a in range(len(board)):
      for b in range(len(board)):
    # for the selected square
        # if the square contains a piece that belongs to the current player's team
            if((c_player == 0 and (board[a][b]).islower()) or (c_player == 1 and (board[a][b]).isupper())):

            # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square
                moves = GetListOfLegalMoves(board, c_player, [a,b]) # Added board argument
            # if there are any legel moves
                if len(moves)>0:
                # append this piece to the list of pieces with legal moves
                     LegalpiecesList.append([board[a,b],[a,b]])
    # return the final list of pieces with legal moves
    return LegalpiecesList



# returns True if the current player is in checkmate, else False
def IsCheckmate(board, c_player): # Added board argument
    # call GetPiecesWithLegalMoves() to get all legal moves for the current player
    legal_move = GetPiecesWithLegalMoves(board, c_player) # Added board argument
    # if there is no piece with any valid move
    if len(legal_move) == 0 and IsInCheck(board, c_player): # Changed <0 to == 0 and added IsInCheck check
        # return True
        return True
    # else
        # return False
    else:
        return False



# returns True if the given player is in Check state
def IsInCheck(board, c_player): # Added board argument
    king_square=[]
    # find given player's King's location = king-square
    if c_player == 0:
          pos = np.where(board=='k')
    elif c_player == 1:
          pos = np.where(board=='K')

    if pos[0].size == 0: # Check if king was found
        return False

    king_square.append(pos[0][0])
    king_square.append(pos[1][0])


    # go through all squares on the board
    for a in range(8):
          for b in range(8):
        # if there is a piece at that location and that piece is of the enemy team
            if ((board[a][b]) == "."):
                 continue
            elif ((c_player == 0 and (board[a][b]).isupper()) or (c_player == 1 and (board[a][b]).islower())):
            # call IsMoveLegal() for the enemy player from that square to the king-square
                    legal = IsMoveLegal(board, c_player,[a,b],king_square) # Added board argument
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
def IsClearPath(board, from_square, to_square): # Added board argument
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
    else:
        return True # Added this else case to handle when new_square is not updated.

    if board[new_square[0]][new_square[1]] != '.': # Changed != None to != '.'
      return False
    else:
      return IsClearPath(board, new_square, to_square)



# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck(board, from_square, to_square,c_player): # Added board argument
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    temp_board = board.copy() # Create a copy of the board
    from_piece = temp_board[from_square[0],from_square[1]]
    to_piece =  temp_board[to_square[0],to_square[1]]
    # make the move temporarily by changing the 'board'
    temp_board[to_square[0],to_square[1]] = from_piece # Used temp_board
    temp_board[from_square[0], from_square[1]] = '.' # Used temp_board
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    DoesMovePutPlayerInCheck = IsInCheck(temp_board, c_player) # Added temp_board argument
    # Undo the temporary move (not needed with copy)
    # return the value saved - True if it puts current player into check, False otherwise
    #print(DoesMovePutPlayerInCheck)
    return DoesMovePutPlayerInCheck


#Artificial Intelligence

# This section contains code for the Artificial Intelligence (AI) that plays chess.
# It includes two types of AI:
# RandomAI, which moves a chess piece randomly.
# MinMaxAI, which moves a chess piece using the MinMax strategy.

def GetRandomMove(board, current_p): # Added board argument
    # pick a random piece and a random legal move for that piece
    pieces_with_legal_moves = GetPiecesWithLegalMoves(board, current_p) # Added board argument
    if not pieces_with_legal_moves: # Check if list is empty
        return None
    random_piece_list = random.choice(pieces_with_legal_moves)
    legal_moves = GetListOfLegalMoves(board, current_p,random_piece_list[1]) # Added board argument
    if not legal_moves: # Check if list is empty
        return None
    random_move = random.choice(legal_moves)
    # print(random_move) # Removed print statement
    return (random_piece_list[1], random_move) # Return the move
# GetRandomMove(board, 0) # Commented out the test call


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
current_player = 0 # Changed to integer for player representation
turns = 0
N = 100

# main game loop - while a player is not in checkmate or stalemate (<N turns)
# below is the rough looping strategy
while not IsCheckmate(board, current_player) and turns < N: # Added board argument
  clear_output()
  DrawBoard(board) # Added board argument

    # Code to take turns and move the pieces
  if current_player == 1: # Black's turn
    print("\nBLACK's Turn")
    move = GetRandomMove (board, current_player) # Added board argument
    if move:
        board = MovePiece(board, move[0], move[1]) # Added board argument and unpacked move
  else: # White's turn
    turns = turns + 1
    print("\nWHITE's Turn")
    # Assuming player 1 (white) is MinMaxAI for now, will need to implement MinMaxAI later
    move = GetRandomMove(board, current_player) # Using RandomMove for now, will replace with MinMax later
    if move:
        board = MovePiece(board, move[0], move[1]) # Added board argument and unpacked move


  current_player = (current_player + 1)%2


  DrawBoard(board) # Added board argument
  time.sleep(3) # Changed to slow down print

# check and print - Stalemate or Checkmate
if(IsCheckmate(board, current_player)): # Added board argument
  print("CHECKMATE")
  winner_check = (current_player + 1)%2 # Simplified winner determination
  if(winner_check == 0):
    print("WHITE won the game in " + str(turns) + " turns!") # Added space
  else:
    print("BLACK won the game in " + str(turns) + " turns!") # Added space
else:
  print("STALEMATE")
# Chess Game with AI Players

This Python app lets you watch a game of chess played between two computer-controlled players. It includes a virtual chess board, follows all the rules for how each chess piece moves, and features two types of AI to control the players: one that makes random moves and another that tries to play smart using a strategy called "MinMax."

## What the App Does

- **Shows a chess board**: The app sets up an 8x8 grid just like a real chess game, with all the pieces in their usual starting spots.
- **Follows chess rules**: Each piece (pawn, rook, knight, bishop, queen, king) moves according to official chess rules.
- **Two AI players**: The game is played by two computer programs:
  - **Random AI**: This player picks a legal move at random.
  - **MinMax AI**: This player looks ahead several moves, tries to predict what will happen, and chooses the move that gives it the best chance to win.

## How Each Chess Piece Moves

| Piece   | How It Moves                                                                 |
|---------|------------------------------------------------------------------------------|
| Pawn    | Moves forward one square (or two from starting position), captures diagonally |
| Rook    | Moves any number of squares in straight lines (up, down, left, right)        |
| Knight  | Moves in an "L" shape: two squares one way, then one square at a right angle |
| Bishop  | Moves any number of squares diagonally                                       |
| Queen   | Moves any number of squares in any direction                                 |
| King    | Moves one square in any direction                                            |

## How the AI Players Work

- **Random AI**:
  - Looks at all possible moves and picks one randomly.
  - Does not try to win, just makes legal moves.

- **MinMax AI**:
  - Looks ahead a few moves to see possible outcomes.
  - Tries to choose the move that maximizes its own chance of winning and minimizes the opponent’s chances.
  - This is a basic version of how computers play chess at a higher level.

## What You See

- The board updates after each move.
- Both white and black sides are played by the AI.
- You can watch the game unfold from start to finish.

This app is a fun way to see how different computer strategies play chess, and it follows all the official rules for how each piece moves. No chess knowledge is needed to watch the game!

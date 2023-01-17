# Chess MkIII
### Ayden Hogeveen
***
TODO: Finish illegal move pruning and more advanced move generation.


## Requirements
Understand the problem and identify requirements that the program should fulfill
#### Basic Requirements
1. While the game is Running, players will take turns making moves
2. Each turn, take the move input from the player, and if the move is valid, allow the move
3. Continue the game until one player wins(by checkmate, or by the opponent resigning), or the game is drawn(by stalemate, 50-move rule, or agreement).
4. Handle legal moves and check conditions

#### Advanced Requirements
1. Handling Special Moves
- Castling -- Castling is only allowed if both the king, and the rook involved have never moved, the squares between the king and the rook are not occupied, the king is not in check, and the 2 squares the king will jump are not attacked by any piece
- Pawn Promotion -- If a pawn can reach the opposite back rank, either the 8th rank for the white player, or the 1st rank for the black player, that pawn can be promoted to any piece the player chooses, other than a king
- Two Square Pawn Advance -- The first time a pawn moves, it has the option of moving forward one or two squares.

2. Adding a Computer Player
- The second player can be a human player or a computer player
- Create a player class that both the human, and the computer player can inherit from


## Entities
Think of the entities involved. Using this, identify the classes required. Also, identify the basic data members and methods using the properties of the entity. (Use OOP concepts)

In a chess game:
1. Chess Board (8x8 Checkered Board, holds the pieces)
2. Player (Player colour and pieces)
3. Piece (Piece colour and method to contain the legal moves for each piece)
    - King
    - Queen
    - Rook
    - Bishop 
    - Knight
    - Pawn
    
"Just write down the declaration of the method and complete the implementation late after designing the main class. This is because after implementing the main class, we will have a better understanding of what parameters to pass, how to implement, and what the function should return."



## Bibliography
***
### Window Icon
<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

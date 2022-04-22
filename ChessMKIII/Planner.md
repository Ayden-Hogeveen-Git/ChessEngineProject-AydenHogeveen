# Chess MkIII
### Ayden Hogeveen


TODO: Add piece movement -- Drag and Drop
* When the user clicks and holds on a piece, draw that piece at the current mouse position, until the mouse is released, then move the piece to the square where the mouse was let go, if the piece can legally move there
* WHILE the mouse is held "pick up" the piece
  * Draw the piece at the current mouse position
  * IF the user releases the mouse, and the piece can move to the square, draw the piece at the square where the mouse was let go, and update the gamestate in the engine
  * ELSE IF the mouse is released and the piece cannot move to the square, redraw the piece at its original position
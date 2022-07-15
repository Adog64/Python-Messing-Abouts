"Wave Function" Collapse Sudoku Solver

By: Aidan Sharpe

The concept originates from the wave function collapse procedural
generation algorithm: https://github.com/mxgmn/WaveFunctionCollapse

When a preset sudoku board is input to the console, all blank cells are
assumed to be in a superposition of all numbers (1-9).

A cell's "entropy" is defined as the number of possible states it represents.
For example: 
- A fully collpased cell has entropy 1
- A cell that can be a 3, 5, or 6 has entropy 3.

When a keydown event is triggered:
- Cells update by sudoku rules to reduce the number of possible states.
- If no cells can be updated by sudoku (the change in entropy is 0), 
  a cell of minimum entropy is chosen to collapse to a single state. 
  This causes new information to be put into the board allowing for more
  collapses by sudoku.

Once the total entropy of the system has reached 81, all cells have 
been reduced to a single state, and the puzzle is solved.
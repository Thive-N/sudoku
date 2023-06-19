def prettyprint(board: list[list[int]]) -> None:
    """Print a sudoku board"""
    print("+-------+-------+-------+")
    for row in range(9):
        print("|", end=" ")
        for column in range(9):
            if board[row][column] is None:
                print(" ", end=" ")
            else:
                print(board[row][column], end=" ")
            if (column+1) % 3 == 0:
                print("|", end=" ")
        print()
        if (row+1) % 3 == 0:
            print("+-------+-------+-------+")

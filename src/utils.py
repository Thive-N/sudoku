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


def exportboard(board: list[list[int]]) -> None:
    """Export a sudoku board to a string"""
    return "".join([str(board[row][column]) if board[row][column] is not None else "0" for row in range(9) for column in range(9)])


def importboard(board: str) -> list[list[int]]:
    """Import a sudoku board from a string"""
    return [[int(board[row*9+column]) if board[row*9+column] != "0" else None for column in range(9)] for row in range(9)]

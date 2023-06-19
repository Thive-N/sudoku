import validity
import utils
import random
import generate


def solve(board: list[list[int]]) -> list[list[int]]:
    """Solve a sudoku board.

    Args:
        board (list[list[int]]): The board to solve.

    Returns:
        list[list[int]]: The solved board.

    Note:
        Empty cells are represented by the Nonetype.
    """
    # if not validity.boardValid(board):
    #     raise ValueError("The board is invalid.")

    # emptycells = validity.getemptysquares(board)
    # if len(emptycells) == 0:
    #     return board

    return solveEasyCases(board)


def solveEasyCases(board: list[list[int]]) -> list[list[int]]:
    """Solve easy cases of a sudoku board.

    Args:
        board (list[list[int]]): The board to solve.

    Returns:
        list[list[int]]: The solved board.

    Note:
        Empty cells are represented by the Nonetype.
        boards are considered valid
    """
    complete = False
    while not complete:
        complete = True
        emptycells = validity.getemptysquares(board)
        for row, column in emptycells:
            valids = validity.validatposition(board, row, column)
            if len(valids) == 1:
                complete = False
                board[row][column] = valids[0]

    return board


if __name__ == "__main__":
    board = generate.generatepartial(percentageRemoved=0.5)
    utils.prettyprint(board)
    print()
    solved = solve(board)
    utils.prettyprint(solved)

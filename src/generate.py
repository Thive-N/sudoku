import random
import validity
import utils
import solver


def generatefull() -> list[list[int]]:
    """Generate a new sudoku board.

    Returns:
        list[list[int]]: The generated board.
    """
    board = [[None for _ in range(9)] for _ in range(9)]

    for row in range(9):
        for column in range(9):
            board = solver.solveEasyCases(board)
            if board[row][column] is None:
                valids = validity.validatposition(board, row, column)

                # if there is a cell with no valid values, the board is invalid so generate a new one

                if len(valids) == 0:
                    return generatefull()

                value = random.choice(valids)
                board[row][column] = value

    return board


def generatepartial(percentageRemoved: int = 0.8) -> list[list[int]]:
    """Generate a new sudoku board with some cells removed.

    Args:
        percentageRemoved (int, optional): The percentage of cells to remove. Defaults to 0.1.

    Returns:
        list[list[int]]: The generated board.
    """
    board = generatefull()
    cellsToRemove = min(70, int(81 * (1-percentageRemoved)))
    allcells = [(row, column) for row in range(9) for column in range(9)]
    random.shuffle(allcells)
    allcells = allcells[:cellsToRemove]

    for cell in allcells:
        board[cell[0]][cell[1]] = None

    return board


if __name__ == "__main__":
    board = generatefull()
    utils.prettyprint(board)

def boardValid(board: list[list[int]]) -> bool:
    """Check if the board is valid.

    Args:
        board (list[list[str]]): The board to check.

    Returns:
        bool: True if the board is valid, False otherwise.

    Note:
        Empty cells are represented by the Nonetype.
    """
    valid = True

    for row in board:
        filteredrow = list(filter(lambda x: x is not None, row))
        if len(filteredrow) != len(set(filteredrow)):
            valid = False

    for index in range(9):
        xs = [row[index] for row in board]
        filteredcolumn = list(filter(lambda x: x is not None, xs))
        if len(filteredcolumn) != len(set(filteredcolumn)):
            valid = False

    for row in range(3):
        for column in range(3):
            xs = [board[row*3+i][column*3+j]
                  for i in range(3) for j in range(3)]
            filteredbox = list(filter(lambda x: x is not None, xs))
            if len(filteredbox) != len(set(filteredbox)):
                valid = False

    return valid


def boardComplete(board: list[list[int]]) -> bool:
    """Check if the board is complete.

    Args:
        board (list[list[str]]): The board to check.

    Returns:
        bool: True if the board is complete, False otherwise.

    Note:
        Empty cells are represented by the Nonetype.
    """
    for row in board:
        if None in row:
            return False
    return True


def validatposition(board: list[list[int]], row: int, column: int) -> list[int]:
    """Return a list of valid values for the cell at the given position.

    Args:
        board (list[list[str]]): The board to check.
        row (int): The row of the cell to check.
        column (int): The column of the cell to check.

    Returns:
        list[int]: A list of valid values for the cell at the given position.

    Note:
        Empty cells are represented by the Nonetype.
    """
    valid = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if board[row][column] is not None:
        return []

    for index in range(9):
        if board[row][index] in valid:
            valid.remove(board[row][index])

        if board[index][column] in valid:
            valid.remove(board[index][column])

    boxrow = row - row % 3
    boxcolumn = column - column % 3
    for i in range(3):
        for j in range(3):
            if board[boxrow+i][boxcolumn+j] in valid:
                valid.remove(board[boxrow+i][boxcolumn+j])

    return valid


def validboardmove(board: list[list[int]], row: int, column: int, value: int) -> bool:
    """Check if the given move is valid.

    Args:
        board (list[list[str]]): The board to check.
        row (int): The row of the cell to check.
        column (int): The column of the cell to check.
        value (int): The value to check.

    Returns:
        bool: True if the move is valid, False otherwise.

    Note:
        Empty cells are represented by the Nonetype.
    """

    # less computationally expensive than checking if the board is valid after the move
    return value in validatposition(board, row, column)


def getemptysquares(board: list[list[int]]) -> list[tuple[int, int]]:
    sqs = []
    for row in range(9):
        for column in range(9):
            if board[row][column] == None:
                sqs.append((row, column))
    return sqs


def getAffectingSquares(board: list[list[int]], row: int, col: int) -> list[tuple[int, int]]:
    """Get the squares affected by the given square.

    Args:
        board (list[list[int]]): The board to check.
        row (int): The row of the cell to check.
        col (int): The column of the cell to check.

    Returns:
        list[tuple[int, int]]: A list of the squares affected by the given square.

    Note:
        Empty cells are represented by the Nonetype.
    """
    affected = []
    for i in range(9):
        if i != row:
            affected.append((i, col))
        if i != col:
            affected.append((row, i))

    boxrow = row - row % 3
    boxcolumn = col - col % 3
    for i in range(3):
        for j in range(3):
            if boxrow+i != row and boxcolumn+j != col:
                affected.append((boxrow+i, boxcolumn+j))

    return affected


def getAffectingSquaresBox(board: list[list[int]], row: int, col: int) -> list[tuple[int, int]]:
    affected = []
    boxrow = row - row % 3
    boxcolumn = col - col % 3
    for i in range(3):
        for j in range(3):
            if boxrow+i != row and boxcolumn+j != col:
                affected.append((boxrow+i, boxcolumn+j))

    return affected

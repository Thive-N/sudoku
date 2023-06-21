import validity
import utils
import random
import generate
import copy


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
    maxiterations = 10000
    previousboard = copy.deepcopy(board)
    savestate = None
    while True:
        maxiterations -= 1
        if maxiterations == 0:
            print("max iterations reached")
            break
        board = solveEasyCases(board)

        emptycells = validity.getemptysquares(board)
        if len(emptycells) == 0:
            break

        board = solveSingleCandidateCases(board)

        emptycells = validity.getemptysquares(board)
        if len(emptycells) == 0:
            break

        if maxiterations < 200:
            solveColorTrap(board)

        if previousboard == board:
            if savestate is None:
                savestate = copy.deepcopy(board)
            try:
                board = solveProbabilisticCases(board)
            except:
                board = copy.deepcopy(savestate)

        previousboard = copy.deepcopy(board)
    return board


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


def solveSingleCandidateCases(board: list[list[int]]) -> list[list[int]]:
    """Solve single candidate cases of a sudoku board.

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
            currentvalid = validity.validatposition(board, row, column)
            valids = validity.getAffectingSquares(board, row, column)
            for r, c in valids:
                validsatpos = validity.validatposition(board, r, c)
                currentvalid = [
                    x for x in currentvalid if x not in validsatpos]

            if len(currentvalid) == 1:
                complete = False
                board[row][column] = currentvalid[0]

    return board


def solveProbabilisticCases(board: list[list[int]]) -> list[list[int]]:
    """Solve probabilistic cases of a sudoku board.

    Args:
        board (list[list[int]]): The board to solve.

    Returns:
        list[list[int]]: The solved board.

    Note:
        Empty cells are represented by the Nonetype.
        boards are considered valid
        this part of the algorithm needs to only attempt to fix a single cell
    """

    emptycells = validity.getemptysquares(board)
    randomcell = random.choice(emptycells)
    valids = validity.validatposition(board, randomcell[0], randomcell[1])
    randomvalue = random.choice(valids)
    board[randomcell[0]][randomcell[1]] = randomvalue
    return board


def solveColorTrap(board: list[list[int]], candidate: int = 0) -> list[list[int]]:
    """Solve a board using the color wrap algorithm.

    Args:
        board (list[list[int]]): The board to solve.

    Returns:
        list[list[int]]: The solved board.

    Note:
        Empty cells are represented by the Nonetype.
        boards are considered valid
    """
    if candidate == 10:
        return board

    candidatecells = validity.getCellsWithCandidates(board, candidate)
    conjugatepairs = validity.getConjugatePairs(
        board, candidatecells, candidate)

    # if len(conjugatepairs) == 0:
    #     return solveColorTrap(board, candidate + 1)
    networks: list[dict[tuple[int, int], set[tuple[int, int]]]] = []

    while len(conjugatepairs) > 0:
        updated = False
        for network in networks:
            for pairL, pairR in conjugatepairs:
                if pairL in network:
                    network[pairL].add(pairR)
                    network[pairR] = {pairL}
                    conjugatepairs.remove((pairL, pairR))
                    updated = True
                    break
                elif pairR in network:
                    network[pairR].add(pairL)
                    network[pairL] = {pairR}
                    conjugatepairs.remove((pairL, pairR))
                    updated = True
                    break

        if not updated and len(conjugatepairs) > 0:
            pair = conjugatepairs.pop()
            newnetwork = {pair[0]: {pair[1]}}
            networks.append(newnetwork)

    for network in networks:
        # create colormap
        colormap: dict[tuple[int, int], bool] = {}
        for cell, subnetwork in network.items():
            if cell in colormap:
                for subcell in subnetwork:
                    colormap[subcell] = not colormap[cell]
            else:
                colormap[cell] = True
                for subcell in subnetwork:
                    colormap[subcell] = False

        for candidatecell in candidatecells:
            if candidatecell in colormap:
                continue
            else:
                visf = False
                vist = True
                visible = validity.getAffectingSquaresNonComplete(
                    board, candidatecell[0], candidatecell[1])
                for cell in visible:
                    if cell in colormap:
                        if colormap[cell]:
                            vist = True
                        else:
                            visf = True

                if visf and vist:
                    if candidatecell in validity.colorvalueremove:
                        validity.colorvalueremove[candidatecell].add(candidate)
                    else:
                        validity.colorvalueremove[candidatecell] = {candidate}

    solveColorTrap(board, candidate + 1)


if __name__ == "__main__":
    board = generate.generatepartial(percentageRemoved=0.1)
    utils.prettyprint(solve(board))


# grid = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

grid = [
    [0, 0, 0, 6, 0, 1, 9, 0, 0],
    [0, 0, 0, 0, 4, 0, 5, 0, 6],
    [0, 0, 6, 9, 0, 0, 0, 3, 8],
    [0, 8, 0, 0, 1, 6, 0, 0, 7],
    [0, 0, 1, 0, 0, 0, 3, 0, 0],
    [2, 0, 0, 8, 7, 0, 0, 5, 0],
    [9, 4, 0, 0, 0, 2, 7, 0, 0],
    [6, 0, 7, 0, 8, 0, 0, 0, 0],
    [0, 0, 5, 3, 0, 7, 0, 0, 0]
]

REF = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    0: " "
}


# Print grid in console for testing
def printGrid(b):
    print("\n\n")
    for i in range(len(b)):
        # Add horizontal borders every three rows
        if i % 3 == 0 and i != 0:
            print("------+-------+------")

        for j in range(len(b[0])):
            # Add vertical border every three columns
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            # Add newline when on last cell in row
            if j == 8:
                print(REF[b[i][j]])
            else:
                print(str(REF[b[i][j]]) + " ", end="")


# Find first empty cell in grid
def findEmpty(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return i, j

    # No empty cells found
    return None


# Check if the completed grid is valid for a given number
# i.e. num is not duplicated in any row/column/box
def valid(b, num, pos):
    # Check row
    for i in range(len(b[0])):
        if b[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(b)):
        if b[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    boxX = pos[1] // 3
    boxY = pos[0] // 3

    for i in range(boxY*3, boxY*3 + 3):
        for j in range(boxX*3, boxX*3 + 3):
            if b[i][j] == num and (i, j) != pos:
                return False

    # Board is valid for num
    return True


# Solve the Sudoku using backtracking
def solve(b):
    # Find the first empty cell to start trying values
    find = findEmpty(b)

    # If there are no empty cells, the grid is already solved
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        # Check if the current value is valid in the empty cell
        if valid(b, i, (row, col)):
            b[row][col] = i

            # If grid is now solved return true
            if solve(b):
                return True

            # This value is incorrect so reset the cell
            b[row][col] = 0

    # Unable to solve
    return False


if __name__ == '__main__':
    # Test the solver
    printGrid(grid)
    solve(grid)
    printGrid(grid)

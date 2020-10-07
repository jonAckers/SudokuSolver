import pygame
from main import solve, valid
pygame.font.init()


# Used to represent the Sudoku grid
class Grid:
    # Stores the current state of the grid
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows            # Stores the number of rows
        self.cols = cols            # Stores the number of columns
        self.cells = [[Cell(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]       # Creates an array of cells the correct size
        self.width = width          # Stores width of grid in pixels
        self.height = height        # Stores height of grid in pixels
        self.selected = None        # Stores which cell is being interacted with by user
        self.model = self.grid      # Stores working version of the grid

    # Solve the Sudoku
    def solve(self):
        # Use the solve function in the main script
        solve(self.model)

        # Update the cells with the new values to be displayed
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    self.cells[i][j].set(self.model[i][j], True)
                else:
                    self.cells[i][j].set(self.model[i][j], False)

    # Update the working model
    def updateModel(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Add the user entered values to the grid
    def place(self, val):
        # Get grid coordinates
        row, col = self.selected

        # Check if cell is empty
        if self.cells[row][col].value == 0:
            # Add value
            self.cells[row][col].set(val, False)
            self.updateModel()

            # Check if entered value is valid
            if valid(self.model, val, (row, col)):
                return True
            else:
                self.cells[row][col].set(0, False)
                self.updateModel()
                return False

    # Draw the grid
    def draw(self, win):
        # Draw grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    # Highlight cell selected by user
    def select(self, row, col):
        # Reset other cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        # Select desired cell
        self.cells[row][col].selected = True
        self.selected = (row, col)

    # Allow user to change selected using arrow keys
    def moveSelected(self, direction):
        # If there is no cell selected start with top left corner
        if not self.selected:
            self.select(0, 0)
        else:
            if direction == 'up' and self.selected[0]-1 >= 0:
                self.select(self.selected[0]-1, self.selected[1])
            if direction == 'down' and self.selected[0]+1 < self.rows:
                self.select(self.selected[0]+1, self.selected[1])
            if direction == 'left' and self.selected[1]-1 >= 0:
                self.select(self.selected[0], self.selected[1]-1)
            if direction == 'right' and self.selected[1]+1 < self.cols:
                self.select(self.selected[0], self.selected[1]+1)

    # Clear contents of cell
    def clear(self):
        row, col = self.selected
        self.cells[row][col].set(0, False)

    # Highlight cell when it's clicked
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None


# Used to represent a single cell in the grid
class Cell:
    # Stores number of rows and columns
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value          # Stores value in the cell
        self.temp = 0               # Stores temporary value
        self.row = row              # Stores row cell is in
        self.col = col              # Stores column cell is in
        self.width = width          # Stores width of cell in pixels
        self.height = height        # Stores height of cell in pixels
        self.selected = False       # Stores if cell is selected
        self.colour = (0, 0, 0)     # Stores colour of cell

    # Draw the cell
    def draw(self, win):
        # Set font
        fnt = pygame.font.SysFont(name="courier new", size=35, bold=True)

        # Set dimensions
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # Render cell
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, self.colour)
            win.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, self.colour)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # Make border red if highlighted
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    # Set the value of the cell
    def set(self, val, solved):
        self.value = val
        if solved:
            # If the value has been added by the solver make it blue
            self.colour = (14, 83, 194)
        else:
            # If the value has been added by the user make it black
            self.colour = (0, 0, 0)


# Display GUI and begin program
def main():
    # Set state for window
    width, height = 540, 625
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540)
    solveButton = pygame.Rect((width/2)-200, (height-65), 120, 50)
    resetButton = pygame.Rect((width/2)+80, (height-65), 120, 50)
    key = None
    run = True

    # Loop while program is running
    while run:
        # Check for user input
        for event in pygame.event.get():
            # Check for exit
            if event.type == pygame.QUIT:
                run = False

            # Check for keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    key = 1
                if event.key in [pygame.K_2, pygame.K_KP2]:
                    key = 2
                if event.key in [pygame.K_3, pygame.K_KP3]:
                    key = 3
                if event.key in [pygame.K_4, pygame.K_KP4]:
                    key = 4
                if event.key in [pygame.K_5, pygame.K_KP5]:
                    key = 5
                if event.key in [pygame.K_6, pygame.K_KP6]:
                    key = 6
                if event.key in [pygame.K_7, pygame.K_KP7]:
                    key = 7
                if event.key in [pygame.K_8, pygame.K_KP8]:
                    key = 8
                if event.key in [pygame.K_9, pygame.K_KP9]:
                    key = 9
                if event.key == pygame.K_UP:
                    board.moveSelected('up')
                    key = None
                if event.key == pygame.K_DOWN:
                    board.moveSelected('down')
                    key = None
                if event.key == pygame.K_LEFT:
                    board.moveSelected('left')
                    key = None
                if event.key == pygame.K_RIGHT:
                    board.moveSelected('right')
                    key = None
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                elif solveButton.collidepoint(pos):
                    board.solve()
                elif resetButton.collidepoint(pos):
                    main()
                    return

        # Update grid when user enters value
        if board.selected and key is not None:
            board.place(key)

        # Colour UI
        win.fill((255, 255, 255))
        pygame.draw.rect(win, [0, 0, 0], solveButton)
        pygame.draw.rect(win, [0, 0, 0], resetButton)

        text = pygame.font.SysFont(name="courier new", size=32, bold=True)
        solveText = text.render("Solve!", 1, (255, 255, 255))
        resetText = text.render("Reset", 1, (255, 255, 255))
        win.blit(solveText, ((width/2)-195, (height-57)))
        win.blit(resetText, ((width/2)+95, (height-57)))

        board.draw(win)
        pygame.display.update()


if __name__ == '__main__':
    # Start program
    main()
    pygame.quit()

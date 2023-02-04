class Position:
    def __init__(self, max_length: int):
        """
        Initialize a Position object with the main scanner position index and the line-column index.
        :param max_length: Total number of characters in the file;
        """
        self.main_pos = -1
        self.max_length = max_length
        self.line = 1
        self.column = 0

        self.filename = "<stdin>"

    def advance(self, line_break: bool = False) -> None:
        self.main_pos += 1
        # Reset the column index and increment the line if line_break is True
        if self.main_pos < self.max_length:
            if line_break:
                self.line += 1
                self.column = 0
            else:
                self.column += 1

    # Return a copy of the Position object
    def copy(self):
        new_pos = Position(self.max_length)
        new_pos.main_pos = self.main_pos
        new_pos.line = self.line
        new_pos.column = self.column
        new_pos.filename = self.filename
        return new_pos

    def get_lcpos(self) -> tuple:
        return (self.line, self.column)

    def print_lcpos(self) -> None:
        print(f"Line {self.line}, Column {self.column}")

from arrowpointer import generate_arrow_string


class Error:
    def __init__(self, error_type: str, error_message: str, error_pos, error_width: int = 1):
        self.type = error_type
        self.message = error_message
        self.pos = error_pos
        self.error_line = ""
        self.error_width = error_width

    def set_error_line(self, error_line):
        self.error_line = error_line

    def raise_error(self):
        traceback_header: str = "Traceback (most recent call last):\n\t"
        full_traceback_message: str = f"File \"{self.pos.filename}\", line {self.pos.line}, column {self.pos.column}\n\t\t"

        arrow_pointer = generate_arrow_string('\t\t', self.pos.column)
        code_pointer: str = f"{self.error_line}\n{arrow_pointer}"  # Pointer pointing to error in code codes here.
        error_message: str = f"{self.type}: {self.message}\n"

        full_message: str = traceback_header + full_traceback_message + code_pointer + error_message

        print(full_message)


class InvalidCharacterError(Error):
    def __init__(self, error_message: str, error_pos):
        super().__init__("InvalidCharacterError", error_message, error_pos)


class InvalidSyntaxError(Error):
    def __init__(self, error_message: str, error_pos, token_width: int = 1):
        super().__init__("SyntaxError", error_message, error_pos, token_width)

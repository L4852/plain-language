from arrowpointer import generate_arrow_string


class Error:
    def __init__(self, error_type: str, error_message: str, error_pos=None, error_width: int = 1):
        self.type = error_type
        self.message = error_message
        self.pos = error_pos
        self.error_line = ""
        self.error_width = error_width
        self.token_widths = None
        self.point = True

        self.context = None
        self.is_runtime_error = False

        self.error_line_number = -1

        self.filename = "<stdin>"

    def set_error_line(self, error_line, token_widths: list = None, point: bool = True):
        self.error_line = error_line.strip('\n')
        self.token_widths = token_widths
        self.point = point

    def raise_error(self):
        traceback_header: str = "Traceback (most recent call last):\n\t"

        full_traceback_message: str

        if self.is_runtime_error:
            full_traceback_message = ""

            active_context = self.context

            while active_context:
                full_traceback_message += f"File \"{self.filename}\", line {self.error_line_number} in {self.context.context_name}\n"
                active_context = active_context.parent_context
        else:
            full_traceback_message = f"File \"{self.pos.filename}\", line {self.pos.line}, column {self.pos.column}\n\t\t"

        error_message: str = f"{self.type}: {self.message}\n"

        if self.pos:
            if not self.token_widths:
                arrow_pointer = generate_arrow_string('\t\t', self.pos.column, self.error_width)
            else:
                arrow_pointer = "\n"

                code_pointer: str = f"{self.error_line}\n{arrow_pointer}"  # Pointer pointing to error in code codes here.

                full_message: str = traceback_header + full_traceback_message + code_pointer + error_message
                print(full_message)
                return

        full_message = traceback_header + full_traceback_message + error_message
        print(full_message)


class InvalidCharacterError(Error):
    def __init__(self, error_message: str, error_pos):
        super().__init__("InvalidCharacterError", error_message, error_pos)


class InvalidSyntaxError(Error):
    def __init__(self, error_message: str, error_pos, token_width: int = 1):
        super().__init__("SyntaxError", error_message, error_pos, token_width)


class NewRuntimeError(Error):
    def __init__(self, error_message, error_line_number=-1, context=None, filename=""):
        super().__init__("RuntimeError", error_message)
        self.is_runtime_error = True

        if filename:
            self.filename = filename

        self.context = context
        self.error_line_number = error_line_number

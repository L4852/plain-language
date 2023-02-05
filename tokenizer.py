from tokens import Token
from constants import Constants
from position import Position
from error import InvalidCharacterError


class Tokenizer:
    def __init__(self, source: str, filename: str = "<stdin>", debug_mode=False):
        self.source = source
        self.src_len = len(source)
        self.position = Position(self.src_len)
        self.index = self.position.main_pos
        self.position.filename = filename
        self.char = None
        self.delin_source = None

        self.token_list = None

        self.debug_mode = debug_mode

        self.next()

        self.delineate_source()

    def delineate_source(self) -> None:
        separated_source = [k + '\n' for k in self.source.split('\n')]
        self.delin_source = separated_source

    def next(self) -> None:
        """
        Advance the scanner position.
        """
        if self.char == '\n':
            self.position.advance(line_break=True)
        else:
            self.position.advance()
        self.index = self.position.main_pos
        self.char = self.source[self.index] if self.index < len(self.source) else None

    def tokenize(self) -> list:
        """
        Tokenize the input source text.

        :return: Returns a list of tokens.
        """

        token_list: list = []

        # Flags/buffer for number string
        has_dot: bool = False
        num_buffer: str = ""

        # Update line info for error message
        error_encountered = None
        start_of_line_index: int = -1

        # Comment active flag
        comment_active: bool = False

        # Identifier / keyword buffer
        idn_buffer = ""

        # String buffer
        string_buffer = ""
        string_active = False

        # Main tokenizer loop
        while self.char is not None:
            # Initialize line start flag location if at file start
            if start_of_line_index == -1:
                start_of_line_index = 0

            if string_active:
                if self.char == Constants.STRING_QUOTES:
                    string_length = len(string_buffer)

                    token_list.append(
                        Token(Constants.TYPE_STR, string_buffer, string_length, line_number=self.position.line))

                    string_buffer = ""
                    string_active = False
                    self.next()

                    if self.char is None and not error_encountered:
                        error_encountered = InvalidCharacterError(
                            "Missing ';' at end of statement",
                            self.position.copy()
                        )
                        error_encountered.set_error_line(self.delin_source[self.position.line - 1])
                        error_encountered.raise_error()
                        return []

                else:
                    string_buffer += self.char
                    self.next()

                    if self.char is None:
                        if not error_encountered:
                            error_encountered = InvalidCharacterError(
                                'Unexpected EOL when scanning string literal',
                                self.position.copy()
                            )
                            error_encountered.set_error_line(self.delin_source[self.position.line - 1])
                            error_encountered.raise_error()
                            return []
                    continue

            # Check if number buffer is not empty, terminates number and creates new Token object if current character
            # is not a number.
            if num_buffer and self.char not in Constants.NUM_CHARS:
                num_length = len(num_buffer)

                if has_dot:
                    token_list.append(
                        Token(Constants.TYPE_FLT, float(num_buffer), num_length, line_number=self.position.line))
                else:
                    token_list.append(
                        Token(Constants.TYPE_INT, int(num_buffer), num_length, line_number=self.position.line))
                num_buffer = ""
                has_dot = False
            elif idn_buffer and self.char not in Constants.VALID_IDN and not string_buffer:
                idn_length = len(idn_buffer)

                if idn_buffer in Constants.COMPARISONS:
                    token_list.append(Token(Constants.TYPE_SYMBOLS[idn_buffer], idn_buffer, idn_length,
                                            line_number=self.position.line))
                elif idn_buffer not in Constants.KEYWORDS:
                    token_list.append(Token(Constants.TYPE_IDN, idn_buffer, idn_length, line_number=self.position.line))

                else:
                    token_list.append(Token(Constants.TYPE_KYW, idn_buffer, idn_length, line_number=self.position.line))

                idn_buffer = ""

            # Skip over character if it is a tab, space, or newline
            if self.char in ' \t\n':
                # Keep track of the spaces to align Parser traceback
                if self.char == '\n':
                    self.next()
                    start_of_line_index = self.position.main_pos

                    # If comment line is active, terminate comment when \n encountered.
                    if comment_active:
                        comment_active = False
                else:
                    self.next()
            # Ignore the rest of the line if comment symbol detected
            elif self.char == '$':
                comment_active = True
                self.next()
            # Check if a valid int or float can be created
            elif self.char in Constants.NUM_CHARS and not idn_buffer and not comment_active:
                if self.char == Constants.NUMPOINT:
                    # Check if point already exists in the number buffer
                    if not has_dot:
                        next_char = self.source[self.position.main_pos + 1]
                        # Append the dot to the number buffer if it is not the only character in the buffer
                        # (following character is a space)
                        if num_buffer or next_char not in ' \t\n':
                            num_buffer += Constants.NUMPOINT
                            has_dot = True
                        else:
                            # Create a new error if dot rules are violated
                            if not error_encountered:
                                error_encountered = InvalidCharacterError(
                                    'An individual radix point \'.\' is not a number.',
                                    self.position.copy()
                                )

                    else:
                        # Create a new error if dot rules are violated
                        if not error_encountered:
                            error_encountered = InvalidCharacterError(
                                'Cannot have more than one radix point \'.\' in a number.',
                                self.position.copy()
                            )
                # Append if the character is a number and valid buffer
                else:
                    num_buffer += self.char

                self.next()
            elif self.char == Constants.STRING_QUOTES and not string_active:
                self.next()
                string_active = True

            # Append symbol with corresponding type in Constants.TYPE_SYMBOLS
            elif self.char in Constants.TYPE_SYMBOLS and not comment_active:
                token_list.append(Token(Constants.TYPE_SYMBOLS[self.char], line_number=self.position.line))
                self.next()
            elif self.char in Constants.VALID_IDN and not comment_active:
                idn_buffer += self.char
                self.next()

            if comment_active:
                self.next()
                continue

            # Print the error if it exists after the end of the current line is reached
            if error_encountered:
                self.next()
                if self.char == '\n' or self.char is None:
                    start_col = start_of_line_index

                    # Get the position of the end of the line
                    end_col = (self.position.column - 1) \
                        if self.position.line == 1 \
                        else (self.position.main_pos + self.position.column)

                    # Set the string for the error to the line containing the error
                    error_encountered.set_error_line(self.source[start_col:end_col])
                    error_encountered.raise_error()
                    error_encountered = None
                    return []

        # Return the finished token list
        if len(token_list) > 1:
            token_list.append(Token(Constants.TYPE_EOF, line_number=self.position.line))
            self.token_list = token_list

            if self.debug_mode:
                print(f"TOKENIZE RESULT: {token_list}")

            return token_list
        return []

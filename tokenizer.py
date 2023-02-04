from tokens import Token
from constants import Constants
from position import Position
from error import InvalidCharacterError


class Tokenizer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.src_len = len(source)
        self.position = Position(self.src_len)
        self.index = self.position.main_pos
        self.position.filename = filename
        self.char = None

        self.token_list = None

        self.next()

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

        # Main tokenizer loop
        while self.char is not None:
            # Initialize line start flag location if at file start
            if start_of_line_index == -1:
                start_of_line_index = 0

            # Check if number buffer is not empty, terminates number and creates new Token object if current character
            # is not a number.
            if num_buffer and self.char not in Constants.NUM_CHARS:
                num_length = len(num_buffer)

                if has_dot:
                    token_list.append(Token(Constants.TYPE_FLT, float(num_buffer), num_length))
                else:
                    token_list.append(Token(Constants.TYPE_INT, int(num_buffer), num_length))
                num_buffer = ""
                has_dot = False
            elif idn_buffer and self.char in " \t\n":
                idn_length = len(idn_buffer)
                
                if idn_buffer not in Constants.KEYWORDS:
                    token_list.append(Token(Constants.TYPE_IDN, idn_buffer, idn_length))
                else:
                    token_list.append(Token(Constants.TYPE_KYW, idn_buffer, idn_length))
                idn_buffer = ""

            # Skip over character if it is a tab, space, or newline
            if self.char in ' \t\n' or comment_active:
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
            # Check if a valid int or float can be created
            elif self.char in Constants.NUM_CHARS and not (idn_buffer):
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
            # Append symbol with corresponding type in Constants.TYPE_SYMBOLS
            elif self.char in Constants.TYPE_SYMBOLS:
                token_list.append(Token(Constants.TYPE_SYMBOLS[self.char]))
                self.next()
            elif self.char in Constants.VALID_IDN:
                idn_buffer += self.char

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
        token_list.append(Token(Constants.TYPE_EOF))
        self.token_list = token_list
        return token_list
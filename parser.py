from constants import Constants
from error import InvalidSyntaxError
from nodes import NumberNode, BinaryOperationNode, UnaryOperationNode, VariableAssignmentNode, VariableNode
from position import Position


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def __repr__(self):
        return f"{self.node}"

    def extract(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:
    def __init__(self, token_list, source: str = None):
        self.source = source
        self.token_list = token_list
        self.tkl_len = len(token_list)
        self.position = Position(self.tkl_len)
        self.index = self.position.main_pos
        self.ctoken = None

        self.line_token_index = 0

        self.delineate_source()

        self.next()

    def delineate_source(self) -> None:
        separated_source = [k + '\n' for k in self.source.split('\n')]
        self.source = separated_source

    def next(self) -> None:
        """
        Advance the scanner position.
        """
        self.index += 1
        self.ctoken = self.token_list[self.index] if self.index < len(self.token_list) else None

    def binary_operation(self, grammar, operators):
        result = ParseResult()
        left = result.extract(grammar())  # Get the node from the ParseResult

        if result.error:
            return result

        while self.ctoken.type in operators:
            operator = self.ctoken
            self.next()
            right = result.extract(grammar())

            if result.error:
                return result

            left = BinaryOperationNode(left, operator, right)

        if self.ctoken.type != Constants.TYPE_EOF:
            return result.success(left)

        new_error = InvalidSyntaxError("invalid syntax", self.position.copy(), self.ctoken.width)
        new_error.set_error_line(self.source[self.position.line - 1], [k.width for k in self.token_list], point=False)

        encapsulated_error = result.failure(new_error)

        return encapsulated_error

    def fact(self):
        result = ParseResult()

        token = self.ctoken

        if token.type in (Constants.TYPE_INT, Constants.TYPE_FLT):
            self.next()
            return result.success(NumberNode(token))
        elif token.type == Constants.TYPE_LPA:
            self.next()
            internal_expression = result.extract(self.expr())

            if result.error:
                return result

            if self.ctoken.type == Constants.TYPE_RPA:
                self.next()
                return result.success(internal_expression)
        elif token.type in (Constants.TYPE_ADD, Constants.TYPE_SUB):
            operator = self.ctoken
            self.next()

            factor = result.extract(self.fact())

            if result.error:
                return result

            return result.success(UnaryOperationNode(operator, factor))

        elif token.type == Constants.TYPE_IDN:
            self.next()
            return result.success(VariableNode(token))

        new_error = InvalidSyntaxError("invalid syntax", self.position.copy(), self.ctoken.width)
        new_error.set_error_line(self.source[self.position.line - 1], [k.width for k in self.token_list], point=False)

        encapsulated_error = result.failure(new_error)

        return encapsulated_error

    def term(self):
        return self.binary_operation(self.fact, (Constants.TYPE_MUL, Constants.TYPE_DIV))

    def expr(self):
        result = ParseResult()
        current = self.ctoken
        if current.type == Constants.TYPE_KYW:
            if current.value in Constants.KW_DATA_TYPES:
                self.next()
                if self.ctoken.type != Constants.TYPE_IDN:
                    new_error = InvalidSyntaxError("Expected identifier", self.position.copy(), self.ctoken.width)
                    new_error.set_error_line(self.source[self.position.line - 1], [k.width for k in self.token_list],
                                             point=False)

                    encapsulated_error = result.failure(new_error)

                    return encapsulated_error

                identifier = self.ctoken
                self.next()

                if self.ctoken.type != Constants.TYPE_EQU:
                    new_error = InvalidSyntaxError("Missing '=' in assignment", self.position.copy(), self.ctoken.width)
                    new_error.set_error_line(self.source[self.position.line - 1], [k.width for k in self.token_list],
                                             point=False)

                    encapsulated_error = result.failure(new_error)

                    return encapsulated_error

                self.next()

                expression = result.extract(self.expr())

                if result.error:
                    return result

                return result.success(VariableAssignmentNode(identifier, expression))

        else:
            return self.binary_operation(self.term, (Constants.TYPE_ADD, Constants.TYPE_SUB))

    def parse(self) -> BinaryOperationNode:
        expression = self.expr()

        if not expression.error:
            return expression.node

        expression.error.raise_error()
        return expression.error

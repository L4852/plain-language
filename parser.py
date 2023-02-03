from constants import Constants
from error import InvalidSyntaxError
from nodes import NumberNode, BinaryOperationNode
from position import Position

from tokenizer import test


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
    def __init__(self, token_list):
        self.token_list = token_list
        self.tkl_len = len(token_list)
        self.position = Position(self.tkl_len)
        self.index = self.position.main_pos
        self.ctoken = None

        self.next()

    def next(self) -> None:
        """
        Advance the scanner position.
        """
        self.position.advance()
        self.index = self.position.main_pos
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

        return result.success(left)

    def fact(self):
        result = ParseResult()

        token = self.ctoken

        if token.type in (Constants.TYPE_INT, Constants.TYPE_FLT):
            self.next()
            return result.success(NumberNode(token))

        return result.failure(
            InvalidSyntaxError("Expected int or float", self.position.copy(), self.ctoken.width)
        )

    def term(self):
        return self.binary_operation(self.fact, (Constants.TYPE_MUL, Constants.TYPE_DIV))

    def expr(self):
        return self.binary_operation(self.term, (Constants.TYPE_ADD, Constants.TYPE_SUB))

    def parse(self):
        expression = self.expr()
        return expression


if __name__ == "__main__":
    a = test()
    b = Parser(a)
    c = b.parse()

    print(c)

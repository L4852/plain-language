class NumberNode:
    def __init__(self, token):
        self.node = token
        self.update_context()

    def __repr__(self):
        return f"{self.node}"

    def update_context(self, context=None):
        self.context = context


class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.operator}, {self.right})"


class UnaryOperationNode:
    def __init__(self, operator, factor):
        self.operator = operator
        self.factor = factor

    def __repr__(self):
        return f"({self.operator}, {self.factor})"


class VariableDeclarationNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"[{self.identifier} <-+]"


class VariableAssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"[{self.identifier} <- {self.expression}]"


class VariableInitializationNode(VariableAssignmentNode):
    def __init__(self, identifier, expression):
        super().__init__(identifier, expression)


class VariableNode:
    def __init__(self, token):
        self.node = token


class StringNode(NumberNode):
    def __init__(self, token):
        super().__init__(token)

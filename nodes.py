class NumberNode:
    def __init__(self, token):
        self.node = token

    def __repr__(self):
        return f"{self.node}"


class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.operator}, {self.right})"

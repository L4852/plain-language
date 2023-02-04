from constants import Constants
from nodes import BinaryOperationNode, NumberNode, UnaryOperationNode


class Interpreter:
    def __init__(self, source):
        self.source = source

    def visit(self, node):
        if isinstance(node, NumberNode):
            return node.node.value
        elif isinstance(node, BinaryOperationNode):
            operator_type = node.operator.type
            if operator_type == Constants.TYPE_ADD:
                return self.visit(node.left) + self.visit(node.right)
            elif operator_type == Constants.TYPE_SUB:
                return self.visit(node.left) - self.visit(node.right)
            elif operator_type == Constants.TYPE_MUL:
                return self.visit(node.left) * self.visit(node.right)
            elif operator_type == Constants.TYPE_DIV:
                return self.visit(node.left) / self.visit(node.right)
        elif isinstance(node, UnaryOperationNode):
            if node.operator.type == Constants.TYPE_SUB:
                return -1 * self.visit(node.factor)
            return self.visit(node.factor)

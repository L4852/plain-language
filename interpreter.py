import pdb

from constants import Constants
from error import NewRuntimeError
from nodes import BinaryOperationNode, NumberNode, UnaryOperationNode, VariableNode, VariableAssignmentNode


class SymbolTable:
    def __init__(self):
        self.parent = None
        self.table = {}

    def lookup(self, variable_name):
        variable_value = self.table.get(variable_name, None)

        if variable_value is None and self.parent:
            return self.parent.get(variable_name)
        return variable_value

    def insert(self, variable_name):
        self.table.update({variable_name, })

    def update(self, variable_name, value):
        self.table[variable_name] = value

    def remove(self, variable_name):
        self.table.pop(variable_name)

class Interpreter:
    def __init__(self, source, context):
        self.source = source
        self.context = context

    def visit(self, node):
        if isinstance(node, NumberNode):
            node.update_context(self.context)
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
                denominator = self.visit(node.right)

                if denominator == 0:
                    return NewRuntimeError("Division by zero", error_line_number=node.right.node.line, context=self.context).raise_error()
                return self.visit(node.left) / denominator
        elif isinstance(node, UnaryOperationNode):
            if node.operator.type == Constants.TYPE_SUB:
                return -1 * self.visit(node.factor)
            return self.visit(node.factor)

        elif isinstance(node, VariableNode):
            variable_name = node.node.value
            variable_value = self.context.symbol_table.lookup(variable_name)
            print(self.context.symbol_table.table)

            if variable_value is None:
                return NewRuntimeError(f"'{variable_name}' is not defined", error_line_number=node.node.line, context=self.context).raise_error()

            return variable_value

        elif isinstance(node, VariableAssignmentNode):
            pdb.set_trace()
            variable_name = node.identifier.value
            print("WE ARE ASSIGNING!")
            variable_value = self.visit(node.expression)
            print("variable survived")
            self.context.symbol_table.table[variable_name] = variable_value


            print(self.context.symbol_table.table)

            return variable_value

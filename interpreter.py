import pdb

from constants import Constants
from error import NewRuntimeError
from nodes import BinaryOperationNode, NumberNode, UnaryOperationNode, VariableNode, VariableAssignmentNode, \
    VariableDeclarationNode, VariableInitializationNode


class SymbolTable:
    def __init__(self):
        self.parent = None
        self.table = {}

    def lookup(self, variable_name):
        variable_value = self.table.get(variable_name, None)

        if variable_value is None and self.parent:
            return self.parent.lookup(variable_name)
        return variable_value

    def exists(self, variable_name):
        if self.table.get(variable_name, '\0') != '\0':
            return True
        if self.parent and self.parent.lookup(variable_name) is not None:
            return True

        return False

    def insert(self, variable_name):
        self.table.update({variable_name, None})

    def update(self, variable_name, value):
        self.table[variable_name] = value

    def remove(self, variable_name):
        self.table.pop(variable_name)


class Interpreter:
    def __init__(self, source, context, filename=None, debug_mode = False):
        self.source = source
        self.context = context
        self.filename = filename
        self.debug_mode = debug_mode

    def _visit(self, node):
        if isinstance(node, NumberNode):
            node.update_context(self.context)
            return node.node.value
        elif isinstance(node, BinaryOperationNode):
            operator_type = node.operator.type
            if operator_type == Constants.TYPE_ADD:
                return self._visit(node.left) + self._visit(node.right)
            elif operator_type == Constants.TYPE_SUB:
                return self._visit(node.left) - self._visit(node.right)
            elif operator_type == Constants.TYPE_MUL:
                return self._visit(node.left) * self._visit(node.right)
            elif operator_type == Constants.TYPE_DIV:
                denominator = self._visit(node.right)

                if denominator == 0:
                    return NewRuntimeError("Division by zero", error_line_number=node.right.node.line,
                                           context=self.context, filename=self.filename).raise_error()
                return self._visit(node.left) / denominator
        elif isinstance(node, UnaryOperationNode):
            if node.operator.type == Constants.TYPE_SUB:
                return -1 * self._visit(node.factor)
            return self._visit(node.factor)

        elif isinstance(node, VariableNode):
            variable_name = node.node.value
            variable_value = self.context.symbol_table.lookup(variable_name)

            if variable_value is None:
                if self.context.symbol_table.exists(variable_name):
                    return NewRuntimeError(f"'{variable_name}' has been declared but not initialized to a value", error_line_number=node.node.line,
                                           context=self.context).raise_error()
                return NewRuntimeError(f"'{variable_name}' is not defined", error_line_number=node.node.line,
                                       context=self.context).raise_error()

            return variable_value

        elif isinstance(node, VariableDeclarationNode):
            variable_name = node.identifier.value

            if self.context.symbol_table.exists(variable_name):
                return NewRuntimeError(f"redeclaration of '{variable_name}'", error_line_number=0,
                                       context=self.context).raise_error()
            self.context.symbol_table.update(variable_name, None)

        elif isinstance(node, VariableInitializationNode):
            variable_name = node.identifier.value

            if not self.context.symbol_table.exists(variable_name):
                variable_value = self._visit(node.expression)
                self.context.symbol_table.update(variable_name, variable_value)
                return variable_value
            return NewRuntimeError(f"redefinition of '{variable_name}'", error_line_number=0,
                                   context=self.context).raise_error()

        elif isinstance(node, VariableAssignmentNode):
            variable_name = node.identifier.value

            variable_value = self._visit(node.expression)
            self.context.symbol_table.update(variable_name, variable_value)
            return variable_value

    def evaluate(self, node):
        completed = self._visit(node)
        if self.debug_mode:
            print(f"INTERPRETER: {completed}")
        return completed, self.context

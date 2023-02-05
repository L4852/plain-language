from context import Context
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter, SymbolTable


class Plain:
    def __init__(self, source_text, filename="<stdin>"):
        self.source_text = source_text
        self.filename = filename

    def interpret(self):
        tknz = Tokenizer(self.source_text).tokenize()
        parser = Parser(tknz, self.source_text).parse()

        global_context = Context("<main>")
        global_symbol_table = SymbolTable()
        global_symbol_table.update("false", 0)
        global_symbol_table.update("true", 1)

        global_context.symbol_table = global_symbol_table

        interpreter = Interpreter(self.source_text, global_context).visit(parser)

        return interpreter

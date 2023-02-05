import pdb

from context import Context
from interpreter import SymbolTable, Interpreter
from parser import Parser
from tokenizer import Tokenizer


def main():
    global_context = Context("<main>")
    global_symbol_table = SymbolTable()
    global_symbol_table.update("false", 0)
    global_symbol_table.update("true", 1)

    global_context.symbol_table = global_symbol_table

    while True:
        user_input = input("<shell> ")
        debug = False

        if user_input:
            token_list = Tokenizer(user_input, debug_mode=debug).tokenize()
            abstract_syntax_tree = Parser(token_list, user_input, debug_mode=debug).parse()
            output, global_context = Interpreter(user_input, global_context, filename=None, debug_mode=debug).evaluate(abstract_syntax_tree)

            if output is not None:
                print(output)


if __name__ == "__main__":
    main()
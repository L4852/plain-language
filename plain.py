import sys
from context import Context
from interpreter import SymbolTable, Interpreter
from parser import Parser
from tokenizer import Tokenizer

if __name__ == "__main__":
    filename = sys.argv[1]

    file_text: str
    with open(filename, 'r') as f:
        file_text = f.read()

    statements = [k.strip('\n') + ';' for k in file_text.split(';')]

    global_context = Context("<main>")
    global_symbol_table = SymbolTable()
    global_symbol_table.update("false", 0)
    global_symbol_table.update("true", 1)

    global_context.symbol_table = global_symbol_table

    if file_text:
        for item in statements:
            token_list = Tokenizer(item).tokenize()

            if not token_list:
                continue

            abstract_syntax_tree = Parser(token_list, item).parse()
            output, global_context = Interpreter(item, global_context, filename=filename).evaluate(
                abstract_syntax_tree)

            if output is not None:
                print(output)

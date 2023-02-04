from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def interpret(source_text: str):
    tknz = Tokenizer(source_text).tokenize()
    parser = Parser(tknz, source_text).parse()
    interpreter = Interpreter(source_text).visit(parser)

    return interpreter


def main():
    while True:
        user_input = input("> ")
        result = interpret(user_input)

        if result:
            print(result)


if __name__ == "__main__":
    main()

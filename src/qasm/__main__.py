import argparse
from qasm.lexer import Lexer
from qasm.parser import Parser


def main(file_name):
    file = open(file_name, "r")
    text = file.read()
    lexer = Lexer(text)
    parser = Parser(lexer.tokens)
    parser.programme.execute()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Execute and simulate qasm code")
    argparser.add_argument("file")
    args = argparser.parse_args()
    main(args.file)

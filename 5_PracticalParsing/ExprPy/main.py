import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprEval import ExprEval

def main(input_stream):
    # Create the lexer and parser
    lexer = ExprLexer(InputStream(input_stream))
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)

    # Parse the input and create the parse tree
    tree = parser.expr()

    # Create the evaluator and walk the tree
    eval_listener = ExprEval()
    walker = ParseTreeWalker()
    walker.walk(eval_listener, tree)

    # Get the final result
    result = eval_listener.getResult()
    print(f"Result: {result}")

if __name__ == '__main__':
    input_expr = input("Enter an expression: ")
    main(input_expr)

from Lexer import *

class Parser:
    """
    This parser implements an attempt to recognize the language of the following
    grammar:

    S ::= ( S | P
    P ::= ( P ) | Empty
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_valid_token()

    def consume(self, expected_type):
        if self.current_token.kind == expected_type:
            self.current_token = self.lexer.next_valid_token()
        else:
            msg = f"Expected {expected_type}, got {self.current_token.kind}"
            raise ValueError(msg)

    def S(self):
        if self.current_token.kind == TokenType.LPR:
            self.consume(TokenType.LPR)  # consume '('
            self.S()  # parse S
        self.P()  # parse P

    def P(self):
        if self.current_token.kind == TokenType.LPR:
            self.consume(TokenType.LPR)  # consume '('
            self.P()  # parse P
            self.consume(TokenType.RPR)  # consume ')'

    def parse(self):
        self.S()
        if self.current_token.kind != TokenType.EOF:
            raise ValueError(f"Unexpected token {self.current_token.kind}")

def test_parser(input_str):
    lexer = Lexer(input_str)
    parser = Parser(lexer)
    try:
        parser.parse()
        print(f"{input_str} is valid.")
    except ValueError as e:
        print(f"{input_str} is invalid: {e}")

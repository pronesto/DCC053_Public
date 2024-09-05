from Exp import *
from Lexer import *

class Parser:
    """
    This class implements a parser for infix arithmetic expressions.

    The parser uses the following grammar:

    E ::= T ('+' E | '-' E | empty)

    T ::= F ('*' T | '/' T | empty)

    F ::= num
	| '(' E ')'

    Example:
    >>> lexer = Lexer("2 + 3 + 4")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    9

    >>> lexer = Lexer("2 * 3 * 4")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    24

    >>> lexer = Lexer("(2 + 3) * 4")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    20

    >>> lexer = Lexer("4 * (2 + 3)")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    20

    >>> lexer = Lexer("2 * 3 + 4")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    10

    >>> lexer = Lexer("2 - 3 - 4")
    >>> parser = Parser(lexer)
    >>> e = parser.E()
    >>> e.eval()
    -5
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_valid_token()

    def eat(self, token_type):
        if self.current_token.kind == token_type:
            self.current_token = self.lexer.next_valid_token()
        else:
            raise ValueError(f"Unexpected token: {self.current_token.kind}")

    def E(self):
        """
        """
        exp = self.T()
        token = self.current_token

        if token.kind == TokenType.ADD:
            self.eat(TokenType.ADD)
            right = self.E()
            exp = Add(exp, right)

        elif token.kind == TokenType.SUB:
            self.eat(TokenType.SUB)
            right = self.E()
            exp = Sub(exp, right)

        return exp

    def T(self):
        """
        """
        exp = self.F()
        token = self.current_token

        if token.kind == TokenType.MUL:
            self.eat(TokenType.MUL)
            right = self.T()
            exp = Mul(exp, right)

        elif token.kind == TokenType.DIV:
            self.eat(TokenType.DIV)
            right = self.T()
            exp = Div(exp, right)

        return exp

    def F(self):
        """
        """
        token = self.current_token

        if token.kind == TokenType.NUM:
            self.eat(TokenType.NUM)
            return Num(int(token.text))

        elif token.kind == TokenType.LPR:  # '('
            self.eat(TokenType.LPR)
            node = self.E()
            self.eat(TokenType.RPR)  # ')'
            return node

from Exp import *
from Lexer import *


class Parser:
    """
    This class implements a parser for infix arithmetic expressions.

    The parser uses the following grammar:

    E ::= num F
        | '(' E ')' F

    F ::= '+' E F
        | '-' E F
        | '*' E F
        | '/' E F
        | empty

    Examples:
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

        >>> lexer = Lexer("(2 * 3) + 4")
        >>> parser = Parser(lexer)
        >>> e = parser.E()
        >>> e.eval()
        10

        >>> lexer = Lexer("(2 - 3) - (4 - 10)")
        >>> parser = Parser(lexer)
        >>> e = parser.E()
        >>> e.eval()
        5
    """

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.next_valid_token()

    def eat(self, token_type: TokenType) -> None:
        if self.current_token.kind == token_type:
            self.current_token = self.lexer.next_valid_token()
        else:
            raise ValueError(f"Unexpected token: {self.current_token.kind}")

    def E(self) -> Expression:
        """
        Parse the base case (numbers or parenthesized expressions).

        This case implements the productions:

        E ::= num F
            | '(' E ')' F

        Returns:
            Expression: an instance of `Expression` with the parsed arithmetic
            expression.
        """

        token = self.current_token

        if token.kind == TokenType.NUM:
            self.eat(TokenType.NUM)
            num = Num(int(token.text))
            return self.F(num)

        elif token.kind == TokenType.LPR:  # '('
            self.eat(TokenType.LPR)
            node = self.E()
            self.eat(TokenType.RPR)  # ')'
            return self.F(node)

    def F(self, left: Expression) -> Expression:
        """
        Parse the continuation of an expression (right recursion).

        This case implements the productions:

        F ::= '+' E F
            | '-' E F
            | '*' E F
            | '/' E F
            | empty

        Parameters:
            left (Expression): the left element of the arithmetic expression.

        Returns
            Expression: an instance of `Expression` with the parsed arithmetic
            expression.
        """

        token = self.current_token

        if token.kind == TokenType.ADD:
            self.eat(TokenType.ADD)
            right = self.E()
            return self.F(Add(left, right))

        elif token.kind == TokenType.SUB:
            self.eat(TokenType.SUB)
            right = self.E()
            return self.F(Sub(left, right))

        elif token.kind == TokenType.MUL:
            self.eat(TokenType.MUL)
            right = self.E()
            return self.F(Mul(left, right))

        elif token.kind == TokenType.DIV:
            self.eat(TokenType.DIV)
            right = self.E()
            return self.F(Div(left, right))

        # If no more operators, return the current node.
        return left

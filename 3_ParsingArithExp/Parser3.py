from Exp import *
from Lexer import *


class Parser:
    """
    This class implements a parser for infix arithmetic expressions.

    The parser uses the following grammar:

    E ::= T EE

    EE ::= '+' T EE
        | '-' T EE
        | empty

    T  ::= F TT

    TT ::= '*' F TT
        | '/' F TT
        | empty

    F  ::= num
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
        Parse an expression according to the production rule:

        E ::= T EE

        Returns:
            exp (Expression): An expression node representing the complete
            expression.
        """

        exp = self.T()
        return self.EE(exp)

    def EE(self, left: Expression) -> Expression:
        """
        Parse the remainder of an expression that includes addition or subtraction.

        This method corresponds to the production rule:

        EE ::= '+' T EE
            | '-' T EE
            | empty

        Parameters:
            left (Expression): the left-hand side expression of the current
            expression.

        Returns:
            Expression: an expression node representing either the left side, or
            a larger expression incorporating additional addition or subtraction
            operations.
        """

        token = self.current_token

        if token.kind == TokenType.ADD:
            self.eat(TokenType.ADD)
            right = self.T()
            return self.EE(Add(left, right))

        elif token.kind == TokenType.SUB:
            self.eat(TokenType.SUB)
            right = self.T()
            return self.EE(Sub(left, right))

        # If no more operators, return the current node.
        return left

    def T(self) -> Expression:
        """
        Parse a term according to the production rule:

        T ::= F TT

        Returns:
            exp (Expression): an expression node representing the complete term.
        """

        exp = self.F()
        return self.TT(exp)

    def TT(self, left: Expression) -> Expression:
        """
        Parse the remainder of a term that includes multiplication or division.

        This method corresponds to the production rule:

        TT ::= '*' F TT
            | '/' F TT
            | empty

        Parameters:
            left (Expression): the left-hand side expression of the current term.

        Returns:
            Expression: an expression node representing either the left side, or
            a larger expression incorporating additional multiplication or
            division operations.
        """

        token = self.current_token

        if token.kind == TokenType.MUL:
            self.eat(TokenType.MUL)
            right = self.F()
            return self.TT(Mul(left, right))

        elif token.kind == TokenType.DIV:
            self.eat(TokenType.DIV)
            right = self.F()
            return self.TT(Div(left, right))

        # If no more operators, return the current node.
        return left

    def F(self) -> Expression:
        """
        Parse a factor, which is either a number or a parenthesized expression.

        This method corresponds to the production rule:

        F ::= num
            | '(' E ')'

        Returns:
            Expression: an expression node representing a number or a
            parenthesized expression.
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

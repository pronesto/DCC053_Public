from Lexer import *


class Parser:
    """
    This parser implements an attempt to recognize the language of the following
    grammar:

    S ::= ( S ) S | Empty

    The grammar accepts valid expressions of balanced parentheses where S can be an empty string
    or can recursively contain valid parenthesis expressions.

    Attributes:
        lexer (Lexer): The lexer instance responsible for tokenizing the input.
        current_token (Token): The token currently being processed.

    Example:
        >>> lexer = Lexer('()')
        >>> parser = Parser(lexer)
        >>> parser.parse()  # Should not raise an error, meaning valid input.

        >>> lexer = Lexer('((()))')
        >>> parser = Parser(lexer)
        >>> parser.parse()  # Should not raise an error for deeply nested expression.

        >>> lexer = Lexer('(()')
        >>> parser = Parser(lexer)
        >>> try:
        ...     parser.parse()
        ... except ValueError as e:
        ...     print(e)
        Expected TokenType.RPR, got TokenType.EOF
    """

    def __init__(self, lexer):
        """
        Initializes the parser with a given lexer.

        Parameters:
            lexer (Lexer): The lexer instance responsible for providing tokens.

        Example:
            >>> lexer = Lexer('()')
            >>> parser = Parser(lexer)
            >>> parser.current_token.kind == TokenType.LPR
            True
        """
        self.lexer = lexer
        self.current_token = self.lexer.next_valid_token()

    def consume(self, expected_type):
        """
        Consumes the current token if it matches the expected token type, otherwise raises a ValueError.

        Parameters:
            expected_type (TokenType): The type of the token expected.

        Raises:
            ValueError: If the current token type doesn't match the expected type.

        Example:
            >>> lexer = Lexer('(')
            >>> parser = Parser(lexer)
            >>> parser.consume(TokenType.LPR)
            >>> parser.current_token.kind == TokenType.EOF
            True

            >>> lexer = Lexer(')')
            >>> parser = Parser(lexer)
            >>> try:
            ...     parser.consume(TokenType.LPR)
            ... except ValueError as e:
            ...     print(e)
            Expected TokenType.LPR, got TokenType.RPR
        """
        if self.current_token.kind == expected_type:
            self.current_token = self.lexer.next_valid_token()
        else:
            msg = f"Expected {expected_type}, got {self.current_token.kind}"
            raise ValueError(msg)

    def S(self):
        """
        Implements the grammar rule for S.

        S ::= ( S ) S | Empty

        This method handles both recursive and base cases for the grammar, consuming tokens and ensuring balanced parentheses.

        Example:
            >>> lexer = Lexer('(())')
            >>> parser = Parser(lexer)
            >>> parser.S()  # Should not raise an error for valid input.

            >>> lexer = Lexer('((())')
            >>> parser = Parser(lexer)
            >>> try:
            ...     parser.S()
            ... except ValueError as e:
            ...     print(e)
            Expected TokenType.RPR, got TokenType.EOF
        """
        if self.current_token.kind == TokenType.LPR:
            self.consume(TokenType.LPR)  # consume '('
            self.S()  # parse S
            self.consume(TokenType.RPR)  # consume ')'
            self.S()  # parse S

    def parse(self):
        self.S()
        if self.current_token.kind != TokenType.EOF:
            raise ValueError(f"Unexpected token {self.current_token.kind}")


def test_parser(input_str):
    """
    This function tests our parser of Dick language.

    Example:
    >>> test_parser('()()()')
    ()()() is valid.

    >>> test_parser('(()())')
    (()()) is valid.

    >>> test_parser('((()))')
    ((())) is valid.
    """
    lexer = Lexer(input_str)
    parser = Parser(lexer)
    try:
        parser.parse()
        print(f"{input_str} is valid.")
    except ValueError as e:
        print(f"{input_str} is invalid: {e}")

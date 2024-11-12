from Lexer import *


class Parser:
    """
    This parser implements an attempt to recognize the language of the following
    grammar:

    S ::= ( S | P
    P ::= ( P ) | Empty

    Attributes:
        lexer (Lexer): The lexer instance responsible for tokenizing the input.
        current_token (Token): The token currently being processed.

    Example:
        >>> lexer = Lexer('(')
        >>> parser = Parser(lexer)
        >>> parser.parse()  # Should not raise an error for valid input.

        >>> lexer = Lexer('((')
        >>> parser = Parser(lexer)
        >>> parser.parse()  # Should not raise an error for valid nested input.

        >>> lexer = Lexer('(())')
        >>> parser = Parser(lexer)
        >>> try:
        ...     parser.parse()
        ... except ValueError as e:
        ...     print(e)
        Unexpected token TokenType.RPR
    """

    def __init__(self, lexer):
        """
        Initializes the parser with a given lexer.

        Parameters:
            lexer (Lexer): The lexer instance responsible for providing tokens.

        Example:
            >>> lexer = Lexer('(')
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

        S ::= ( S | P

        This method handles both the recursive case for S and also invokes P when necessary.

        Example:
            >>> lexer = Lexer('(()())')
            >>> parser = Parser(lexer)
            >>> parser.S()  # Should not raise an error for valid nested parentheses.
        """
        if self.current_token.kind == TokenType.LPR:
            self.consume(TokenType.LPR)  # consume '('
            self.S()  # parse S
        self.P()  # parse P

    def P(self):
        """
        Implements the grammar rule for P.

        P ::= ( P ) | Empty

        This method handles nested parentheses expressions and ensures they are balanced.

        Example:
            >>> lexer = Lexer('(())')
            >>> parser = Parser(lexer)
            >>> parser.P()  # Should not raise an error for balanced parentheses.

            >>> lexer = Lexer('(()')
            >>> parser = Parser(lexer)
            >>> try:
            ...     parser.P()
            ... except ValueError as e:
            ...     print(e)
            Expected TokenType.RPR, got TokenType.EOF
        """
        if self.current_token.kind == TokenType.LPR:
            self.consume(TokenType.LPR)  # consume '('
            self.P()  # parse P
            self.consume(TokenType.RPR)  # consume ')'

    def parse(self):
        """
        Starts the parsing process by invoking the S method and checks for unexpected tokens after parsing.

        Raises:
            ValueError: If there are unexpected tokens after parsing is complete.
        """
        self.S()
        if self.current_token.kind != TokenType.EOF:
            raise ValueError(f"Unexpected token {self.current_token.kind}")


def test_parser(input_str):
    """
    Tests the parser with the given input string.

    Parameters:
        input_str (str): The input string to be parsed.

    Example:
        >>> test_parser('()')
        () is invalid: Unexpected token TokenType.RPR

        >>> test_parser('(()') # Notice that this test should pass, but since it is a LL parser the left recursion prevents it
        (() is invalid: Unexpected token TokenType.RPR

        >>> test_parser('((')
        (( is valid.

        >>> test_parser('(()))')
        (())) is invalid: Unexpected token TokenType.RPR
    """
    lexer = Lexer(input_str)
    parser = Parser(lexer)
    try:
        parser.parse()
        print(f"{input_str} is valid.")
    except ValueError as e:
        print(f"{input_str} is invalid: {e}")

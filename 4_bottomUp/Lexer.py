import enum
from Exp import *


class TokenType(enum.Enum):
    """
    These class defines the possible tokens that we consider.
    """

    EOF = -1  # End of file
    NLN = 0  # New line
    WSP = 1  # White Space
    NUM = 2  # Number (integers)
    LPR = 3  # Left parenthesis
    RPR = 4  # Right parenthesis
    ADD = 202  # The token '+'
    SUB = 203  # The token '-'
    MUL = 204  # The token '*'
    DIV = 205  # The token '/'


class Token:
    """
    This class represents a token, which is a basic unit of meaning extracted
    from the input string during lexical analysis.

    Attributes:
        text (str): The token's actual text, used for identifiers, strings, and
        numbers.
        kind (TokenType): The type of the token, which classifies it based on
        its role in the expression.


    """

    # A list of tokens that represent operators in arithmetic expressions:
    operators = {TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV}

    def __init__(self, tokenText, tokenKind):
        """
        Initializes a Token object with its text and type.

        Parameters:
            tokenText (str): The actual text of the token.
            tokenKind (TokenType): The type of the token defined in TokenType.


        Example:
            >>> token = Token("3", TokenType.NUM)
            >>> token.text
            '3'
            >>> token.kind == TokenType.NUM
            True

            >>> token = Token("+", TokenType.ADD)
            >>> token.text
            '+'
            >>> token.kind == TokenType.ADD
            True
        """
        self.text = tokenText
        self.kind = tokenKind


class Lexer:
    """
    This class implements a simple lexer. It processes an input string and
    breaks it down into a sequence of tokens.

    The lexer maintains an internal state that tracks the current position in
    the input string. Each call to `getToken` returns the next token and
    advances the lexer state.

    Attributes:
        input_string (str): The string to be tokenized.
        position (int): The current position in the input string.
        length (int): The length of the input string.
    Example:
        >>> lexer = Lexer("3 + 4")
        >>> token = lexer.next_valid_token()
        >>> token.text
        '3'
        >>> token.kind == TokenType.NUM
        True
    """

    def __init__(self, input_string):
        """
        Initializes the lexer with the input string that will be scanned.

        Parameters:
            input_string (str): The string to be tokenized.

        Example:
            >>> lexer = Lexer("1 + 2")
            >>> lexer.input_string
            '1 + 2'
        """
        self.input_string = input_string
        self.position = 0
        self.length = len(input_string)

    def next_valid_token(self):
        """
        Retrieves the next valid token that is not a white space or a new line.

        This method skips any tokens that are classified as white space or new
        line and returns the first non-whitespace token found.

        Returns:
            Token: The next valid token in the input stream.

        Example:
            >>> lexer = Lexer("  2 + 3 ")
            >>> token = lexer.next_valid_token()
            >>> token.text
            '2'
            >>> lexer.next_valid_token().text
            '+'
        """
        token = self.getToken()
        if token.kind == TokenType.WSP or token.kind == TokenType.NLN:
            token = self.next_valid_token()
        return token

    def tokens(self):
        """
        Generator that yields valid tokens from the input string, ignoring
        white spaces and new lines.

        This method continues to yield tokens until the end of the file is
        reached.

        Yields:
            Token: The next valid token in the input stream.

        Example:
            >>> lexer = Lexer("(3 + 2)")
            >>> [token.text for token in lexer.tokens()]
            ['(', '3', '+', '2', ')']
        """
        token = self.getToken()
        while token.kind != TokenType.EOF:
            if token.kind != TokenType.WSP and token.kind != TokenType.NLN:
                yield token
            token = self.getToken()

    def getToken(self):
        """
        Retrieves the next token from the input string.

        The lexer reads characters from the input string, classifies them
        according to their type (e.g., operator, number, white space), and
        returns a Token object.

        Returns:
            Token: The next token identified in the input string.

        Example:
            >>> lexer = Lexer("3 + 4")
            >>> lexer.getToken().text
            '3'
            >>> lexer.getToken().text
            ' '
            >>> lexer.getToken().text
            '+'
        """
        if self.position >= self.length:
            return Token("", TokenType.EOF)

        current_char = self.input_string[self.position]
        self.position += 1

        if current_char.isdigit():
            # Handle numbers (NUM)
            number_text = current_char
            while (
                self.position < self.length
                and self.input_string[self.position].isdigit()
            ):
                number_text += self.input_string[self.position]
                self.position += 1
            return Token(number_text, TokenType.NUM)

        elif current_char == "+":
            return Token(current_char, TokenType.ADD)

        elif current_char == "-":
            return Token(current_char, TokenType.SUB)

        elif current_char == "*":
            return Token(current_char, TokenType.MUL)

        elif current_char == "/":
            return Token(current_char, TokenType.DIV)

        elif current_char == "(":
            return Token(current_char, TokenType.LPR)

        elif current_char == ")":
            return Token(current_char, TokenType.RPR)

        elif current_char == " ":
            return Token(current_char, TokenType.WSP)

        elif current_char == "\n":
            return Token(current_char, TokenType.NLN)

        else:
            raise ValueError(f"Unexpected character: {current_char}")


def compute_prefix(lexer):
    """
    Converts an arithmetic expression in Polish Notation to an expression tree.

    This function converts a string into an expression tree, and returns it.

    Parameters:
        lexer (Lexer): An instance of the Lexer class, initialized with a string
                       containing the arithmetic expression in prefix notation.

    Returns:
        int: The computed value of the arithmetic expression.

    Raises:
        ValueError: If an unexpected token type is encountered.

    Examples:
        >>> lexer = Lexer("+ 3 * 4 2")
        >>> e = compute_prefix(lexer)
        >>> e.eval()
        11

        >>> lexer = Lexer("+ * 3 4 2")
        >>> e = compute_prefix(lexer)
        >>> e.eval()
        14
    """
    token = lexer.next_valid_token()

    if token.kind == TokenType.NUM:
        # Base case: return the value if it's a number
        return Num(int(token.text))

    elif token.kind in Token.operators:
        # Recursive case: evaluate the operands
        a = compute_prefix(lexer)
        b = compute_prefix(lexer)

        if token.kind == TokenType.ADD:
            return Add(a, b)
        elif token.kind == TokenType.SUB:
            return Sub(a, b)
        elif token.kind == TokenType.MUL:
            return Mul(a, b)
        elif token.kind == TokenType.DIV:
            return Div(a, b)

    else:
        raise ValueError(f"Unexpected token type: {token.kind}")

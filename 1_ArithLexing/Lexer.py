import enum


class TokenType(enum.Enum):
    """
    These class defines the possible tokens that we consider.
    """

    EOF = -1  # End of file
    NLN = 0  # New line
    WSP = 1  # White Space
    NUM = 2  # Number (integers)
    ADD = 202  # The token '+'
    SUB = 203  # The token '-'
    MUL = 204  # The token '*'
    DIV = 205  # The token '/'


class Token:
    """
    This class contains the definition of Tokens. A token has two fields: its
    text and its kind. The "kind" of a token is a constant that identifies it
    uniquely. See the TokenType to know the possible identifiers (if you want).
    You don't need to change this class.
    """

    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind


class Lexer:
    """
    This class implements a simple lexer. It keeps, as its internal state, the
    string that must be scanned. At any given point, we can read the next token
    in this string and return it. This operation modifies the internal state of
    the object: if we read the next token twice, unless we are at the end of the
    token stream, we will get always a different token.
    """

    def __init__(self, input_string):
        """
        The constructor initializes the lexer with the string that must be
        scanned. This string will be transformed into a sequence of tokens as
        needed: whenever we read the next token.
        """ 
        self.input_string = input_string
        self.position = 0
        self.length = len(input_string)

    def next_valid_token(self):
        """
        A valid token is any token that is not a white space or a new line.
        """
        token = self.getToken()
        if token.kind == TokenType.WSP or token.kind == TokenType.NLN:
            token = self.next_valid_token()
        return token

    def tokens(self):
        """
        This method iterates over the list of tokens lazily.
        """
        token = self.next_valid_token()
        while token.kind != TokenType.EOF:
            yield token
            token = self.next_valid_token()

    def getToken(self):
        """
        This method returns the next token in the sequence of tokens. Notice
        that this method changes the state of our lexer. If invoked twice, it
        will return different tokens, unless we are at the end of the token
        stream. In this case, it return EOF.
        """
        if self.position >= self.length:
            return Token("", TokenType.EOF)

        current_char = self.input_string[self.position]

        # Skip whitespaces and new lines
        while current_char in [" ", "\n"]:
            if current_char == " ":
                token = Token(current_char, TokenType.WSP)
            elif current_char == "\n":
                token = Token(current_char, TokenType.NLN)
            self.position += 1
            if self.position >= self.length:
                return Token("", TokenType.EOF)
            current_char = self.input_string[self.position]
            return token

        # Handle numbers
        if current_char.isdigit():
            num_str = ""
            while (
                self.position < self.length
                and self.input_string[self.position].isdigit()
            ):
                num_str += self.input_string[self.position]
                self.position += 1
            return Token(num_str, TokenType.NUM)

        # Handle operators
        if current_char == "+":
            self.position += 1
            return Token("+", TokenType.ADD)
        elif current_char == "-":
            self.position += 1
            return Token("-", TokenType.SUB)
        elif current_char == "*":
            self.position += 1
            return Token("*", TokenType.MUL)
        elif current_char == "/":
            self.position += 1
            return Token("/", TokenType.DIV)

        # If none of the above, move to next character (could add error
        # handling here)
        self.position += 1
        return self.getToken()


def compute_postfix(lexer):
    """
    Computes the arithmetic value associated with a list of tokens assumed to
    be in reverse polish notation.

    Examples:
        >>> lexer = Lexer("3 4 + 2 * 7 /")
        >>> compute_postfix(lexer)
        2

        >>> lexer = Lexer("4 2 5 * + 1 3 2 * + /")
        >>> compute_postfix(lexer)
        2
    """
    stack = []

    operators = {TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV}
    for token in lexer.tokens():
        if token.kind == TokenType.NUM:
            stack.append(int(token.text))
        elif token.kind in operators:
            if len(stack) < 2:
                raise ValueError("Insufficient values in expression.")
            b = stack.pop()
            a = stack.pop()

            if token.kind == TokenType.ADD:
                stack.append(a + b)
            elif token.kind == TokenType.SUB:
                stack.append(a - b)
            elif token.kind == TokenType.MUL:
                stack.append(a * b)
            elif token.kind == TokenType.DIV:
                if b == 0:
                    raise ZeroDivisionError("Division by zero is undefined.")
                stack.append(a // b)  # Integer division

    if len(stack) != 1:
        raise ValueError("The user input has too many values.")

    return stack.pop()


def compute_prefix(lexer):
    """
    Computes the arithmetic value associated with a list of tokens assumed to
    be in polish notation.

    Examples:
        >>> lexer = Lexer("+ 3 * 4 2")
        >>> compute_prefix(lexer)
        11

        >>> lexer = Lexer("+ * 3 4 2")
        >>> compute_prefix(lexer)
        14
    """
    token = lexer.next_valid_token()

    if token.kind == TokenType.NUM:
        return int(token.text)

    operators = {TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV}
    if token.kind in operators:
        # Recursively compute the two operands
        a = compute_prefix(lexer)
        b = compute_prefix(lexer)

        if token.kind == TokenType.ADD:
            return a + b
        elif token.kind == TokenType.SUB:
            return a - b
        elif token.kind == TokenType.MUL:
            return a * b
        elif token.kind == TokenType.DIV:
            if b == 0:
                raise ZeroDivisionError("Division by zero is undefined.")
            return a // b  # Integer division

    raise ValueError(f"Unexpected token in expression: {token.kind}.")

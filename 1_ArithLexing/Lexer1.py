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
    VAR = 206  # General variables


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
        """
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def key_word_token(text):
        """
        This method returns the token associated with a given keyword in the
        language, or None otherwise.

        Example:
        >>> Token.key_word_token('add').text
        '+'

        >>> Token.key_word_token('sub').text
        '-'

        >>> Token.key_word_token('x').text
        'x'
        """
        tokens = {}
        tokens["add"] = Token("+", TokenType.ADD)
        tokens["sub"] = Token("-", TokenType.SUB)
        if text in tokens:
            return tokens[text]
        else:
            return Token(text, TokenType.VAR)


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
    """

    def __init__(self, input_string):
        """
        Initializes the lexer with the input string that will be scanned.

        Parameters:
            input_string (str): The string to be tokenized.
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

        elif current_char.isalpha():
            id_text = current_char
            while (
                self.position < self.length
                and self.input_string[self.position].isalnum()
            ):
                id_text += self.input_string[self.position]
                self.position += 1
            return Token.key_word_token(tokText)

        elif current_char == "+":
            return Token(current_char, TokenType.ADD)

        elif current_char == "-":
            return Token(current_char, TokenType.SUB)

        elif current_char == "*":
            return Token(current_char, TokenType.MUL)

        elif current_char == "/":
            return Token(current_char, TokenType.DIV)

        elif current_char == " ":
            return Token(current_char, TokenType.WSP)

        elif current_char == "\n":
            return Token(current_char, TokenType.NLN)

        else:
            raise ValueError(f"Unexpected character: {current_char}")


def compute_postfix(lexer):
    """
    Evaluates an arithmetic expression in Reverse Polish Notation (Postfix
    Notation).

    The function uses a stack to compute the value of the expression. As it
    processes tokens from the lexer, it pushes numbers onto the stack and pops
    them when an operator is encountered, performing the operation and pushing
    the result back onto the stack.

    Parameters:
        lexer (Lexer): An instance of the Lexer class, initialized with a string
                       containing the arithmetic expression in postfix notation.

    Returns:
        int: The computed value of the arithmetic expression.

    Raises:
        ValueError: If an unexpected token type is encountered or the stack is
        improperly used.

    Examples:
        >>> lexer = Lexer("3 4 + 2 * 7 /")
        >>> compute_postfix(lexer)
        2

        >>> lexer = Lexer("4 2 5 * + 1 3 2 * + /")
        >>> compute_postfix(lexer)
        2
    """
    stack = []

    for token in lexer.tokens():
        if token.kind == TokenType.NUM:
            # Push numbers onto the stack
            stack.append(int(token.text))

        elif token.kind in Token.operators:
            # Pop the top two numbers off the stack and apply the operator
            if len(stack) < 2:
                raise ValueError("Insufficient values in the expression.")

            b = stack.pop()
            a = stack.pop()

            if token.kind == TokenType.ADD:
                result = a + b
            elif token.kind == TokenType.SUB:
                result = a - b
            elif token.kind == TokenType.MUL:
                result = a * b
            elif token.kind == TokenType.DIV:
                if b == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = a // b

            # Push the result back onto the stack
            stack.append(result)

        else:
            raise ValueError(f"Unexpected token type: {token.kind}")

    # The final result should be the only value left in the stack
    if len(stack) != 1:
        raise ValueError("The user input has too many values.")

    return stack[0]


def compute_prefix(lexer):
    """
    Evaluates an arithmetic expression in Polish Notation (Prefix Notation).

    This function uses recursion to evaluate the expression. When it encounters
    an operator, it recursively computes the values of the operands before
    applying the operator. The recursion effectively builds and evaluates the
    parsing tree for the expression.

    Parameters:
        lexer (Lexer): An instance of the Lexer class, initialized with a string
                       containing the arithmetic expression in prefix notation.

    Returns:
        int: The computed value of the arithmetic expression.

    Raises:
        ValueError: If an unexpected token type is encountered.
        ZeroDivisionError: If a division by zero is attempted.

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
        # Base case: return the value if it's a number
        return int(token.text)

    elif token.kind in Token.operators:
        # Recursive case: evaluate the operands
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
                raise ZeroDivisionError("Division by zero.")
            return a // b

    else:
        raise ValueError(f"Unexpected token type: {token.kind}")

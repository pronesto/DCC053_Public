from Exp import *
from Lexer import *


def parse_infix(lexer) -> Expression:
    """
    Converts an arithmetic expression in Infix Notation to an expression tree.

    This function converts a string into an expression tree, and returns it.

    Parameters:
        lexer (Lexer): An instance of the Lexer class, initialized with a string
                       containing the arithmetic expression in prefix notation.

    Returns:
        Expression: The parsed arithmetic expression.

    Raises:
        ValueError: If an unexpected token type is encountered.

    Examples:
        >>> lexer = Lexer("+ 3 * 4 2")
        >>> e = parse_infix(lexer)
        >>> e.eval()
        11

        >>> lexer = Lexer("+ * 3 4 2")
        >>> e = parse_infix(lexer)
        >>> e.eval()
        14
    """

    token = lexer.next_valid_token()

    if token.kind == TokenType.NUM:
        # Base case: return the value if it's a number
        return Num(int(token.text))

    elif token.kind in Token.operators:
        # Recursive case: evaluate the operands
        a = parse_infix(lexer)
        b = parse_infix(lexer)

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

from Exp import *
from Lexer import *


def parse_infix(lexer):
    """
    Converts an arithmetic expression in Infix Notation to an expression tree.

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

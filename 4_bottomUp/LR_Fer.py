from Lexer import *

def match_and_pop(stack, pattern):
    """
    Check if pattern is a suffix of stack.

    Examples:
        >>> stack = [1, 2, 3, 4, 5]
        >>> match = match_and_pop(stack, [4, 5])
        >>> stack, match
        ([1, 2, 3], True)

        >>> stack = [1, 2, 3, 4, 5]
        >>> match = match_and_pop(stack, [3, 4])
        >>> stack, match
        ([1, 2, 3, 4, 5], False)
    """
    if len(stack) < len(pattern):
        return False
    if stack[-len(pattern):] == pattern:
        stack[-len(pattern):] = []
        return True
    return False

def print_state(state, stack, token):
    print(f"{state} :: {stack} :: {token}")

def shift_0(stack, lexer):
    token = lexer.next_valid_token()
    print_state("shift_0", stack, token.text)
    if token.kind == TokenType.LPR:
        stack.append(TokenType.LPR)
        return 0
    elif token.kind == TokenType.RPR:
        stack.append('P')
        stack.append(TokenType.RPR)
        return 1
    elif token.kind == TokenType.EOF:
        stack.append('S')
        return 2
    else:
        raise ValueError(f"Unknown token: {token.text}")

def reduce_1(stack, _):
    print_state("reduce_1", stack, None)
    if match_and_pop(stack, [TokenType.LPR, 'P', TokenType.RPR]):
        stack.append('P')
        return 3
    if match_and_pop(stack, ['P']):
        stack.append('S')
        return 2
    else:
        raise ValueError("Reduce error")

def reduce_2(stack, _):
    print_state("reduce_2", stack, None)
    if match_and_pop(stack, [TokenType.LPR, 'S']):
        stack.append('S')
        return 2
    elif stack == ['S']:
        return -1
    else:
        raise ValueError("Reduce error")

def shift_3(stack, lexer):
    token = lexer.next_valid_token()
    print_state("shift_3", stack, token.text)
    if token.kind == TokenType.RPR:
        stack.append('P')
        stack.append(TokenType.RPR)
        return 1
    elif token.kind == TokenType.EOF:
        return 1
    else:
        raise ValueError("Reduce error")

state_machine = {0: shift_0, 1: reduce_1, 2: reduce_2, 3: shift_3}

def test_parser(input_str):
    """
    Tests the parser of left-skewed parentheses.

        Example:
    >>> test_parser('()')
    () is valid

    >>> test_parser('(()')
    (() is valid

    >>> test_parser('(')
    ( is valid

    >>> test_parser('())')
    ()) is invalid

    >>> test_parser('(()))')
    (())) is invalid

    >>> test_parser('()()')
    ()() is invalid
    """
    lexer = Lexer(input_str)
    next_state = 0
    stack = []
    try:
        while next_state >= 0:
            action = state_machine[next_state]
            next_state = action(stack, lexer)
        print(f"{input_str} is valid")
    except ValueError as e:
        print(f"{input_str} is invalid")

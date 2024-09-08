from Lexer import *

class LRParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_valid_token()
        self.stack = [0]  # State stack initialized with state 0

        # Action table: (state, token) -> ('shift', next_state) | ('reduce', production) | ('accept')
        self.action_table = {
            (0, TokenType.LPR): ('shift', 1),  # Shift to state 1 on '('
            (1, TokenType.LPR): ('shift', 1),  # Shift to state 1 on '('
            (1, TokenType.RPR): ('shift', 2),  # Shift to state 2 on ')'
            (2, TokenType.RPR): ('reduce', 'P ::= ( P )'),  # Reduce on ')'
            (2, TokenType.EOF): ('accept',),  # Accept on EOF if stack matches the rules
        }

        # Goto table: (state, non-terminal) -> next_state
        self.goto_table = {
            (0, 'S'): 3,  # Goto state 3 on 'S'
            (1, 'P'): 2,  # Goto state 2 on 'P'
        }

    def parse(self):
        while True:
            state = self.stack[-1]
            action = self.action_table.get((state, self.current_token.kind))

            if not action:
                if self.current_token.kind != TokenType.EOF:
                    msg = f"Unexpected token: {self.current_token.kind}"
                    raise ValueError(msg)
                else:
                    return

            if action[0] == 'shift':
                _, next_state = action
                self.stack.append(self.current_token)
                self.stack.append(next_state)
                self.current_token = self.lexer.next_valid_token()

            elif action[0] == 'reduce':
                production = action[1]
                if production == 'P ::= ( P )':
                    self.stack.pop()  # Pop state
                    self.stack.pop()  # Pop token ')'
                    self.stack.pop()  # Pop state
                    self.stack.pop()  # Pop token '('
                    # Now handle the non-terminal reduction
                    non_terminal = 'P'
                    goto_state = self.goto_table.get((self.stack[-1], non_terminal))
                    if goto_state is not None:
                        self.stack.append(non_terminal)
                        self.stack.append(goto_state)
                    else:
                        raise ValueError("Unexpected reduction")
                else:
                    raise ValueError("Unknown reduction")

            elif action[0] == 'accept':
                return

            else:
                raise ValueError("Invalid action in action table")

# Testing the parser with valid and invalid inputs
def test_parser(input_str):
    """
    Tests the parser of left-skewed parentheses.

    Example:
    >>> test_parser('()')
    () is valid.

    >>> test_parser('(()')
    (() is valid.

    >>> test_parser('(')
    ( is valid.

    >>> test_parser('())')
    ()) is invalid: Unexpected reduction

    >>> test_parser('(()))')
    (())) is invalid: Unexpected reduction

    >>> test_parser('()()')
    ()() is invalid: Unexpected token: TokenType.LPR
    """
    lexer = Lexer(input_str)
    parser = LRParser(lexer)
    try:
        parser.parse()
        print(f"{input_str} is valid.")
    except ValueError as e:
        print(f"{input_str} is invalid: {e}")

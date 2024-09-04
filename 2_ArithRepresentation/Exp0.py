class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    """
    Produces the value of an arithmetic expression.

    Examples:
    >>> e = Node('+', Node(23), Node(19))
    >>> evaluate(e)
    42

    >>> e0 = Node('-', Node(23), Node(19))
    >>> e1 = Node('-', Node(20), e0)
    >>> evaluate(e1)
    16
    """
    if node is None:
        return 0
    # Evaluate the a leaf operand.
    if node.left is None and node.right is None:
        return int(node.value)
    # Recursively evaluate the left and right subtrees
    left_val = evaluate(node.left)
    right_val = evaluate(node.right)
    # Apply the operator
    if node.value == "+":
        return left_val + right_val
    elif node.value == "-":
        return left_val - right_val
    elif node.value == "*":
        return left_val * right_val
    elif node.value == "/":
        return left_val / right_val


def print_infix(node):
    """
    This function prints the arithmetic expression in infix notation.

    Examples:
    >>> e = Node('+', Node(23), Node(19))
    >>> print_infix(e)
    '(23+19)'

    >>> e0 = Node('-', Node(23), Node(19))
    >>> e1 = Node('-', Node(20), e0)
    >>> print_infix(e1)
    '(20-(23-19))'
    """
    if node is None:
        return ""
    # If the node is a leaf (operand), just return its value
    if node.left is None and node.right is None:
        return str(node.value)
    # Recursively get the left and right sub-expressions
    left_expr = print_infix(node.left)
    right_expr = print_infix(node.right)
    # Wrap the expression in parentheses
    return f"({left_expr}{node.value}{right_expr})"


def print_postfix(node):
    """
    This function prints the arithmetic expression in postfix notation.

    Examples:
    >>> e = Node('+', Node(23), Node(19))
    >>> print_postfix(e)
    '23 19 + '

    >>> e0 = Node('-', Node(23), Node(19))
    >>> e1 = Node('-', Node(20), e0)
    >>> print_postfix(e1)
    '20 23 19 - - '
    """
    if node is None:
        return ""

    # Recursively get the left and right sub-expressions
    left_expr = print_postfix(node.left)
    right_expr = print_postfix(node.right)

    # Combine left, right, and current node's value
    return f"{left_expr}{right_expr}{node.value} "

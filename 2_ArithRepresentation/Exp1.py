from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def eval(self):
        raise NotImplementedError

class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.
    """
    def __init__(self, num):
        self.num = num
    def eval(self):
        """
        Example:
        >>> e = Num(3)
        >>> e.eval()
        3
        """
        return self.num
    def __str__(self):
        """
        Example:
        >>> e = Num(3)
        >>> print(e)
        3
        """
        return str(self.num)


class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def eval(self):
        raise NotImplementedError

class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.
    """
    def eval(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval()
        7
        """
        return self.left.eval() + self.right.eval()
    def __str__(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> print(e)
        +
        """
        return "+"

class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.
    """
    def eval(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval()
        -1
        """
        return self.left.eval() - self.right.eval()
    def __str__(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> print(e)
        -
        """
        return "-"

class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.
    """
    def eval(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval()
        12
        """
        return self.left.eval() * self.right.eval()
    def __str__(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> print(e)
        *
        """
        return "*"

class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.
    """
    def eval(self):
        """
        Example:
        >>> n1 = Num(28)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval()
        7
        >>> n1 = Num(22)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval()
        5
        """
        return self.left.eval() // self.right.eval()
    def __str__(self):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> print(e)
        /
        """
        return "/"

def evaluate(exp):
    """
    Evaluate an arithmetic expression.

    Examples:
    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e = Div(n1, n2)
    >>> evaluate(e)
    7

    >>> n1 = Num(7)
    >>> n2 = Num(4)
    >>> e = Mul(n1, n2)
    >>> evaluate(e)
    28
    """
    return exp.eval()


def print_infix(exp):
    """
    Evaluate an arithmetic expression.

    Examples:
    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(5)
    >>> e1 = Mul(e0, n3)
    >>> print_infix(e1)
    28
    """
    s = str(exp)
    if isinstance(s, BinaryExpression):
        s = f"({print_infix(exp.left)}) s ({print_infix(exp.right)})"
    return s

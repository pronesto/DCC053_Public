from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    eval():
        Abstract method that should be implemented to evaluate the expression.
    """

    @abstractmethod
    def eval(self):
        raise NotImplementedError


class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.

    Attributes:
    -----------
    num : int
        The numeric value of this expression.

    Methods:
    --------
    eval():
        Returns the numeric value of this expression.

    Examples:
    ---------
    >>> e = Num(3)
    >>> e.eval()
    3
    >>> print(e)
    3
    """

    def __init__(self, num):
        self.num = num

    def eval(self):
        return self.num

    def __str__(self):
        return str(self.num)


class BinaryExpression(Expression):
    """
    Abstract base class for binary expressions.

    Attributes:
    -----------
    left : Expression
        The left operand of the binary expression.
    right : Expression
        The right operand of the binary expression.

    Methods:
    --------
    eval():
        Abstract method that should be implemented to evaluate the binary
        expression.
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

    Methods:
    --------
    eval():
        Returns the result of adding the left and right expressions.
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

    Methods:
    --------
    eval():
        Returns the result of subtracting the right expression from the left.
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

    Methods:
    --------
    eval():
        Returns the result of multiplying the left and right expressions.
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

    Methods:
    --------
    eval():
        Returns the result of dividing the left expression by the right.
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


def print_prefix(exp):
    """
    Evaluate an arithmetic expression.

    Examples:
    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(5)
    >>> e1 = Mul(e0, n3)
    >>> f"{print_prefix(e1)} = {e1.eval()}"
    '* / 28 4 5 = 35'

    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(50)
    >>> e1 = Div(n3, e0)
    >>> e2 = Mul(e1, e0)
    >>> f"{print_prefix(e2)} = {e2.eval()}"
    '* / 50 / 28 4 / 28 4 = 49'
    """
    s = str(exp)
    if isinstance(exp, BinaryExpression):
        s = f"{s} {print_prefix(exp.left)} {print_prefix(exp.right)}"
    return s


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
    '((28) / (4)) * (5)'

    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(50)
    >>> e1 = Div(n3, e0)
    >>> e2 = Mul(e1, e0)
    >>> print_infix(e2)
    '((50) / ((28) / (4))) * ((28) / (4))'
    """
    s = str(exp)
    if isinstance(exp, BinaryExpression):
        s = f"({print_infix(exp.left)}) {s} ({print_infix(exp.right)})"
    return s


def print_postfix(exp):
    """
    Evaluate an arithmetic expression.

    Examples:
    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(5)
    >>> e1 = Mul(e0, n3)
    >>> f"{print_postfix(e1)} = {e1.eval()}"
    '28 4 / 5 * = 35'

    >>> n1 = Num(28)
    >>> n2 = Num(4)
    >>> e0 = Div(n1, n2)
    >>> n3 = Num(50)
    >>> e1 = Div(n3, e0)
    >>> e2 = Mul(e1, e0)
    >>> f"{print_postfix(e2)} = {e2.eval()}"
    '50 28 4 / / 28 4 / * = 49'
    """
    s = str(exp)
    if isinstance(exp, BinaryExpression):
        s = f"{print_postfix(exp.left)} {print_postfix(exp.right)} {s}"
    return s

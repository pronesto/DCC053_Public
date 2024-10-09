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
    def eval(self) -> int:
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

    def __init__(self, num: int) -> None:
        self.num = num

    def eval(self) -> int:
        """
        Evaluate this `Number`.

        Returns:
        --------
        : int
            The value of the evaluated `Number`.
        """

        return self.num

    def __str__(self) -> str:
        """
        Obtain the string representation a `Number`.

        Returns:
        --------
        : str
            The string representation of this `Number`'s value.
        """

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

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left: Expression = left
        self.right: Expression = right

    @abstractmethod
    def eval(self) -> int:
        """
        Evaluate a Binary Expression.

        Returns:
        --------
        : int
            The resulting value of this expression.
        """

        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """
        Obtain the string representation from a Binary Expression.

        Returns:
        --------
        : str
            The string representation of this expression.
        """

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

    def eval(self) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval()
        7

        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> n3 = Num(5)
        >>> add1 = Add(n1, n2)
        >>> add2 = Add(n3, add1)
        >>> add2.eval()
        12
        """

        return self.left.eval() + self.right.eval()

    def __str__(self) -> str:
        """
        Example:
        --------
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

    def eval(self) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval()
        -1

        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> n3 = Num(5)
        >>> sub1 = Sub(n1, n2)
        >>> sub2 = Sub(n3, sub1)
        >>> sub2.eval()
        6
        """

        return self.left.eval() - self.right.eval()

    def __str__(self) -> str:
        """
        Example:
        --------
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

    def eval(self) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval()
        12

        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> n3 = Add(n1, n2)
        >>> mul1 = Mul(n1, n2)
        >>> mul2 = Mul(n3, mul1)
        >>> mul2.eval()
        84
        """

        return self.left.eval() * self.right.eval()

    def __str__(self) -> str:
        """
        Example:
        --------
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

    def eval(self) -> int:
        """
        Examples:
        ---------
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

        >>> zero = Num(0)
        >>> n1 = Num(10)
        >>> n1_prime = Sub(zero, n1)
        >>> n2 = Num(5)
        >>> n2_prime = Sub(zero, n2)
        >>> e = Div(n1_prime, n2_prime)
        >>> e.eval()
        2
        """

        return self.left.eval() // self.right.eval()

    def __str__(self) -> str:
        """
        Example:
        --------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> print(e)
        /
        """

        return "/"


def evaluate(exp: Expression) -> int:
    """
    Evaluate an arithmetic expression.

    Examples:
    ---------
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


def print_prefix(exp: Expression) -> str:
    """
    Obtain the string representation of the expression in prefix notation.

    Examples:
    ---------
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


def print_infix(exp) -> str:
    """
    Obtain the string representation of the expression in infix notation.

    Examples:
    ---------
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


def print_postfix(exp) -> str:
    """
    Obtain the string representation of the expression in postfix notation.

    Examples:
    ---------
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

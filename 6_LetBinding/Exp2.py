import sys

from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    eval(env):
        Abstract method that should be implemented to evaluate the expression.
    """

    @abstractmethod
    def eval(self, env: dict[str, int]) -> int:
        raise NotImplementedError


class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    indentifier is the value associated with it in the environment table.

    Attributes:
    -----------
    identifier : str
        The variable identifier (i.e., its name).

    Methods:
    --------
    eval(env):
        Returns the contents of a variable from a given environment.
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def eval(self, env: dict[str, int]) -> int:
        """
        Examples:
        ---------
        >>> e = Var('var')
        >>> e.eval({'var': 42})
        42

        >>> e = Var('v42')
        >>> e.eval({'v42': True, 'v31': 5})
        True
        """

        if self.identifier in env:
            return env[self.identifier]
        else:
            sys.exit(f"Variavel inexistente {self.identifier}")


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
    eval(env):
        Returns the numeric value of this expression.

    Examples:
    ---------
    >>> e = Num(3)
    >>> e.eval({})
    3
    """

    def __init__(self, num: int) -> None:
        self.num = num

    def eval(self, _) -> int:
        """
        Evaluate this `Number`.

        This method ignores the environment.

        Example:
        --------
        >>> e = Num(3)
        >>> e.eval({})
        3
        """

        return self.num


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
    eval(env):
        Abstract method that should be implemented to evaluate the binary
        expression for some environment.
    """

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left: Expression = left
        self.right: Expression = right

    @abstractmethod
    def eval(self, env: dict[str, int]) -> int:
        """
        Evaluate a Binary Expression.

        Parameters:
        -----------
        env : dict[str, int]
            The environment to evaluate. Maps variables names to values.

        Returns:
        --------
        : int
            The resulting value of this expression.
        """

        raise NotImplementedError


class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.

    Methods:
    --------
    eval(env):
        Returns the result of adding the left and right expressions.
    """

    def eval(self, env: dict[str, int]) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval({})
        7

        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> n3 = Var('some_var')
        >>> add1 = Add(n1, n2)
        >>> add2 = Add(n3, add1)
        >>> add2.eval({'some_var': 5})
        12
        """

        return self.left.eval(env) + self.right.eval(env)


class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.

    Methods:
    --------
    eval(env):
        Returns the result of subtracting the right expression from the left.
    """

    def eval(self, env: dict[str, int]) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval({})
        -1

        >>> n1 = Var('x')
        >>> n2 = Var('y')
        >>> e = Sub(n1, n2)
        >>> e.eval({'x': 23, 'y': 13})
        10
        """

        return self.left.eval(env) - self.right.eval(env)


class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.

    Methods:
    --------
    eval(env):
        Returns the result of multiplying the left and right expressions.
    """

    def eval(self, env: dict[str, int]) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval({})
        12

        >>> n1 = Num(2)
        >>> n2 = Var('x')
        >>> n3 = Var('y')
        >>> n4 = Add(n1, n2)
        >>> e = Mul(n3, n4)
        >>> e.eval({'x': 5, 'y': 7})
        49
        """

        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.

    Methods:
    --------
    eval(env):
        Returns the result of dividing the left expression by the right.
    """

    def eval(self, env: dict[str, int]) -> int:
        """
        Examples:
        ---------
        >>> n1 = Num(28)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval({})
        7
        >>> n1 = Num(22)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval({})
        5

        >>> x = Var('x')
        >>> n1 = Num(10)
        >>> n1_prime = Sub(x, n1)
        >>> n2 = Var('y')
        >>> n2_prime = Sub(x, n2)
        >>> e = Div(n1_prime, n2_prime)
        >>> e.eval({'x': 0, 'y': 5})
        2
        """

        return self.left.eval(env) // self.right.eval(env)


class Let(Expression):
    """
    This class represents a `let` expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:

    1. Evaluate `e0` in the environment `env`, yielding `e0_val`
    2. Evaluate `e1` in the new environment `env'` = `env` + {v: `e0_val`}

    Methods:
    --------
    eval(env):
        Returns the value assigned to the variable.
    """

    def __init__(self, identifier: str, exp_def: Expression, exp_body: Var) -> None:
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def eval(self, env: dict[str, int]) -> None:
        """
        Examples:
        ---------
        >>> e = Let(identifier='v', exp_def=Num(42), exp_body=Var('v'))
        >>> e.eval({})
        42

        >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
        >>> e.eval({})
        42

        >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
        >>> e.eval({})
        1764
        """

        e0_val = self.exp_def.eval(env)

        new_env = dict(env)
        new_env[self.identifier] = e0_val

        return self.exp_body.eval(new_env)

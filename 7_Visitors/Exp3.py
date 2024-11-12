import sys
from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class for expressions. All derived classes must implement
    the `eval` method.
    """

    @abstractmethod
    def eval(self, env):
        raise NotImplementedError


class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    indentifier is the value associated with it in the environment table.

    Attributes:
        identifier (str): The name of the variable.
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def eval(self, env):
        """
        Evaluates the variable in the given environment.

        Parameters:
            env (dict): The environment containing variable bindings.

        Returns:
            The value associated with the identifier in the environment.

        Example:
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

    def size(self):
        """
        Returns the size of the expression.

        Example:
        >>> e = Var('var')
        >>> e.size()
        1
        """
        return 1

    def __str__(self):
        """
        Example:
        >>> e = Var('var')
        >>> print(e)
        var
        """
        return self.identifier


class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.

    Attributes:
        num (int or float): The number value.
    """

    def __init__(self, num):
        self.num = num

    def eval(self, _):
        """
        Evaluates the number.

        Example:
        >>> e = Num(3)
        >>> e.eval(None)
        3
        """
        return self.num

    def size(self):
        """
        Returns the size of the expression.

        Example:
        >>> e = Num(3)
        >>> e.size()
        1
        """
        return 1

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

    Attributes:
        left (Expression): The left operand.
        right (Expression): The right operand.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def eval(self, env):
        raise NotImplementedError

    def size(self):
        """
        Returns the size of the binary expression, which is the sum of
        the sizes of its two subexpressions plus one for the operator.

        Example:
        >>> e = Add(Var('x'), Num(2))
        >>> e.size()
        3
        """
        return 1 + self.left.size() + self.right.size()


class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.

    Attributes:
        left (Expression): The left operand.
        right (Expression): The right operand.
    """

    def eval(self, env):
        """
        Evaluates the sum of the two subexpressions.

        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval(None)
        7
        """
        return self.left.eval(env) + self.right.eval(env)

    def __str__(self):
        """
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> print(e)
        (3 + 4)
        """
        return f"({str(self.left)} + {str(self.right)})"


class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.

    Attributes:
        left (Expression): The left operand.
        right (Expression): The right operand.
    """

    def eval(self, env):
        """
        Evaluates the difference between the two subexpressions.

        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval(None)
        -1
        """
        return self.left.eval(env) - self.right.eval(env)

    def __str__(self):
        """
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> print(e)
        (3 - 4)
        """
        return f"({str(self.left)} - {str(self.right)})"


class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.

    Attributes:
        left (Expression): The left operand.
        right (Expression): The right operand.
    """

    def eval(self, env):
        """
        Evaluates the product of the two subexpressions.

        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval(None)
        12
        """
        return self.left.eval(env) * self.right.eval(env)

    def __str__(self):
        """
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> print(e)
        (3 * 4)
        """
        return f"({str(self.left)} * {str(self.right)})"


class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.

     Attributes:
        left (Expression): The left operand.
        right (Expression): The right operand.
    """

    def eval(self, env):
        """
        Evaluates the integer division of the two subexpressions.

        Example:
        >>> n1 = Num(28)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval(None)
        7
        >>> n1 = Num(22)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> e.eval(None)
        5
        """
        return self.left.eval(env) // self.right.eval(env)

    def __str__(self):
        """
        >>> n1 = Num(28)
        >>> n2 = Num(4)
        >>> e = Div(n1, n2)
        >>> print(e)
        (28 / 4)
        """
        return f"({str(self.left)} / {str(self.right)})"


class Let(Expression):
    """
    This class represents a let expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:
    1. Evaluate e0 in the environment env, yielding e0_val
    2. Evaluate e1 in the new environment env' = env + {v:e0_val}

    Attributes:
        identifier (str): The variable name.
        exp_def (Expression): The expression defining the variable.
        exp_body (Expression): The expression to evaluate using the variable.
    """

    def __init__(self, identifier, exp_def, exp_body):
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def eval(self, env):
        """
        Evaluates the let expression by first evaluating the defining expression,
        then evaluating the body in the extended environment.

        Example:
        >>> e = Let('v', Num(42), Var('v'))
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

    def size(self):
        """
        Returns the size of the let expression, which is the size of its two
        subexpressions plus two for the variable binding.

        Example:
        >>> e = Let('v', Num(42), Var('v'))
        >>> e.size()
        4

        >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
        >>> e.size()
        9

        >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
        >>> e.size()
        8
        """
        return 2 + self.exp_def.size() + self.exp_body.size()

    def __str__(self):
        """
        >>> e = Let('v', Num(42), Var('v'))
        >>> print(e)
        let v = 42 in v end

        >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
        >>> print(e)
        let v = 40 in let w = 2 in (v + w) end end

        >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
        >>> print(e)
        let v = (40 + 2) in (v * v) end
        """
        str_def = str(self.exp_def)
        str_body = str(self.exp_body)
        return f"let {self.identifier} = {str_def} in {str_body} end"

import sys
from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def eval(self, env):
        raise NotImplementedError

class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    indentifier is the value associated with it in the environment table.
    """
    def __init__(self, identifier):
        self.identifier = identifier
    def eval(self, env):
        """
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

class Bln(Expression):
    """
    This class represents expressions that are boolean values. There are only
    two boolean values: true and false. The evaluation of such an expression is
    the boolean itself.
    """
    def __init__(self, bln):
        self.bln = bln
    def eval(self, _):
        """
        Example:
        >>> e = Bln(True)
        >>> e.eval(None)
        True
        """
        return self.bln

class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.
    """
    def __init__(self, num):
        self.num = num
    def eval(self, _):
        """
        Example:
        >>> e = Num(3)
        >>> e.eval(None)
        3
        """
        return self.num

class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def eval(self, env):
        raise NotImplementedError

class Eql(BinaryExpression):
    """
    This class represents the equality between two expressions. The evaluation
    of such an expression is True if the subexpressions are the same, or false
    otherwise.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Eql(n1, n2)
        >>> e.eval(None)
        False

        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Eql(n1, n2)
        >>> e.eval(None)
        True
        """
        return self.left.eval(env) == self.right.eval(env)

class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Add(n1, n2)
        >>> e.eval(None)
        7
        """
        return self.left.eval(env) + self.right.eval(env)

class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Sub(n1, n2)
        >>> e.eval(None)
        -1
        """
        return self.left.eval(env) - self.right.eval(env)

class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Mul(n1, n2)
        >>> e.eval(None)
        12
        """
        return self.left.eval(env) * self.right.eval(env)

class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.
    """
    def eval(self, env):
        """
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

class Leq(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than-or-equal comparator. The evaluation of such an expression is a
    boolean value that is true if the left operand is less than or equal the
    right operand. It is false otherwise.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Leq(n1, n2)
        >>> e.eval(None)
        True
        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Leq(n1, n2)
        >>> e.eval(None)
        True
        >>> n1 = Num(4)
        >>> n2 = Num(3)
        >>> e = Leq(n1, n2)
        >>> e.eval(None)
        False
        """
        return self.left.eval(env) <= self.right.eval(env)

class Lth(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than comparison operator. The evaluation of such an expression is a
    boolean value that is true if the left operand is less than the right
    operand. It is false otherwise.
    """
    def eval(self, env):
        """
        Example:
        >>> n1 = Num(3)
        >>> n2 = Num(4)
        >>> e = Lth(n1, n2)
        >>> e.eval(None)
        True
        >>> n1 = Num(3)
        >>> n2 = Num(3)
        >>> e = Lth(n1, n2)
        >>> e.eval(None)
        False
        >>> n1 = Num(4)
        >>> n2 = Num(3)
        >>> e = Lth(n1, n2)
        >>> e.eval(None)
        False
        """
        return self.left.eval(env) < self.right.eval(env)

class UnaryExpression(Expression):
    """
    This class represents unary expressions. A unary expression has only one
    sub-expression.
    """
    def __init__(self, exp):
        self.exp = exp

    @abstractmethod
    def eval(self, env):
        raise NotImplementedError

class Neg(UnaryExpression):
    """
    This expression represents the additive inverse of a number. The additive
    inverse of a number n is the number -n, so that the sum of both is zero.
    """
    def eval(self, env):
        """
        Example:
        >>> n = Num(3)
        >>> e = Neg(n)
        >>> e.eval(None)
        -3
        >>> n = Num(0)
        >>> e = Neg(n)
        >>> e.eval(None)
        0
        """
        return -self.exp.eval(env)

class Not(UnaryExpression):
    """
    This expression represents the negation of a boolean. The negation of a
    boolean expression is the logical complement of that expression.
    """
    def eval(self, env):
        """
        Example:
        >>> t = Bln(True)
        >>> e = Not(t)
        >>> e.eval(None)
        False
        >>> t = Bln(False)
        >>> e = Not(t)
        >>> e.eval(None)
        True
        """
        return not(self.exp.eval(env))

class Let(Expression):
    """
    This class represents a let expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:
    1. Evaluate e0 in the environment env, yielding e0_val
    2. Evaluate e1 in the new environment env' = env + {v:e0_val}
    """
    def __init__(self, identifier, exp_def, exp_body):
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body
    def eval(self, env):
        """
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
        new_env[self.identifier]= e0_val
        return self.exp_body.eval(new_env)

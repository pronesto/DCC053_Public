import sys
from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class representing an expression.

    Attributes:
        None
    """

    @abstractmethod
    def accept(self, visitor):
        """
        Accepts a visitor that will perform an operation on the expression.

        Args:
            visitor: The visitor performing operations on the expression.

        Returns:
            The result of the visitor's operation.
        """
        pass


class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    indentifier is the value associated with it in the environment table.

    Attributes:
        identifier (str): The name of the identifier.

    Example:
    >>> v = Var('x')
    >>> v.identifier
    'x'
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def accept(self, visitor, arg):
        return visitor.visit_var(self, arg)


class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.

    Attributes:
        num (int): The value of the numeric expression.

    Example:
    >>> n = Num(5)
    >>> n.num
    5
    """

    def __init__(self, num):
        self.num = num

    def accept(self, visitor, arg):
        return visitor.visit_num(self, arg)


class Bln(Expression):
    """
    This class represents expressions that are boolean values. There are only
    two boolean values: true and false. The acceptation of such an expression is
    the boolean itself.

    Attributes:
        bln (bool): The boolean value.

    Example:
    >>> b = Bln(True)
    >>> b.bln
    True
    """

    def __init__(self, bln):
        self.bln = bln

    def accept(self, visitor, arg):
        return visitor.visit_bln(self, arg)


class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.

    Attributes:
        left (Expression): The left sub-expression.
        right (Expression): The right sub-expression.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right


class And(BinaryExpression):
    """
    This class represents the logical disjunction of two boolean expressions.
    The evaluation of an expression of this kind is the logical AND of the two
    subexpression's values.

    Example:
    >>> e = And(Bln(True), Bln(False))
    >>> v = VisitorEval()
    >>> e.accept(v, {})
    False
    """

    def accept(self, visitor, arg):
        return visitor.visit_and(self, arg)


class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.

    Example:
    >>> e = Add(Num(5), Num(3))
    >>> v = VisitorEval()
    >>> e.accept(v, {})
    8
    """

    def accept(self, visitor, arg):
        return visitor.visit_add(self, arg)


class Lth(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than comparison operator. The acceptuation of such an expression is a
    boolean value that is true if the left operand is less than the right
    operand. It is false otherwise.

    Example:
    >>> e = Lth(Num(2), Num(5))
    >>> v = VisitorEval()
    >>> e.accept(v, {})
    True
    """

    def accept(self, visitor, arg):
        return visitor.visit_lth(self, arg)


class Let(Expression):
    """
    This class represents a let expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:
    1. Evaluate e0 in the environment env, yielding e0_val
    2. Evaluate e1 in the new environment env' = env + {v:e0_val}

    Example:
    >>> e = Let('x', Num(10), Var('x'))
    >>> v = VisitorEval()
    >>> e.accept(v, {})
    10
    """

    def __init__(self, identifier, exp_def, exp_body):
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(self, visitor, arg):
        return visitor.visit_let(self, arg)


class IfThenElse(Expression):
    """
    This class represents a conditional expression. The semantics an expression
    such as 'if B then E0 else E1' is as follows:
    1. Evaluate B. Call the result ValueB.
    2. If ValueB is True, then evalute E0 and return the result.
    3. If ValueB is False, then evaluate E1 and return the result.
    Notice that we only evaluate one of the two sub-expressions, not both. Thus,
    "if True then 0 else 1 div 0" will return 0 indeed.

    Example:
    >>> e = IfThenElse(Bln(True), Num(1), Num(0))
    >>> v = VisitorEval()
    >>> e.accept(v, {})
    1
    """

    def __init__(self, cond, e0, e1):
        self.cond = cond
        self.e0 = e0
        self.e1 = e1

    def accept(self, visitor, arg):
        return visitor.visit_ifThenElse(self, arg)


class VisitorEval:
    """
    Pretty print an expression based on its type.

    Example:
    >>> e = Let('v', Num(42), Var('v'))
    >>> v = VisitorEval()
    >>> print(e.accept(v, {}))
    42

    >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
    >>> v = VisitorEval()
    >>> print(e.accept(v, {}))
    42
    """

    def visit_var(self, var, env):
        if var.identifier in env:
            return env[var.identifier]
        else:
            sys.exit(f"Variavel inexistente {var.identifier}")

    def visit_num(self, num, env):
        return num.num

    def visit_bln(self, exp, env):
        return exp.bln

    def visit_add(self, add, env):
        return add.left.accept(self, env) + add.right.accept(self, env)

    def visit_and(self, exp, env):
        val_left = exp.left.accept(self, env)
        if val_left:
            return exp.right.accept(self, env)
        return False

    def visit_lth(self, exp, env):
        val_left = exp.left.accept(self, env)
        val_right = exp.right.accept(self, env)
        return val_left < val_right

    def visit_ifThenElse(self, exp, env):
        cond = exp.cond.accept(self, env)
        if cond:
            return exp.e0.accept(self, env)
        else:
            return exp.e1.accept(self, env)

    def visit_let(self, let, env):
        e0_val = let.exp_def.accept(self, env)
        new_env = dict(env)
        new_env[let.identifier] = e0_val
        return let.exp_body.accept(self, new_env)


class VisitorTypePropagator:
    """
    Visitor that performs type propagation.

    Example:
    >>> e0 = Let('w', Num(2), Add(Var('v'), Var('w')))
    >>> e1 = Let('v', Num(40), e0)
    >>> find_type(e1)
    <class 'int'>
    """

    def visit_var(self, var, env):
        if var.identifier in env:
            return env[var.identifier]
        else:
            raise TypeError(f"Variavel inexistente {var.identifier}")

    def visit_num(self, num, env):
        return int

    def visit_bln(self, exp, env):
        return bool

    def visit_add(self, add, env):
        left_type = add.left.accept(self, env)
        right_type = add.right.accept(self, env)
        if left_type == int and right_type == int:
            return int
        raise TypeError(f"Type error: {left_type} + {right_type}")

    def visit_lth(self, exp, env):
        left_type = exp.left.accept(self, env)
        right_type = exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return bool
        raise TypeError(f"Type error: {left_type} < {right_type}")

    def visit_and(self, add, env):
        left_type = add.left.accept(self, env)
        right_type = add.right.accept(self, env)
        if left_type == bool and right_type == bool:
            return bool
        raise TypeError(f"Type error: {left_type} and {right_type}")

    def visit_ifThenElse(self, exp, env):
        cond_type = exp.cond.accept(self, env)
        e0_type = exp.e0.accept(self, env)
        e1_type = exp.e1.accept(self, env)
        if cond_type == bool and e0_type == e1_type:
            return e0_type
        else:
            then_str = f"then branch is {e0_type}"
            else_str = f"else branch is {e1_type}"
            raise TypeError(f"Type error: {then_str}, {else_str}")

    def visit_let(self, let, env):
        exp_def_type = let.exp_def.accept(self, env)
        new_env = dict(env)
        new_env[let.identifier] = exp_def_type
        return let.exp_body.accept(self, new_env)


def find_type(e):
    """
    Finds the type of an expression via type propagation.

    Example:
    >>> e0 = Let('w', Num(2), Add(Var('v'), Var('w')))
    >>> e1 = Let('v', Num(40), e0)
    >>> find_type(e1)
    <class 'int'>

    >>> e0 = Let('w', Bln(True), And(Var('v'), Var('w')))
    >>> e1 = Let('v', Bln(False), e0)
    >>> find_type(e1)
    <class 'bool'>

    >>> e = IfThenElse(Bln(True), Num(0), Num(42))
    >>> find_type(e)
    <class 'int'>
    """
    v = VisitorTypePropagator()
    return e.accept(v, {})

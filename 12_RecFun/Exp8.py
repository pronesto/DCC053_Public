"""
This is the implementation of the language with functions using dynamic
scoping rules. It does not support closures.
"""

import sys
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    indentifier is the value associated with it in the environment table.
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def accept(self, visitor, arg):
        return visitor.visit_var(self, arg)


class Num(Expression):
    """
    This class represents expressions that are numbers. The evaluation of such
    an expression is the number itself.
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
    """

    def __init__(self, bln):
        self.bln = bln

    def accept(self, visitor, arg):
        return visitor.visit_bln(self, arg)


class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right


class And(BinaryExpression):
    """
    This class represents the logical disjunction of two boolean expressions.
    The evaluation of an expression of this kind is the logical AND of the two
    subexpression's values.
    """

    def accept(self, visitor, arg):
        return visitor.visit_and(self, arg)


class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.
    """

    def accept(self, visitor, arg):
        return visitor.visit_add(self, arg)


class Lth(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than comparison operator. The acceptuation of such an expression is a
    boolean value that is true if the left operand is less than the right
    operand. It is false otherwise.
    """

    def accept(self, visitor, arg):
        return visitor.visit_lth(self, arg)


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
    """

    def __init__(self, cond, e0, e1):
        self.cond = cond
        self.e0 = e0
        self.e1 = e1

    def accept(self, visitor, arg):
        return visitor.visit_ifThenElse(self, arg)


class Fn(Expression):
    """
    This class represents an anonymous function.

        >>> f = Fn('v', Add(Var('v'), Var('v')))
        >>> ev = VisitorEval()
        >>> print(f.accept(ev, {}))
        Fn(v)
    """

    def __init__(self, formal, body):
        self.formal = formal
        self.body = body

    def accept(self, visitor, arg):
        return visitor.visit_fn(self, arg)


class App(Expression):
    """
    This class represents a function application, such as 'e0 e1'. The semantics
    of an application is as follows: we evaluate the left side, e.g., e0. It
    must result into a function fn(p, b) denoting a function that takes in a
    parameter p and evaluates a body b. We then evaluates e1, to obtain a value
    v. Finally, we evaluate b, but in a context where p is bound to v.

    Examples:
        >>> f = Fn('v', Add(Var('v'), Var('v')))
        >>> e = App(f, Add(Num(40), Num(2)))
        >>> ev = VisitorEval()
        >>> e.accept(ev, {})
        84

        >>> f = Fn('v', Add(Var('v'), Var('w')))
        >>> e = Let('w', Num(3), App(f, Num(2)))
        >>> ev = VisitorEval()
        >>> e.accept(ev, {})
        5

        >>> e = Let('f', Fn('x', Add(Var('x'), Num(1))), App(Var('f'), Num(1)))
        >>> ev = VisitorEval()
        >>> e.accept(ev, {})
        2

        >>> e0 = Let('w', Num(3), App(Var('f'), Num(1)))
        >>> e1 = Let('f', Fn('v', Add(Var('v'), Var('w'))), e0)
        >>> e2 = Let('w', Num(2), e1)
        >>> ev = VisitorEval()
        >>> e2.accept(ev, {})
        4
    """

    def __init__(self, function, actual):
        self.function = function
        self.actual = actual

    def accept(self, visitor, arg):
        return visitor.visit_app(self, arg)


class Function:
    """
    This is the class that represents functions. This class lets us distinguish
    the three types that now exist in the language: numbers, booleans and
    functions. Notice that the evaluation of an expression can now be a
    function. For instance:

    Example:
        >>> f = Function('v', Add(Var('v'), Var('v')))
        >>> print(str(f))
        Fn(v)
    """

    def __init__(self, formal, body):
        self.formal = formal
        self.body = body

    def __str__(self):
        return f"Fn({self.formal})"


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

    def visit_fn(self, exp, env):
        return Function(exp.formal, exp.body)

    def visit_app(self, exp, env):
        fval = exp.function.accept(self, env)
        if not isinstance(fval, Function):
            sys.exit("Type error")
        pval = exp.actual.accept(self, env)
        new_env = dict(env)
        new_env[fval.formal] = pval
        return fval.body.accept(self, new_env)

def create_loop(value):
    """
    The goal of this example is to demonstrate that some form of recursion is
    possible in the language with dynamic scope.

    To this end, we create the following function:

    let
      loop = fn x =>
        if 0 < x
        then x + loop (x - 1)
        else 0
      in
        loop value
      end

    Example:
        >>> program = create_loop(5)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        15
    """
    lth_exp = Lth(Num(0), Var('x'))
    rec_app = Add(Var('x'), App(Var('loop'), Add(Var('x'), Num(-1))))
    body = IfThenElse(lth_exp, rec_app, Num(0))
    fn_loop = Fn('x', body)
    return Let('loop', fn_loop, App(Var('loop'), Num(value)))

def create_closure(v0, v1):
    """
    The goal of this test is to demonstrate that our language with dynamic
    scope cannot handle closures. We shall use the following code:

    let
      f = fn x => fn y => x + y
    in
      f v0 v1
    end

    In this case, the variable 'x' will not be defined upon evaluating the
    expression 'x + y'. This happens because the application (f v0) returns a
    function Fn('y', x + y), but it does not return the environment where the
    application happen; hence, the value of 'x' is discarded.

    Example:
        >>> program = create_closure(2, 7)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        Traceback (most recent call last):
        ...
        SystemExit: Variavel inexistente x
    """
    func_dec = Fn('x', Fn('y', Add(Var('x'), Var('y'))))
    let_body = App(App(Var('f'), Num(v0)), Num(v1))
    return Let('f', func_dec, let_body)


def create_arithmetic_sum(init_value, end_value):
    """
    The goal of this example is to demonstrate that the language with
    dynamic scope does not support recursive closures.

    To this end, we create the following function:

    let
      range = fn n0 = fn n1 =>
        if n0 < n1
        then n0 + range (n0 + 1) n1
        else 0
      in
        range 2 7
      end

    Example:
        >>> program = create_arithmetic_sum(2, 7)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        Traceback (most recent call last):
        ...
        SystemExit: Variavel inexistente n0
    """
    # Inner recursive function call range (n0 + 1) n1
    recursive_call = App(App(Var('range'), Add(Var('n0'), Num(1))), Var('n1'))

    # If-then-else statement: if n0 < n1 then n0 + range (n0 + 1) n1 else 0
    body = IfThenElse(
        Lth(Var('n0'), Var('n1')),       # Condition: n0 < n1
        Add(Var('n0'), recursive_call),  # Then: n0 + range (n0 + 1) n1
        Num(0)                           # Else: 0
    )

    # The inner function: fn n1 => ...
    fn_n1 = Fn('n1', body)

    # The outer function: fn n0 => ...
    fn_n0 = Fn('n0', fn_n1)

    # Let expression: let range = fn n0 => fn n1 => ... in range 2 7 end
    program = Let(
        'range',                         # Name of the bound function: range
        fn_n0,              # The function itself: fn n0 => fn n1 => ...
        App(App(Var('range'), Num(init_value)), Num(end_value))
    )

    return program

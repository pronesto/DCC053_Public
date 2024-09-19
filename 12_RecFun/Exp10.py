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


class Fun(Fn):
    """
    This class represents a named function. Named functions can be invoked
    recursively.

        >>> f = Fun('f', 'v', Add(Var('v'), Var('v')))
        >>> ev = VisitorEval()
        >>> print(f.accept(ev, {}))
        Fun f(v)
    """

    def __init__(self, name, formal, body):
        super().__init__(formal, body)
        self.name = name

    def accept(self, visitor, arg):
        return visitor.visit_fun(self, arg)


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
        3
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

        >>> f = Function('v', Add(Var('v'), Var('v')), {})
        >>> print(str(f))
        Fn(v)
    """

    def __init__(self, formal, body, env):
        self.formal = formal
        self.body = body
        self.env = env

    def __str__(self):
        return f"Fn({self.formal})"


class RecFunction(Function):
    """
    This is the class that represents named functions. The key different between
    named and anonymous functions is exactly the "name" :)

        >>> f = RecFunction('f', 'v', Add(Var('v'), Var('v')), {})
        >>> print(str(f))
        Fun f(v)
    """

    def __init__(self, name, formal, body, env):
        super().__init__(formal, body, env)
        self.name = name

    def __str__(self):
        return f"Fun {self.name}({self.formal})"


class VisitorEval:
    """
    Evaluates an expression with recursive functions.

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
        return Function(exp.formal, exp.body, env)

    def visit_fun(self, exp, env):
        return RecFunction(exp.name, exp.formal, exp.body, env)

    def visit_app(self, exp, env):
        """
        The application of function to actual parameter must contain two cases:
        1. An anonymous function is applied: (fn x => x + 1) 2
        2. A named function is applied: f 2, where f is fun f a = a + a
        The only difference between these two cases is that in the second we
        must augment the environment with the name of the named function.

        Example:
        >>> f = Fun('f', 'v', Add(Var('v'), Var('v')))
        >>> e0 = Let('f', f, App(Var('f'), Num(2)))
        >>> ev = VisitorEval()
        >>> e0.accept(ev, {})
        4
        """
        fval = exp.function.accept(self, env)
        if isinstance(fval, Function):
            pval = exp.actual.accept(self, env)
            new_env = dict(fval.env)
            new_env[fval.formal] = pval
            if isinstance(fval, RecFunction):
                new_env[fval.name] = fval
            return fval.body.accept(self, new_env)
        else:
            sys.exit("Type error")

def create_arithmetic_sum(init_value, end_value):
    """
    This function creates the following function:

    let
      fun range n0 = fn n1 =>
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
        20

        >>> program = create_arithmetic_sum(1, 8)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        28
    """
    # The inner body of the function:
    # if n0 < n1 then n0 + range (n0 + 1) n1 else 0
    body = IfThenElse(
        Lth(Var('n0'), Var('n1')),  # Condition: n0 < n1
        Add(Var('n0'), App(            # Then: n0 + range (n0 + 1) n1
            App(Var('range'), Add(Var('n0'), Num(1))),  # range (n0 + 1)
            Var('n1')
        )),
        Num(0)  # Else: 0
    )
   
    # Anonymous function: fn n1 => ...
    fn_n1 = Fn('n1', body)
   
    # Recursive function: fun range n0 = fn n1 => ...
    fun_range = Fun('range', 'n0', fn_n1)
   
    # Application: range init_value end_value
    app_range = App(
        App(Var('range'), Num(init_value)),  # range 2
        Num(end_value)                      # range 2 7
    )
   
    # Whole program:
    return Let('range', fun_range, app_range)

def create_loop(num_iterations):
    """
    This function creates the following function:

    let
      fun loop n = fn f => fn a =>
        if n = 1
        then a
        else loop (n-1) f (f a)
    in
      loop num_iterations (fn x => x + 1) 2
    end

    Example:
        >>> program = create_loop(10)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        11
    """
    # The body of the recursive function:
    # if n = 1 then a else loop (n - 1) f (f a)
    body = IfThenElse(
        Lth(Var('n'), Num(2)),           # Condition: n < 2)
        Var('a'),                        # Then: a
        App(                             # Else: loop (n-1) f (f a)
            App(App(Var('loop'), Add(Var('n'), Num(-1))),  # loop (n - 1)
                Var('f')),
            App(Var('f'), Var('a'))      # f a
        )
    )
   
    # Anonymous function fn a => ...
    fn_a = Fn('a', body)
   
    # Anonymous function fn f => fn a => ...
    fn_f = Fn('f', fn_a)
   
    # Recursive function fun loop n = fn f => fn a => ...
    fun_loop = Fun('loop', 'n', fn_f)
   
    # Application: loop num_iterations (fn x => x + 1) 2
    app_loop = App(
        App(App(Var('loop'), Num(num_iterations)),  # loop num_iterations
            Fn('x', Add(Var('x'), Num(1)))),         # (fn x => x + 1)
        Num(2)                                      # 2
    )
   
    # Whole program:
    return Let('loop', fun_loop, app_loop)

def create_for_loop(begin, end, function):
    """
    This function parameterizes our loops with the begin and end of the
    iterations, plus a high order function that simulates the body of the loop.

    Example:
        >>> program = create_for_loop(2, 10, Fn('x', Add(Var('x'), Num(1))))
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        11

        >>> double = Fn('x', Add(Var('x'), Var('x')))
        >>> program = create_for_loop(2, 10, double)
        >>> v = VisitorEval()
        >>> program.accept(v, {})
        1024
    """
    # The body of the recursive function:
    # if n = 1 then a else loop (n - 1) f (f a)
    body = IfThenElse(
        Lth(Var('n'), Num(2)),           # Condition: n < 2)
        Var('a'),                        # Then: a
        App(                             # Else: loop (n-1) f (f a)
            App(App(Var('loop'), Add(Var('n'), Num(-1))),  # loop (n - 1)
                Var('f')),
            App(Var('f'), Var('a'))      # f a
        )
    )
   
    # Anonymous function fn a => ...
    fn_a = Fn('a', body)
   
    # Anonymous function fn f => fn a => ...
    fn_f = Fn('f', fn_a)
   
    # Recursive function fun loop n = fn f => fn a => ...
    fun_loop = Fun('loop', 'n', fn_f)
   
    # Application: loop num_iterations (fn x => x + 1) 2
    app_loop = App(
        App(App(Var('loop'), Num(end)), function),
        Num(begin)
    )
   
    # Whole program:
    return Let('loop', fun_loop, app_loop)

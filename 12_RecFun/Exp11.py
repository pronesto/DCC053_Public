from abc import ABC, abstractmethod
from typing import Union


class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    accept(visitor, arg):
        Abstract method that should be implemented to accept a visitor.
    """

    @abstractmethod
    def accept(self, visitor):
        pass


class Var(Expression):
    """
    This class represents expressions that are identifiers. The value of an
    identifier is the value associated with it in the environment table.

    Attributes:
    -----------
    identifier : str
        The variable identifier (i.e., its name).

    Methods:
    --------
    accept(visitor, arg):
        Returns the result from the `visit_var` method of the given `visitor`,
        considering some environment defined in `arg`.

    Examples:
    ---------
    >>> var = Var("abc")
    >>> visitor = VisitorEval()
    >>> arg = {"abc": 23}
    >>> var.accept(visitor, arg)
    23

    >>> var = Var("some_var")
    >>> visitor = VisitorEval()
    >>> arg = {"some_var": True}
    >>> var.accept(visitor, arg)
    True
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def accept(
        self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]
    ) -> Union[bool, int]:
        """
        Accept a visitor in this variable.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, Union[bool, int]]
            The environment to evaluate.

        Returns:
        --------
        : Union[bool, int]
            The contents of this variable in the given enviroment.
        """

        return visitor.visit_var(self, arg)


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
    accept(visitor, arg):
        Returns the result from the `visit_num` method of the given `visitor`.

    Examples:
    ---------
    >>> num = Num(23)
    >>> visitor = VisitorEval()
    >>> arg = {"abc": 123}
    >>> num.accept(visitor, arg)
    23
    """

    def __init__(self, num: int) -> None:
        self.num = num

    def accept(
        self,
        visitor: "VisitorEval",
        arg: dict[str, Union[bool, int]],
    ) -> int:
        """
        Accept a visitor in this number.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : int
            The value of this number.
        """

        return visitor.visit_num(self, arg)


class Bln(Expression):
    """
    This class represents expressions that are boolean values. There are only
    two boolean values: `True` and `False`. The acceptation of such an
    expression is the boolean itself.

    Attributes:
    -----------
    bln : bool
        The boolean value of this expression.

    Methods:
    --------
    accept(visitor, arg):
        Returns the result from the `visit_bln` method of the given `visitor`.

    Examples:
    ---------
    >>> bln = Bln(True)
    >>> visitor = VisitorEval()
    >>> arg = {}
    >>> bln.accept(visitor, arg)
    True
    """

    def __init__(self, bln: bool) -> None:
        self.bln = bln

    def accept(
        self,
        visitor: "VisitorEval",
        arg: dict[str, Union[bool, int]],
    ) -> bool:
        """
        Accept a visitor in this boolean.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, Union[bool, int]]
            The environment to evaluate.

        Returns:
        --------
        : bool
            The value of this boolean.
        """

        return visitor.visit_bln(self, arg)


class BinaryExpression(Expression):
    """
    This class represents binary expressions. A binary expression has two
    sub-expressions: the left operand and the right operand.

    Attributes:
    -----------
    left : Expression
        The left operand of the binary expression.
    right : Expression
        The right operand of the binary expression.

    Methods:
    --------
    accept(visitor, arg):
        Abstract method that should be implemented to accept a visit in each
        subclass.
    """

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    @abstractmethod
    def accept(
        self,
        visitor: "VisitorEval",
        arg: dict[str, Union[bool, int]],
    ) -> Union[bool, int]:
        """
        Accept a visitor in this binary expression.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, Union[bool, int]]
            The environment to evaluate.

        Returns:
        --------
        : Union[int, bool]
            The resulting value of this binary expression.
        """

        pass


class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the result of addition between the left and right
        expressions.

    Examples:
    ---------
    >>> add = Add(left=Num(23), right=Var("a"))
    >>> visitor = VisitorEval()
    >>> arg = {"a": 1}
    >>> add.accept(visitor, arg)
    24
    """

    def accept(self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]) -> int:
        return visitor.visit_add(self, arg)


class And(BinaryExpression):
    """
    This class represents the logical disjunction of two boolean expressions.
    The evaluation of an expression of this kind is the logical AND of the two
    subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the type or the result of conjunction between the left and right
        expressions.

    Examples:
    ---------
    >>> _and = And(left=Bln(True), right=Var("a"))
    >>> visitor = VisitorEval()
    >>> arg = {"a": True}
    >>> _and.accept(visitor, arg)
    True

    >>> _and = And(left=Var("a"), right=Var("b"))
    >>> visitor = VisitorEval()
    >>> arg = {"a": True, "b": False}
    >>> _and.accept(visitor, arg)
    False
    """

    def accept(self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]) -> bool:
        return visitor.visit_and(self, arg)


class Lth(BinaryExpression):
    """
    This class represents comparison of two expressions using the
    less-than comparison operator. The acceptation of such an expression is a
    boolean value that is true if the left operand is less than the right
    operand. It is false otherwise.

    Methods:
    --------
    accept(visitor, arg):
        Returns the result of comparison between the left and right
        expressions.

    Examples:
    ---------
    >>> lth = Lth(left=Num(23), right=Var("a"))
    >>> visitor = VisitorEval()
    >>> arg = {"a": 6}
    >>> lth.accept(visitor, arg)
    False
    """

    def accept(self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]):
        return visitor.visit_lth(self, arg)


class Let(Expression):
    """
    This class represents a let expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:
    1. Evaluate e0 in the environment env, yielding e0_val
    2. Evaluate e1 in the new environment env' = env + {v:e0_val}

    Attributes:
    -----------
    identifier : str
        The variable identifier (i.e., its name).
    exp_def : Expression (values = `Num` or `Bln`)
        The expression that defines the variable. Must be `Num` or `Bln`.
    exp_body : Expression
        The expression to evaluate considering this variable.

    Examples:
    ---------
    >>> let = Let(
    ...     identifier='x',
    ...     exp_def=Num(23),
    ...     exp_body=Add(Var('x'), Var('y'))
    ... )
    >>> visitor = VisitorEval()
    >>> arg = {'y': 6}
    >>> let.accept(visitor, arg)
    29
    """

    def __init__(
        self,
        identifier: str,
        exp_def: Expression,
        exp_body: Expression,
    ) -> None:
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(
        self,
        visitor: "VisitorEval",
        arg: dict[str, Union[bool, int]],
    ) -> Union[bool, int]:
        return visitor.visit_let(self, arg)


class IfThenElse(Expression):
    """
    This class represents a conditional expression. The semantics of an
    expression such as 'if B then E0 else E1' is as follows:

    1. Evaluate B. Call the result `ValueB`.
    2. If `ValueB` is True, then evalute `E0` and return the result.
    3. If ValueB is False, then evaluate `E1` and return the result.

    Notice that we only evaluate one of the two sub-expressions, not both. Thus,
    "if True then 0 else 1 div 0" will return 0 indeed.

    Attributes:
    -----------
    cond : Expression
        A `bool`-typed expression.
    e0 : Expression
        Expression to evaluate if `cond` is `True`.
    e1 : Expression
        Expression to evaluate if `cond` is `False`.

    Methods:
    --------
    accept(visitor, arg):
        Returns the result from the `visit_var` method of the given `visitor`,
        considering some environment defined in `arg`.

    Examples:
    ---------
    >>> # If `x` < `y`, then evaluate (z + x); if not, evaluate (z + y)
    >>> cond = Lth(Var('x'), Var('y'))
    >>> e0 = Let('z', Num(10), Add(Var('z'), Var('x')))
    >>> e1 = Let('z', Num(10), Add(Var('z'), Var('y')))
    >>> if_then_else = IfThenElse(cond, e0, e1)
    >>> visitor = VisitorEval()
    >>> arg = {'x': 20, 'y': 30}
    >>> if_then_else.accept(visitor, arg)
    30
    """

    def __init__(self, cond: Expression, e0: Expression, e1: Expression) -> None:
        self.cond = cond
        self.e0 = e0
        self.e1 = e1

    def accept(
        self,
        visitor: "VisitorEval",
        arg: dict[str, Union[bool, int]],
    ) -> Union[bool, int]:
        return visitor.visit_ifThenElse(self, arg)


class Fn(Expression):
    """
    This class represents an anonymous function.

    Attributes:
    -----------
    formal : str
        The formal parameter name for the function.
    body : Expression
        The expression representing the function's body.

    Examples:
    ---------
    >>> f = Fn('v', Add(Var('v'), Var('v')))
    >>> ev = VisitorEval()
    >>> print(f.accept(ev, {}))
    Fn(v)
    """

    def __init__(self, formal: str, body: Expression) -> None:
        self.formal = formal
        self.body = body

    def accept(
        self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]
    ) -> Union[bool, int]:
        return visitor.visit_fn(self, arg)


class Fun(Fn):
    """
    This class represents a named function. Named functions can be invoked
    recursively.

    Attributes:
    -----------
    name : str
        The name of the function.
    formal : str
        The formal parameter name for the function.
    body : Expression
        The expression representing the function's body.

    Examples:
    ---------
    >>> f_obj = Fun('some_named_func', 'v', Add(Var('v'), Var('v')))
    >>> ev = VisitorEval()
    >>> print(f_obj.accept(ev, {}))
    Fun some_named_func(v)
    """

    def __init__(self, name: str, formal: str, body: Expression) -> None:
        super().__init__(formal, body)
        self.name = name

    def accept(
        self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]
    ) -> Union[bool, int]:
        return visitor.visit_fun(self, arg)


class App(Expression):
    """
    This class represents a function application, such as 'e0 e1'. The semantics
    of an application is as follows: we evaluate the left side, e.g., e0. It
    must result into a function fn(p, b) denoting a function that takes in a
    parameter p and evaluates a body b. We then evaluate e1 to obtain a value
    v. Finally, we evaluate b, but in a context where p is bound to v.

    Attributes:
    -----------
    function : Expression
        The expression representing the function being applied.
    actual : Expression
        The argument expression that will be applied to the function.

    Examples:
    ---------
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

    def __init__(self, function: Expression, actual: Expression) -> None:
        self.function = function
        self.actual = actual

    def accept(
        self, visitor: "VisitorEval", arg: dict[str, Union[bool, int]]
    ) -> Union[bool, int]:
        return visitor.visit_app(self, arg)


class Function:
    """
    This is the class that represents functions. This class lets us distinguish
    the three types that now exist in the language: numbers, booleans and
    functions. Notice that the evaluation of an expression can now be a
    function.

    Attributes:
    -----------
    formal : str
        The formal parameter name for the function.
    body : Expression
        The expression representing the function's body.
    env : dict[str, Union[bool, int]]
        The environment to evaluate.

    Examples:
    ---------
    >>> f = Function('v', Add(Var('v'), Var('v')), {})
    >>> print(str(f))
    Fn(v)
    """

    def __init__(
        self, formal: str, body: Expression, env: dict[str, Union[bool, int]]
    ) -> None:
        self.formal = formal
        self.body = body
        self.env = env

    def __str__(self) -> str:
        return f"Fn({self.formal})"


class RecFunction(Function):
    """
    This is the class that represents named functions. The key different between
    named and anonymous functions is exactly the "name" :)

    Attributes:
    -----------
    name : str
        The name of the function.
    formal : str
        The formal parameter name for the function.
    body : Expression
        The expression representing the function's body.
    env : dict[str, Union[bool, int]]
        The environment to evaluate.

    Examples:
    ---------
    >>> f = RecFunction('f', 'v', Add(Var('v'), Var('v')), {})
    >>> print(str(f))
    Fun f(v)
    """

    def __init__(
        self, name: str, formal: str, body: Expression, env: dict[str, Union[bool, int]]
    ) -> None:
        super().__init__(formal, body, env)
        self.name = name

    def __str__(self) -> str:
        return f"Fun {self.name}({self.formal})"


class VisitorEval:
    """
    This class implements a visitor that evaluates an expression with recursive
    functions.

    This class does not have any attributes.

    Methods:
    --------
    visit_var(var, env):
        Visit a variable and return its value.

    visit_num(num, env):
        Visit a number and return its value.

    visit_bln(bln, env):
        Visit a boolean and return its value.

    visit_add(add, env):
        Visit an `Add` operation, and evaluate it.

    visit_and(exp, env):
        Visit an `And` operation, and evaluate it.

    visit_lth(exp, env):
        Visit a `Lth` operation, and evaluate it.

    visit_ifThenElse(exp, env):
        Visit a `IfThenElse` expression, and evaluate it.

    visit_let(exp, env):
        Visit a `Let` expression, and evaluate it.

    visit_fn(exp, env):
        Visit an anonymous function, and evaluate it.

    visit_fun(exp, env):
        Visit a named function, and evaluate it.

    visit_app(exp, env):
        Visit a function application, and evaluate it.

    Examples:
    ---------
    >>> e = Let('v', Num(42), Var('v'))
    >>> v = VisitorEval()
    >>> print(e.accept(v, {}))
    42

    >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
    >>> v = VisitorEval()
    >>> print(e.accept(v, {}))
    42
    """

    def visit_var(self, var: Var, env: dict[str, Union[bool, int]]) -> Union[bool, int]:
        """
        Visit a variable and return its contents.

        Parameters:
        -----------
        var : Var
            The `Var` representation of this variable.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The contents of the variable in the given `env`.

        Examples:
        ---------
        >>> var = Var("some_var")
        >>> visitor = VisitorEval()
        >>> arg = {"some_var": 4}
        >>> var.accept(visitor, arg)
        4

        >>> try:
        ...     var = Var("some_var")
        ...     visitor = VisitorEval()
        ...     arg = {"some_other_var": 10}
        ...     var.accept(visitor, arg)
        ... except ValueError as e:
        ...     print(e)
        Variable not found some_var

        Raises:
        -------
        ValueError
            Raised if the variable's identifier is not found in `env`.
        """

        if var.identifier in env:
            return env[var.identifier]
        else:
            raise ValueError(f"Variable not found {var.identifier}")

    def visit_num(self, num: Num, env: dict[str, Union[bool, int]]) -> int:
        """
        Visit a number and return its value.

        Parameters:
        -----------
        num : Num
            The `Num` representation of this number.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values. This
            parameter is required, but ignored.

        Returns:
        --------
        : int
            The value of this number.

        Examples:
        >>> num = Num(23)
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> num.accept(visitor, arg)
        23
        """

        return num.num

    def visit_bln(self, exp: Bln, env: dict[str, Union[bool, int]]) -> bool:
        """
        Visit a boolean and return its value.

        Parameters:
        -----------
        exp : Bln
            The `Bln` representation of this boolean.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values. This
            parameter is required, but ignored.

        Returns:
        --------
        : bool
            The value of this boolean.

        Examples:
        >>> exp = Bln(True)
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> exp.accept(visitor, arg)
        True
        """

        return exp.bln

    def visit_add(self, add: Add, env: dict[str, Union[bool, int]]) -> int:
        """
        Visit an addition and return its result.

        Parameters:
        -----------
        add : Add
            The `Add` representation of this operation.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : int
            The result of this addition.

        Examples:
        ---------
        >>> add = Add(left=Num(23), right=Num(6))
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> add.accept(visitor, arg)
        29
        """

        return add.left.accept(self, env) + add.right.accept(self, env)

    def visit_and(self, exp: And, env: dict[str, Union[bool, int]]) -> bool:
        """
        Visit a `logical and` expression and return its result.

        Parameters:
        -----------
        exp : And
            The `And` representation of this expression.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : bool
            The result of this expression, if type-valid.

        Examples:
        ---------
        >>> _and = And(left=Bln(True), right=Bln(True))
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> _and.accept(visitor, arg)
        True
        """

        val_left = exp.left.accept(self, env)

        if val_left:
            return exp.right.accept(self, env)

        return False

    def visit_lth(self, exp: Lth, env: dict[str, Union[bool, int]]) -> bool:
        """
        Visit a `less than` expression and return its result.

        Parameters:
        -----------
        exp : Lth
            The `Lth` representation of this expression.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : bool
            The result of this expression.

        Examples:
        ---------
        >>> lth = Lth(left=Num(23), right=Num(6))
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> lth.accept(visitor, arg)
        False
        """

        val_left = exp.left.accept(self, env)
        val_right = exp.right.accept(self, env)

        return val_left < val_right

    def visit_ifThenElse(
        self, exp: IfThenElse, env: dict[str, Union[bool, int]]
    ) -> Union[bool, int]:
        """
        Visit an `if/else` expression and return the result of the evaluated branch.

        Parameters:
        -----------
        exp : IfThenElse
            The `IfThenElse` representation of this expression.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The result of evaluated branch.

        Examples:
        ---------
        >>> cond = Lth(Var('x'), Var('y'))
        >>> e0 = Let('z', Num(10), Add(Var('z'), Var('x')))
        >>> e1 = Let('z', Num(10), Add(Var('z'), Var('y')))
        >>> if_then_else = IfThenElse(cond, e0, e1)
        >>> visitor = VisitorEval()
        >>> arg = {'x': 23, 'y': 10}
        >>> if_then_else.accept(visitor, arg)
        20
        """

        cond = exp.cond.accept(self, env)

        if cond:
            return exp.e0.accept(self, env)
        else:
            return exp.e1.accept(self, env)

    def visit_let(self, let: Let, env: dict[str, Union[bool, int]]) -> Union[bool, int]:
        """
        Visit a `let` expression and return its result.

        Parameters:
        -----------
        let : Let
            The `Let` representation of this operation.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The result of `let.exp_body` evaluation.

        Examples:
        ---------
        >>> let = Let(
        ...     identifier='x',
        ...     exp_def=Num(23),
        ...     exp_body=Add(Var('x'), Var('y'))
        ... )
        >>> visitor = VisitorEval()
        >>> arg = {'y': 7}
        >>> let.accept(visitor, arg)
        30

        >>> let = Let(
        ...     identifier='x',
        ...     exp_def=Bln(False),
        ...     exp_body=And(Var('x'), Bln(True))
        ... )
        >>> visitor = VisitorEval()
        >>> arg = {}
        >>> let.accept(visitor, arg)
        False
        """

        e0_val = let.exp_def.accept(self, env)
        new_env = dict(env)
        new_env[let.identifier] = e0_val

        return let.exp_body.accept(self, new_env)

    def visit_fn(self, exp: Fn, env: dict[str, Union[bool, int]]) -> Function:
        """
        Visit an anonymous function and create a `Function` object from it.

        Parameters:
        -----------
        exp : Fn
            The anonymous function to visit.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Function
            The `Function` object that represents the given anonymous function.
        """

        return Function(exp.formal, exp.body, env)

    def visit_fun(self, exp: Fun, env: dict[str, Union[bool, int]]) -> RecFunction:
        """
        Visit a named function and create a `RecFunction` object from it.

        Parameters:
        -----------
        exp : Fun
            The named function to visit.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : RecFunction
            The `RecFunction` object that represents the given named function.
        """

        return RecFunction(exp.name, exp.formal, exp.body, env)

    def visit_app(self, exp: App, env: dict[str, Union[bool, int]]) -> Union[bool, int]:
        """
        Visit a function application and evaluate it.

        The application of function to actual parameter must contain two cases:

        1. An anonymous function is applied: (fn x => x + 1) 2
        2. A named function is applied: f 2, where f is fun f a = a + a
        The only difference between these two cases is that in the second we
        must augment the environment with the name of the named function.

        Parameters:
        -----------
        exp : App
            The `App` representation of this expression.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The result of the function application.

        Examples:
        ---------
        >>> f = Fun('f', 'v', Add(Var('v'), Num(1)))
        >>> e0 = Let('f', f, App(Var('f'), Num(2)))
        >>> ev = VisitorEval()
        >>> e0.accept(ev, {})
        3

        Raises:
        -------
        TypeError
            Raised if `exp.function` is not a `Function` object.
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
            raise TypeError("Type error: exp.function is not a Function object.")


def create_arithmetic_sum(init_value: int, end_value: int) -> Let:
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

    Parameters:
    -----------
    init_value : int
        The initial value of the sum.
    end_value : int
        The end value of the sum.

    Returns:
    --------
    : Let
        The `Let` representation of this arithmetic sum.

    Examples:
    ---------
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
    cond_lth = Lth(Var("n0"), Var("n1"))
    add_n1 = Add(Var("n0"), Num(1))
    app_range_add = App(Var("range"), add_n1)  # range (n0 + 1)
    app_range_n1 = App(app_range_add, Var("n1"))
    add_n1_range = Add(Var("n0"), app_range_n1)
    body = IfThenElse(cond_lth, add_n1_range, Num(0))

    # Anonymous function: fn n1 => ...
    fn_n1 = Fn("n1", body)

    # Recursive function: fun range n0 = fn n1 => ...
    fun_range = Fun("range", "n0", fn_n1)

    # Application: range init_value end_value
    app_range_init = App(Var("range"), Num(init_value))
    app_range = App(app_range_init, Num(end_value))

    # Whole program:
    return Let("range", fun_range, app_range)


def create_loop(num_iterations: int) -> Let:
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

    Parameters:
    -----------
    num_iterations : int
        The number of iterations this loop must perform.

    Returns:
    --------
    : Let
        The `Let` representation of this loop.

    Examples:
    ---------
    >>> program = create_loop(10)
    >>> v = VisitorEval()
    >>> program.accept(v, {})
    11
    """
    # The body of the recursive function:
    add_var_minus = Add(Var("n"), Num(-1))
    app_loop_var_minus = App(Var("loop"), add_var_minus)
    app_f_a = App(Var("f"), Var("a"))
    app_loop_f = App(app_loop_var_minus, Var("f"))
    app_loop_f_a = App(app_loop_f, app_f_a)
    cond_n_2 = Lth(Var("n"), Num(2))
    body = IfThenElse(cond_n_2, Var("a"), app_loop_f_a)

    # Anonymous function fn a => ...
    fn_a = Fn("a", body)

    # Anonymous function fn f => fn a => ...
    fn_f = Fn("f", fn_a)

    # Recursive function fun loop n = fn f => fn a => ...
    fun_loop = Fun("loop", "n", fn_f)

    # Application: loop num_iterations (fn x => x + 1) 2
    app_loop_num_iter = App(Var("loop"), Num(num_iterations))
    add_x_1 = Add(Var("x"), Num(1))
    iterate_over_x = App(app_loop_num_iter, Fn("x", add_x_1))
    app_loop = App(iterate_over_x, Num(2))

    # Whole program:
    return Let("loop", fun_loop, app_loop)


def create_for_loop(begin: int, end: int, function: Function) -> Let:
    """
    This function parameterizes our loops with the begin and end of the
    iterations, plus a high order function that simulates the body of the loop.

    Parameters:
    -----------
    begin : int
        The initial value of the iterator.
    end : int
        The final value of the iterator.
    function : Function
        The body of the loop.

    Returns:
    --------
    : Let
        The `Let` representation of this `for` loop.

    Examples:
    ---------
    >>> program = create_for_loop(4, 10, Fn('x', Add(Var('x'), Num(1))))
    >>> v = VisitorEval()
    >>> program.accept(v, {})
    8

    >>> program = create_for_loop(2, 10, Fn('x', Add(Var('x'), Num(1))))
    >>> v = VisitorEval()
    >>> program.accept(v, {})
    7

    >>> double = Fn('x', Add(Var('x'), Var('x')))
    >>> program = create_for_loop(2, 10, double)
    >>> v = VisitorEval()
    >>> program.accept(v, {})
    16
    """
    # The body of the recursive function:
    # if n = 1 then a else loop (n - 1) f (f a)
    n_lth_a = Lth(Var("n"), Var("a"))
    add_n_minus_1 = Add(Var("n"), Num(-1))
    app_loop_n_minus_1 = App(Var("loop"), add_n_minus_1)
    app_f_n_times = App(app_loop_n_minus_1, Var("f"))
    app_f_a = App(Var("f"), Var("a"))
    loop_over_app = App(app_f_n_times, app_f_a)
    body = IfThenElse(n_lth_a, Var("a"), loop_over_app)

    # Anonymous function fn a => ...
    fn_a = Fn("a", body)

    # Anonymous function fn f => fn a => ...
    fn_f = Fn("f", fn_a)

    # Recursive function fun loop n = fn f => fn a => ...
    fun_loop = Fun("loop", "n", fn_f)

    # Application: loop num_iterations (fn x => x + 1) 2
    loop_till_end = App(Var("loop"), Num(end))
    loop_over_function = App(loop_till_end, function)
    app_loop = App(loop_over_function, Num(begin))

    # Whole program:
    return Let("loop", fun_loop, app_loop)

add_y_x = Add(Var("y"), Var("x"))
f_y_is_add = Fn("y", add_y_x)
fun_f_x_is_add = Fun("f", "x", f_y_is_add)
def_g = Let("g", fun_f_x_is_add, Var("g"))
app_g_on_3 = App(def_g, Num(3))
p = App(app_g_on_3, Num(4))
v = VisitorEval()
print(p.accept(v, {}))

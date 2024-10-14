import sys

from abc import ABC, abstractmethod
from typing import Union

class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    accept():
        Abstract method that should be implemented to accept a visitor.
    """

    @abstractmethod
    def accept(self, visitor: Union["TypeChecker", "VisitorTypeSafeEval"]) -> Union[type, int]:
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
    >>> visitor = TypeChecker()
    >>> arg = {"abc": 23}
    >>> var.accept(visitor, arg)
    23

    >>> var = Var("abc")
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"abc": True}
    >>> var.accept(visitor, arg)
    True
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> int:
        """
        Accept a visitor in this variable.

        Parameters:
        -----------
        visitor : TypeChecker or VisitorTypeSafeEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : int
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
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> num.accept(visitor, arg)
    <class 'int'>

    >>> num = Num(23)
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"abc": 123}
    >>> num.accept(visitor, arg)
    23
    """

    def __init__(self, num: int) -> None:
        self.num = num

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:
        """
        Accept a visitor in this number.

        Parameters:
        -----------
        visitor : TypeChecker or VisitorTypeSafeEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : Union[type, int]
            The type (if `visitor` is `TypeChecker`) or the value (if `visitor`
            is `VisitorTypeSafeEval`) of this number.
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
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> bln.accept(visitor, arg)
    <class 'bool'>

    >>> bln = Bln(True)
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {}
    >>> bln.accept(visitor, arg)
    True
    """

    def __init__(self, bln: bool) -> None:
        self.bln = bln

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:
        """
        Accept a visitor in this boolean.

        Parameters:
        -----------
        visitor : TypeChecker or VisitorTypeSafeEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : Union[type, bool]
            The type (if `visitor` is `TypeChecker`) or the value (if `visitor`
            is `VisitorTypeSafeEval`) of this boolean.
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
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:
        """
        Accept a visitor in this binary expression.

        Parameters:
        -----------
        visitor : TypeChecker or VisitorTypeSafeEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : Union[type, bool]
            The type (if `visitor` is `TypeChecker`) or the resulting value (if
            `visitor` is `VisitorTypeSafeEval`) of this binary expression.
        """

        pass

class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the type or the result of addition between the left and right
        expressions.

    Examples:
    ---------
    >>> add = Add(left=Num(23), right=Num(6))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> add.accept(visitor, arg)
    <class 'int'>

    >>> try:
    ...     add = Add(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     add.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot add int to bool")
    Error raised as expected: cannot add int to bool

    >>> add = Add(left=Num(23), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": 1}
    >>> add.accept(visitor, arg)
    24
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_add(self, arg)

class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the type or the result of subtraction between the left and right
        expressions.

    Examples:
    ---------
    >>> sub = Sub(left=Num(23), right=Num(6))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> sub.accept(visitor, arg)
    <class 'int'>

    >>> try:
    ...     sub = Sub(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     sub.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot subtract bool from int")
    Error raised as expected: cannot subtract bool from int

    >>> sub = Sub(left=Num(24), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": 4}
    >>> sub.accept(visitor, arg)
    20
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_sub(self, arg)

class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the type or the result of multiplication between the left and
        right expressions.

    Examples:
    ---------
    >>> mul = Mul(left=Num(23), right=Num(6))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> mul.accept(visitor, arg)
    <class 'int'>

    >>> try:
    ...     mul = Mul(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     mul.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot multiply int and bool")
    Error raised as expected: cannot multiply int and bool

    >>> mul = Mul(left=Num(24), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": 4}
    >>> mul.accept(visitor, arg)
    96
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_mul(self, arg)

class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.

    Methods:
    --------
    accept(visitor, arg):
        Returns the type or the result of division between the left and right
        expressions.

    Examples:
    ---------
    >>> div = Div(left=Num(23), right=Num(6))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> div.accept(visitor, arg)
    <class 'int'>

    >>> try:
    ...     div = Div(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     div.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot divide int by bool")
    Error raised as expected: cannot divide int by bool

    >>> div = Div(left=Num(24), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": 4}
    >>> div.accept(visitor, arg)
    6
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_div(self, arg)

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
    >>> _and = And(left=Bln(True), right=Bln(False))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> _and.accept(visitor, arg)
    <class 'bool'>

    >>> try:
    ...     _and = And(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     _and.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot compute logical and between int and bool")
    Error raised as expected: cannot compute logical and between int and bool

    >>> _and = And(left=Bln(True), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": True}
    >>> _and.accept(visitor, arg)
    True
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

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
        Returns the type or the result of comparison between the left and right
        expressions.

    Examples:
    ---------
    >>> lth = Lth(left=Num(5), right=Num(10))
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> lth.accept(visitor, arg)
    <class 'bool'>

    >>> try:
    ...     lth = Lth(left=Num(23), right=Bln(True))
    ...     visitor = TypeChecker()
    ...     arg = {}
    ...     lth.accept(visitor, arg)
    ... except TypeError:
    ...     print("Error raised as expected: cannot compare int to bool with `less-than`")
    Error raised as expected: cannot compare int to bool with `less-than`

    >>> lth = Lth(left=Num(23), right=Var("a"))
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {"a": 6}
    >>> lth.accept(visitor, arg)
    False
    """

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_lth(self, arg)

class Let(Expression):
    """
    This class represents a let expression. The semantics of a let expression,
    such as "let v <- e0 in e1" on an environment env is as follows:
    1. Evaluate e0 in the environment env, yielding e0_val
    2. Evaluate e1 in the new environment env' = env + {v:e0_val}

    The let expression is the only expression where variable names can be
    associated with types. For instance, if we create an expression like:
    Let('v', int, e0, e1), then we are saying that variable 'v' must have
    type int.

    Attributes:
    -----------
    identifier : str
        The variable identifier (i.e., its name).
    type_identifier : type (values = `int` or `bool`)
        The variable type. Must be `int` or `bool`.
    exp_def : Expression (values = `Num` or `Bln`)
        The expression that defines the variable. Must be `Num` or `Bln`.
    exp_body : Expression
        The expression to evaluate considering this variable.

    Examples:
    ---------
    >>> let = Let(
    ...     identifier='x',
    ...     type_identifier=int,
    ...     exp_def=Num(23),
    ...     exp_body=Add(Var('x'), Num(5))
    ... )
    >>> visitor = TypeChecker()
    >>> arg = {}
    >>> let.accept(visitor, arg)
    <class 'int'>

    >>> let = Let(
    ...     identifier='x',
    ...     type_identifier=int,
    ...     exp_def=Num(23),
    ...     exp_body=Add(Var('x'), Var('y'))
    ... )
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {'y': 6}
    >>> let.accept(visitor, arg)
    29
    """

    def __init__(
        self,
        identifier: str,
        type_identifier: type,
        exp_def: Expression,
        exp_body: Expression
    ):
        self.identifier = identifier
        self.type_identifier = type_identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

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
    >>> cond = Lth(Var('x'), Var('y'))
    >>> e0 = Let('z', int, Num(10), Add(Var('z'), Var('x')))
    >>> e1 = Let('z', int, Num(10), Add(Var('z'), Var('y')))
    >>> if_then_else = IfThenElse(cond, e0, e1)
    >>> visitor = TypeChecker()
    >>> arg = {'x': int, 'y': int}
    >>> if_then_else.accept(visitor, arg)
    <class 'int'>

    >>> # If `x` < `y`, then evaluate (z + x); if not, evaluate (z + y)
    >>> cond = Lth(Var('x'), Var('y'))
    >>> e0 = Let('z', int, Num(10), Add(Var('z'), Var('x')))
    >>> e1 = Let('z', int, Num(10), Add(Var('z'), Var('y')))
    >>> if_then_else = IfThenElse(cond, e0, e1)
    >>> visitor = VisitorTypeSafeEval()
    >>> arg = {'x': 20, 'y': 30}
    >>> if_then_else.accept(visitor, arg)
    30
    """

    def __init__(self, cond: Expression, e0: Expression, e1: Expression):
        self.cond = cond
        self.e0 = e0
        self.e1 = e1

    def accept(
        self,
        visitor: Union["TypeChecker", "VisitorTypeSafeEval"],
        arg: dict[str, int]
    ) -> Union[type, int]:

        return visitor.visit_ifThenElse(self, arg)


class TypeChecker:
    def visit_var(self, var_exp, env):
        # Look up the variable's type in the environment
        if var_exp.identifier in env:
            return env[var_exp.identifier]
        else:
            raise TypeError(f"Variable {var_exp.identifier} is not defined")

    def visit_num(self, num_exp, env):
        # Numbers are always of type int
        return int

    def visit_bln(self, bln_exp, env):
        # Boolean literals are always of type bool
        return bool

    def visit_add(self, add_exp, env):
        # Both operands must be of type int
        left_type = add_exp.left.accept(self, env)
        right_type = add_exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} + {right_type}")

    def visit_sub(self, sub_exp, env):
        # Both operands must be of type int
        left_type = sub_exp.left.accept(self, env)
        right_type = sub_exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} - {right_type}")

    def visit_mul(self, mul_exp, env):
        # Both operands must be of type int
        left_type = mul_exp.left.accept(self, env)
        right_type = mul_exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} * {right_type}")

    def visit_div(self, div_exp, env):
        # Both operands must be of type int
        left_type = div_exp.left.accept(self, env)
        right_type = div_exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} / {right_type}")

    def visit_and(self, and_exp, env):
        # Both operands must be of type bool
        left_type = and_exp.left.accept(self, env)
        right_type = and_exp.right.accept(self, env)
        if left_type == bool and right_type == bool:
            return bool
        else:
            raise TypeError(f"Type error: {left_type} and {right_type}")

    def visit_lth(self, lth_exp, env):
        # Both operands must be of type int and result is of type bool
        left_type = lth_exp.left.accept(self, env)
        right_type = lth_exp.right.accept(self, env)
        if left_type == int and right_type == int:
            return bool
        else:
            raise TypeError(f"Type error: {left_type} < {right_type}")

    def visit_let(self, let_exp, env):
        # Type-check the definition and bind it to the environment
        def_type = let_exp.exp_def.accept(self, env)
        if def_type == let_exp.type_identifier:
            # Temporarily extend the environment with the new variable
            new_env = dict(env)
            new_env[let_exp.identifier] = let_exp.type_identifier
            # Restore the environment
            return let_exp.exp_body.accept(self, new_env)
        else:
            epct_str = f"expected {let_exp.type_identifier}"
            raise TypeError(f"Type error in let: {epct_str} but got {def_type}")

    def visit_ifThenElse(self, if_exp, env):
        # The condition must be of type bool, and both branches must have
        # the same type
        cond_type = if_exp.cond.accept(self, env)
        if cond_type != bool:
            raise TypeError(f"Type error: expected bool but got {cond_type}")
        then_type = if_exp.e0.accept(self, env)
        else_type = if_exp.e1.accept(self, env)
        if then_type == else_type:
            return then_type
        else:
            then_str = f"then branch is {then_type}"
            else_str = f"else branch is {else_type}"
            raise TypeError(f"Type error: {then_str}, {else_str}")

def test_type_checking_rules():
    # Example Usage
    env = {'x': int, 'y': bool}
    checker = TypeChecker()

    # Example expressions:
    expr = Add(Var('x'), Num(5))  # x + 5
    print(expr.accept(checker, env))  # Should return int

    # Example expressions:
    expr = And(Var('y'), Bln(True))  # y and True
    print(expr.accept(checker, env))  # Should return bool

    expr2 = IfThenElse(Var('y'), Num(1), Num(0))  # if y then 1 else 0
    print(expr2.accept(checker, env))  # Should return int

    expr3 = Let('z', int, Num(3), Add(Var('z'), Num(2)))  # let z = 3 in z + 2
    print(expr3.accept(checker, env))  # Should return int

class VisitorTypeSafeEval:
    def visit_var(self, var, env):
        if var.identifier in env:
            return env[var.identifier]
        else:
            sys.exit(f"Variable not found {var.identifier}")

    def visit_num(self, num, env):
        return num.num

    def visit_bln(self, exp, env):
        return exp.bln

    def visit_add(self, add, env):
        v0 = add.left.accept(self, env)
        v1 = add.right.accept(self, env)
        self.ensure_type(v0, int, "Addition")
        self.ensure_type(v1, int, "Addition")
        return v0 + v1

    def visit_sub(self, sub, env):
        v0 = sub.left.accept(self, env)
        v1 = sub.right.accept(self, env)
        self.ensure_type(v0, int, "Subtraction")
        self.ensure_type(v1, int, "Subtraction")
        return v0 - v1

    def visit_mul(self, mul, env):
        v0 = mul.left.accept(self, env)
        v1 = mul.right.accept(self, env)
        self.ensure_type(v0, int, "Multiplication")
        self.ensure_type(v1, int, "Multiplication")
        return v0 * v1

    def visit_div(self, div, env):
        v0 = div.left.accept(self, env)
        v1 = div.right.accept(self, env)
        self.ensure_type(v0, int, "Division")
        self.ensure_type(v1, int, "Division")
        return v0 // v1

    def visit_and(self, exp, env):
        v0 = exp.left.accept(self, env)
        self.ensure_type(v0, bool, "And")
        if v0:
            v1 = exp.right.accept(self, env)
            self.ensure_type(v1, bool, "And")
            return v1
        return False

    def visit_lth(self, exp, env):
        v0 = exp.left.accept(self, env)
        v1 = exp.right.accept(self, env)
        self.ensure_type(v0, int, "Less Than")
        self.ensure_type(v1, int, "Less Than")
        return v0 < v1

    def visit_ifThenElse(self, exp, env):
        cond = exp.cond.accept(self, env)
        self.ensure_type(cond, bool, "If-Then-Else Condition")
        if cond:
            return exp.e0.accept(self, env)
        else:
            return exp.e1.accept(self, env)

    def visit_let(self, let, env):
        v0 = let.exp_def.accept(self, env)
        new_env = dict(env)
        new_env[let.identifier] = v0
        return let.exp_body.accept(self, new_env)

    def ensure_type(self, value, expected_type, operation_name):
        #if not isinstance(value, expected_type):
        if not type(value) == expected_type:
            op_str = f"Type error in {operation_name}"
            ex_str = f"expected {expected_type.__name__}"
            gt_str = f"got {type(value).__name__}"
            raise TypeError(f"{op_str}: {ex_str}, {gt_str}")

def dynamically_type_safe_eval(e):
    """
    Evaluates the expression in a type safe way.

    Example:
    >>> e0 = Let('w', int, Num(2), Add(Var('v'), Var('w')))
    >>> e1 = Let('v', int, Num(40), e0)
    >>> dynamically_type_safe_eval(e1)
    42

    >>> e0 = Let('w', int, Num(2), And(Var('v'), Var('w')))
    >>> e1 = Let('v', int, Num(40), e0)
    >>> dynamically_type_safe_eval(e1)
    Type error in And: expected bool, got int

    >>> e = IfThenElse(Bln(True), Num(0), Bln(False))
    >>> dynamically_type_safe_eval(e)
    0
    """
    v = VisitorTypeSafeEval()
    try:
        return e.accept(v, {})
    except TypeError as tp_error:
        print(tp_error)

def statically_type_safe_eval(e):
    """
    Evaluates the expression in a type safe way.

    Example:
    >>> e0 = Let('w', int, Num(2), Add(Var('v'), Var('w')))
    >>> e1 = Let('v', int, Num(40), e0)
    >>> statically_type_safe_eval(e1)
    42

    >>> e0 = Let('w', int, Num(2), And(Var('v'), Var('w')))
    >>> e1 = Let('v', int, Num(40), e0)
    >>> statically_type_safe_eval(e1)
    Type error: <class 'int'> and <class 'int'>

    >>> e = IfThenElse(Bln(True), Num(0), Bln(False))
    >>> statically_type_safe_eval(e)
    Type error: then branch is <class 'int'>, else branch is <class 'bool'>
    """
    tp_check = TypeChecker()
    v = VisitorTypeSafeEval()
    try:
        e.accept(tp_check, {})
        return e.accept(v, {})
    except TypeError as tp_error:
        print(tp_error)

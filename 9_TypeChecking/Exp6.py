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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> + <class 'bool'>

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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> - <class 'bool'>

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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> * <class 'bool'>

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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> / <class 'bool'>

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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> and <class 'bool'>

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
    ... except TypeError as e:
    ...     print(e)
    Type error: <class 'int'> < <class 'bool'>

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
    """
    This class implements a visitor that enacts a TypeChecker: it checks whether
    the types of the operands in some expression are compatible.

    This class does not have any attributes.

    Methods:
    --------
    visit_var(var_exp, env):
        Visit a variable and return its type.

    visit_num(num_exp, env):
        Visit a number and return its type (i.e., `int`).

    visit_bln(bln_exp, env):
        Visit a boolean and return its type (i.e., `bool`).

    visit_add(add_exp, env):
        Visit an `Add` operation and type-check it.

    visit_sub(sub_exp, env):
        Visit a `Sub` operation and type-check it.

    visit_mul(mul_exp, env):
        Visit a `Mul` operation and type-check it.

    visit_div(div_exp, env):
        Visit a `Div` operation and type-check it.

    visit_and(and_exp, env):
        Visit an `And` operation and type-check it.

    visit_lth(lth_exp, env):
        Visit a `Lth` operation and type-check it.

    visit_let(let_exp, env):
        Visit a `Let` operation and type-check it.

    visit_ifThenElse(if_exp, env):
        Visit a `IfThenElse` operation and type-check it.
    """

    def visit_var(self, var_exp: Var, env: dict[str, type]) -> type:
        """
        Type-check a variable.

        Parameters:
        -----------
        var_exp : Var
            The `Var` representation of this variable.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type
            The type of the variable.

        Examples:
        ---------
        >>> var = Var("some_var")
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> var.accept(visitor, arg)
        <class 'int'>

        >>> try:
        ...     var = Var("some_var")
        ...     visitor = TypeChecker()
        ...     arg = {"some_other_var": int}
        ...     var.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Variable some_var is not defined

        Raises:
        -------
        TypeError
            Raised if the variable's identifier is not found in `env`.
        """

        # Look up the variable's type in the environment
        if var_exp.identifier in env:
            return env[var_exp.identifier]
        else:
            raise TypeError(f"Variable {var_exp.identifier} is not defined")

    def visit_num(self, num_exp: Num, env: dict[str, type]) -> type[int]:
        """
        Type-check a number.

        Parameters:
        -----------
        num_exp : Var
            The `Num` representation of this number. This parameter is
            required, but ignored.
        env : dict[str, type]
            A mapping between variables identifiers and their types. This
            parameter is required, but ignored.

        Returns:
        --------
        : type[int]
            It always returns `<class 'int'>`, as numbers are always int-typed.

        Examples:
        ---------
        >>> num = Num(23)
        >>> visitor = TypeChecker()
        >>> arg = {}
        >>> num.accept(visitor, arg)
        <class 'int'>
        """

        # Numbers are always of type int
        return int

    def visit_bln(self, bln_exp: Bln, env: dict[str, type]) -> type[bool]:
        """
        Type-check a boolean.

        Parameters:
        -----------
        bln_exp : Var
            The `Bln` representation of this boolean. This parameter is
            required, but ignored.
        env : dict[str, type]
            A mapping between variables identifiers and their types. This
            parameter is required, but ignored.

        Returns:
        --------
        : type[bool]
            It always returns `<class 'bool'>`, as booleans are always
            bool-typed.

        Examples:
        ---------
        >>> bln = Bln(False)
        >>> visitor = TypeChecker()
        >>> arg = {}
        >>> bln.accept(visitor, arg)
        <class 'bool'>
        """

        # Boolean literals are always of type bool
        return bool

    def visit_add(self, add_exp: Add, env: dict[str, type]) -> type[int]:
        """
        Type-check an addition expression.

        This requires both operands of the addition (i.e., `add_exp.left` and
        `add_exp.right`) to be int-typed.

        Parameters:
        -----------
        add_exp : Add
            The `Add` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the operation. It will always return `int`, as it is the
            only type supported by addition.

        Examples:
        ---------
        >>> add = Add(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int, "some_other_var": int}
        >>> add.accept(visitor, arg)
        <class 'int'>

        >>> add = Add(Var("some_var"), Num(23))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> add.accept(visitor, arg)
        <class 'int'>

        >>> try:
        ...     add = Add(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     add.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> + <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `int`.
        """

        # Both operands must be of type int
        left_type = add_exp.left.accept(self, env)
        right_type = add_exp.right.accept(self, env)

        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} + {right_type}")

    def visit_sub(self, sub_exp: Sub, env: dict[str, type]) -> type[int]:
        """
        Type-check a subtraction expression.

        This requires both operands of the subtraction (i.e., `add_exp.left` and
        `add_exp.right`) to be int-typed.

        Parameters:
        -----------
        sub_exp : Sub
            The `Sub` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the operation. It will always return `int`, as it is the
            only type supported by subtraction.

        Examples:
        ---------
        >>> sub = Sub(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int, "some_other_var": int}
        >>> sub.accept(visitor, arg)
        <class 'int'>

        >>> sub = Sub(Var("some_var"), Num(23))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> sub.accept(visitor, arg)
        <class 'int'>

        >>> try:
        ...     sub = Sub(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     sub.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> - <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `int`.
        """

        # Both operands must be of type int
        left_type = sub_exp.left.accept(self, env)
        right_type = sub_exp.right.accept(self, env)

        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} - {right_type}")

    def visit_mul(self, mul_exp: Mul, env: dict[str, type]) -> type[int]:
        """
        Type-check a multiplication expression.

        This requires both operands of the multiplication (i.e., `add_exp.left`
        and `add_exp.right`) to be int-typed.

        Parameters:
        -----------
        mul_exp : Mul
            The `Mul` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the operation. It will always return `int`, as it is the
            only type supported by multiplication.

        Examples:
        ---------
        >>> mul = Mul(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int, "some_other_var": int}
        >>> mul.accept(visitor, arg)
        <class 'int'>

        >>> mul = Mul(Var("some_var"), Num(23))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> mul.accept(visitor, arg)
        <class 'int'>

        >>> try:
        ...     mul = Mul(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     mul.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> * <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `int`.
        """

        # Both operands must be of type int
        left_type = mul_exp.left.accept(self, env)
        right_type = mul_exp.right.accept(self, env)

        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} * {right_type}")

    def visit_div(self, div_exp: Div, env: dict[str, type]):
        """
        Type-check a division expression.

        This requires both operands of the division (i.e., `add_exp.left` and
        `add_exp.right`) to be int-typed.

        Parameters:
        -----------
        div_exp : Div
            The `Div` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the operation. It will always return `int`, as it is the
            only type supported by division.

        Examples:
        ---------
        >>> div = Div(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int, "some_other_var": int}
        >>> div.accept(visitor, arg)
        <class 'int'>

        >>> div = Div(Var("some_var"), Num(23))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> div.accept(visitor, arg)
        <class 'int'>

        >>> try:
        ...     div = Div(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     div.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> / <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `int`.
        """

        # Both operands must be of type int
        left_type = div_exp.left.accept(self, env)
        right_type = div_exp.right.accept(self, env)

        if left_type == int and right_type == int:
            return int
        else:
            raise TypeError(f"Type error: {left_type} / {right_type}")

    def visit_and(self, and_exp: And, env: dict[str, type]) -> type[bool]:
        """
        Type-check a `logical and` expression.

        This requires both operands of the operation (i.e., `add_exp.left` and
        `add_exp.right`) to be bool-typed.

        Parameters:
        -----------
        and_exp : And
            The `And` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[bool]
            The type of the operation. It will always return `bool`, as all
            logical operations yield this type.

        Examples:
        ---------
        >>> _and = And(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": bool, "some_other_var": bool}
        >>> _and.accept(visitor, arg)
        <class 'bool'>

        >>> _and = And(Var("some_var"), Bln(False))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": bool}
        >>> _and.accept(visitor, arg)
        <class 'bool'>

        >>> try:
        ...     _and = And(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     _and.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> and <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `bool`.
        """

        # Both operands must be of type bool
        left_type = and_exp.left.accept(self, env)
        right_type = and_exp.right.accept(self, env)

        if left_type == bool and right_type == bool:
            return bool
        else:
            raise TypeError(f"Type error: {left_type} and {right_type}")

    def visit_lth(self, lth_exp: Lth, env: dict[str, type]) -> type[bool]:
        """
        Type-check a `less than` expression.

        This requires both operands of the operation (i.e., `add_exp.left` and
        `add_exp.right`) to be int-typed.

        Parameters:
        -----------
        lth_exp : Lth
            The `Lth` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[bool]
            The type of the operation. It will always return `bool`, as all
            logical operations yield this type.

        Examples:
        ---------
        >>> lth = Lth(Var("some_var"), Var("some_other_var"))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int, "some_other_var": int}
        >>> lth.accept(visitor, arg)
        <class 'bool'>

        >>> lth = Lth(Var("some_var"), Num(23))
        >>> visitor = TypeChecker()
        >>> arg = {"some_var": int}
        >>> lth.accept(visitor, arg)
        <class 'bool'>

        >>> try:
        ...     lth = Lth(Var("some_var"), Bln(True))
        ...     visitor = TypeChecker()
        ...     arg = {"some_var": int}
        ...     lth.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: <class 'int'> < <class 'bool'>

        Raises:
        -------
        TypeError
            Raised if the one of the operands is not `bool`.
        """

        # Both operands must be of type int and result is of type bool
        left_type = lth_exp.left.accept(self, env)
        right_type = lth_exp.right.accept(self, env)

        if left_type == int and right_type == int:
            return bool
        else:
            raise TypeError(f"Type error: {left_type} < {right_type}")

    def visit_let(self, let_exp: Let, env: dict[str, type]):
        """
        Type-check a `let` expression.

        Parameters:
        -----------
        let_exp : Let
            The `Let` representation of this operation.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the operation.

        Examples:
        ---------
        >>> let = Let(
        ...     identifier='x',
        ...     type_identifier=int,
        ...     exp_def=Num(23),
        ...     exp_body=Add(Var('x'), Var('y'))
        ... )
        >>> visitor = TypeChecker()
        >>> arg = {'y': int}
        >>> let.accept(visitor, arg)
        <class 'int'>

        >>> let = Let(
        ...     identifier='x',
        ...     type_identifier=bool,
        ...     exp_def=Bln(False),
        ...     exp_body=And(Var('x'), Bln(True))
        ... )
        >>> visitor = TypeChecker()
        >>> arg = {}
        >>> let.accept(visitor, arg)
        <class 'bool'>

        >>> try:
        ...     let = Let(
        ...         identifier='x',
        ...         type_identifier=bool,
        ...         exp_def=Num(1),
        ...         exp_body=And(Var('x'), Bln(True))
        ...     )
        ...     visitor = TypeChecker()
        ...     arg = {}
        ...     let.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error in let: expected <class 'bool'> but got <class 'int'>

        Raises:
        -------
        TypeError
            Raised if the type of `let_exp.exp_def` is different from
            `let_exp.type_identifier`.
        """

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

    def visit_ifThenElse(self, if_exp: IfThenElse, env: dict[str, type]) -> type:
        """
        Type-check an `if/else` expression.

        The returned type is the type of the branching expressions.

        Parameters:
        -----------
        if_exp : IfThenElse
            The `IfThenElse` representation of this expression.
        env : dict[str, type]
            A mapping between variables identifiers and their types.

        Returns:
        --------
        : type[int]
            The type of the expression.

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

        >>> try:
        ...     cond = Lth(Var('x'), Var('y'))
        ...     e0 = Let('z', int, Num(10), Add(Var('z'), Var('x')))
        ...     e1 = Let('z', int, Num(10), Lth(Var('z'), Var('y')))
        ...     if_then_else = IfThenElse(cond, e0, e1)
        ...     visitor = TypeChecker()
        ...     arg = {'x': int, 'y': int}
        ...     if_then_else.accept(visitor, arg)
        ... except TypeError as e:
        ...     print(e)
        Type error: then branch is <class 'int'>, else branch is <class 'bool'>

        Raises:
        -------
        TypeError
            - Raised if the type of `if_exp.cond` is not `bool`.
            - Raised if the types of both conditional branches (i.e.,
            `if_exp.e0` and `if_exp.e1`) are not the same.
        """

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


def test_type_checking_rules() -> None:
    """Run additional usage examples of `TypeChecker`."""

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

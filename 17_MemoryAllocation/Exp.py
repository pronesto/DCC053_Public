from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    accept(visitor, arg):
        Abstract method that should be implemented to accept a visitor.
    """

    @abstractmethod
    def accept(self, visitor, arg):
        raise NotImplementedError


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
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def accept(self, visitor, arg):
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
    """

    def __init__(self, num):
        self.num = num

    def accept(self, visitor, arg):
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
    """

    def __init__(self, identifier, exp_def, exp_body):
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(self, visitor, arg):
        """
        Accept a visitor in this `let` expression.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : int
            The resulting value of the expression.
        """

        return visitor.visit_let(self, arg)


class Fn(Expression):
    """
    This class represents an anonymous function.

    Attributes:
    -----------
    formal : str
        The formal parameter name for the function.
    body : Expression
        The expression representing the function's body.
    """

    def __init__(self, formal, body):
        self.formal = formal
        self.body = body

    def accept(self, visitor, arg):
        """
        Accept a visitor in this function.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : int
            The function itself.
        """

        return visitor.visit_fn(self, arg)


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
    """

    def __init__(self, function, actual):
        self.function = function
        self.actual = actual

    def accept(self, visitor, arg):
        """
        Accept a visitor in this function application.

        Parameters:
        -----------
        visitor : VisitorEval
            An instance of a visitor class.
        arg : dict[str, int]
            The environment to evaluate.

        Returns:
        --------
        : int
            The resulting value of the function application.
        """

        return visitor.visit_app(self, arg)


class Visitor(ABC):
    @abstractmethod
    def visit_var(self, exp, arg):
        """
        Visit a variable and return its contents.

        Parameters:
        -----------
        exp : Expression
            The `Expression` representation of this variable.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The contents of the variable in the given `env`.

        Raises:
        -------
        ValueError
            Raised if the variable's identifier is not found in `env`.
        """

        pass

    @abstractmethod
    def visit_num(self, exp, arg):
        """
        Visit a number and return its value.

        Parameters:
        -----------
        exp : Expression
            The `Expression` representation of this number.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values. This
            parameter is required, but ignored.

        Returns:
        --------
        : int
            The value of this number.
        """

        pass

    @abstractmethod
    def visit_let(self, exp, arg):
        """
        Visit a `let` expression and return its result.

        Parameters:
        -----------
        exp : Expression
            The `Expression` representation of this operation.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The result of `let.exp_body` evaluation.
        """

        pass

    @abstractmethod
    def visit_fn(self, exp, arg):
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

        pass

    @abstractmethod
    def visit_app(self, exp, arg):
        """
        Visit a function application and evaluate it.

        The application of function to actual parameter must contain two cases:

        1. An anonymous function is applied: (fn x => x + 1) 2
        2. A named function is applied: f 2, where f is fun f a = a + a

        The only difference between these two cases is that in the second we
        must augment the environment with the name of the named function.

        Parameters:
        -----------
        exp : Expression
            The `Expression` representation of this expression.
        env : dict[str, Union[bool, int]]
            A mapping between variables identifiers and their values.

        Returns:
        --------
        : Union[bool, int]
            The result of the function application.

        Raises:
        -------
        TypeError
            Raised if `exp.function` is not a `Function` object.
        """

        pass


class VisitorLocClassifier(Visitor):
    def visit_var(self, exp, arg):
        """
        >>> e0 = Var('v0')
        >>> e0.accept(VisitorLocClassifier(), None)
        set()
        """

        return set()

    def visit_num(self, exp, arg):
        """
        >>> e0 = Num(0)
        >>> e0.accept(VisitorLocClassifier(), None)
        set()
        """

        return set()

    def visit_let(self, exp, arg):
        """
        >>> e0 = Let('v', Num(0), Var('v'))
        >>> e0.accept(VisitorLocClassifier(), None)
        {'v'}

        >>> e0 = Fn('w', Var('w'))
        >>> e1 = Let('v', e0, e0)
        >>> e1.accept(VisitorLocClassifier(), None)
        {'v'}
        """

        globs = exp.exp_def.accept(self, arg)

        return {exp.identifier} | globs | exp.exp_body.accept(self, arg)

    def visit_fn(self, exp, arg):
        """
        >>> e0 = Fn('v0', Var('v0'))
        >>> e0.accept(VisitorLocClassifier(), None)
        set()
        """

        return set()

    def visit_app(self, exp, arg):
        """
        >>> e0 = Fn('w', Var('w'))
        >>> e1 = App(e0, Var('x'))
        >>> e1.accept(VisitorLocClassifier(), None)
        set()

        >>> e0 = Let('v', Fn('w', Var('w')), Var('v'))
        >>> e1 = App(e0, Num(0))
        >>> e1.accept(VisitorLocClassifier(), None)
        {'v'}

        >>> e0 = Let('v', Fn('w', Var('w')), Var('v'))
        >>> e1 = Let('x', Num(0), Var('x'))
        >>> e2 = App(e0, e1)
        >>> sorted(e2.accept(VisitorLocClassifier(), None))
        ['v', 'x']
        """

        globs = exp.function.accept(self, arg)
        return globs | exp.actual.accept(self, arg)

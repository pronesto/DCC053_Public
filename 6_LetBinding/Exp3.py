import sys
from abc import ABC, abstractmethod


class Store:
    """
    The `Store` class simulates memory management for variable storage.
    It maps locations (integers) to values and manages allocation of new
    locations.

    Attributes:
    -----------
    store : dict[int, int]
        A mapping of memory locations to values.
    next_loc : int
        The next available location in the store.

    Methods:
    --------
    allocate(value):
        Allocates a new memory location and stores the given value.
    update(loc, value):
        Updates the value at a given location.
    lookup(loc):
        Retrieves the value at a given location.
    """

    def __init__(self):
        self.store = {}
        self.next_loc = 0

    def allocate(self, value):
        """
        Allocate a new location in the store and associate it with `value`.

        Parameters:
        -----------
        value : int
            The value to store at the new location.

        Returns:
        --------
        int
            The allocated memory location.
        """
        loc = self.next_loc
        self.store[loc] = value
        self.next_loc += 1
        return loc

    def update(self, loc, value):
        """
        Update the value stored at the given location.

        Parameters:
        -----------
        loc : int
            The memory location to update.
        value : int
            The new value to store.

        Raises:
        -------
        KeyError:
            If the location does not exist in the store.
        """
        if loc in self.store:
            self.store[loc] = value
        else:
            raise KeyError(f"Location {loc} not found in store.")

    def lookup(self, loc):
        """
        Look up the value stored at the given location.

        Parameters:
        -----------
        loc : int
            The memory location.

        Returns:
        --------
        int
            The value stored at `loc`.
        """
        return self.store[loc]

    def __repr__(self):
        return str(self.store)


class Expression(ABC):
    """
    Abstract base class for all expressions.

    Methods:
    --------
    eval(env, store):
        Abstract method that should be implemented to evaluate the expression.
    """

    @abstractmethod
    def eval(self, env: dict[str, int], store: Store) -> int:
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
    eval(env, store):
        Returns the contents of a variable from a given environment.
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def eval(self, env: dict[str, int], store: Store) -> int:
        if self.identifier in env:
            loc = env[self.identifier]
            return store.lookup(loc)
        else:
            sys.exit(f"Variavel inexistente {self.identifier}")


class Assign(Expression):
    """
    This class represents a variable assignment.

    Attributes:
    -----------
    name : str
        The variable name being assigned.
    exp : Expression
        The expression whose evaluated value will be assigned.

    Methods:
    --------
    eval(env, store):
        Updates the store with the evaluated value of `exp` bound to `name`.

    Example:
    --------
    >>> env = {}
    >>> store = Store()
    >>> let_exp = Let("x", Num(5), Assign("x", Num(10)))
    >>> result = let_exp.eval(env, store)
    >>> store
    {0: 10}
    """

    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def eval(self, env, store):
        if self.name in env:
            loc = env[self.name]
            new_val = self.exp.eval(env, store)
            store.update(loc, new_val)
            return new_val
        else:
            sys.exit(f"Undefined variable {self.name}")


class Num(Expression):
    """
    This class represents expressions that are numbers.
    The evaluation of such an expression is the number itself.
    """

    def __init__(self, num: int) -> None:
        self.num = num

    def eval(self, env, store) -> int:
        """
        Evaluate this `Number`.

        Parameters:
        -----------
        env : dict[str, int]
            The environment (ignored for numbers).
        store : Store
            The store (ignored for numbers).

        Returns:
        --------
        int
            The numeric value.

        Examples:
        ---------
        >>> e = Num(3)
        >>> e.eval({}, Store())
        3
        """
        return self.num


class BinaryExpression(Expression):
    """
    Abstract base class for binary expressions.

    Attributes:
    -----------
    left : Expression
        The left operand.
    right : Expression
        The right operand.

    Methods:
    --------
    eval(env, store):
        Abstract method to evaluate the binary expression.
    """

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left: Expression = left
        self.right: Expression = right

    @abstractmethod
    def eval(self, env: dict[str, int], store: Store) -> int:
        raise NotImplementedError


class Add(BinaryExpression):
    """Represents addition of two expressions."""

    def eval(self, env: dict[str, int], store: Store) -> int:
        return self.left.eval(env, store) + self.right.eval(env, store)


class Sub(BinaryExpression):
    """Represents subtraction of two expressions."""

    def eval(self, env: dict[str, int], store: Store) -> int:
        return self.left.eval(env, store) - self.right.eval(env, store)


class Mul(BinaryExpression):
    """Represents multiplication of two expressions."""

    def eval(self, env: dict[str, int], store: Store) -> int:
        return self.left.eval(env, store) * self.right.eval(env, store)


class Div(BinaryExpression):
    """Represents integer division of two expressions."""

    def eval(self, env: dict[str, int], store: Store) -> int:
        return self.left.eval(env, store) // self.right.eval(env, store)


class Let(Expression):
    """
    Represents a `let` expression.

    Semantics of `let v <- e0 in e1`:
    1. Evaluate `e0` in environment `env` to yield `e0_val`.
    2. Allocate a location in the store for `e0_val`.
    3. Extend the environment with {v : loc}.
    4. Evaluate `e1` in the new environment.

    Examples:
    ---------
    >>> e = Let(identifier='v', exp_def=Num(42), exp_body=Var('v'))
    >>> e.eval({}, Store())
    42

    >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
    >>> e.eval({}, Store())
    42

    >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e.eval({}, Store())
    1764
    """

    def __init__(self, identifier: str, exp_def: Expression, exp_body: Expression) -> None:
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body

    def eval(self, env: dict[str, int], store: Store) -> int:
        e0_val = self.exp_def.eval(env, store)
        loc = store.allocate(e0_val)
        new_env = dict(env)
        new_env[self.identifier] = loc
        return self.exp_body.eval(new_env, store)

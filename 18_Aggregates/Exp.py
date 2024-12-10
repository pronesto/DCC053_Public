from abc import ABC, abstractmethod


class Expression(ABC):
    """
    Abstract base class for all expressions.
    """

    @abstractmethod
    def accept(self, visitor, arg):
        """
        Accept a visitor to process this expression.

        :param visitor: The visitor implementing the processing logic.
        :param arg: Optional argument to pass to the visitor.
        """
        raise NotImplementedError


# Expressions
class Var(Expression):
    """
    Represents a variable.

    :param name: The name of the variable.
    """

    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        return visitor.visit_var(self, arg)


class Num(Expression):
    """
    Represents a numeric constant.

    :param num: The numeric value.
    """

    def __init__(self, num):
        self.num = num

    def accept(self, visitor, arg):
        return visitor.visit_num(self, arg)


class Let(Expression):
    """
    Represents a let.

    :param name: The variable name to bind.
    :param exp_def: The defining expression.
    :param exp_body: The body expression.
    """

    def __init__(self, name, exp_def, exp_body):
        self.name = name
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(self, visitor, arg):
        return visitor.visit_let(self, arg)


class Assign(Expression):
    """
    Represents an assignment.

    :param exp_target: The target.
    :param exp_value: The value expression.
    """

    def __init__(self, exp_target, exp_value):
        self.exp_target = exp_target
        self.exp_value = exp_value

    def accept(self, visitor, arg):
        return visitor.visit_assign(self, arg)


class AddressOf(Expression):
    """
    Represents an address-of expression.

    :param name: The variable name.
    """

    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        return visitor.visit_address_of(self, arg)


class Dereference(Expression):
    """
    Represents a dereference expression.

    :param exp: The expression to dereference.
    """

    def __init__(self, exp):
        self.exp = exp

    def accept(self, visitor, arg):
        return visitor.visit_dereference(self, arg)


class Add(Expression):
    """
    Represents an addition expression.

    :param exp_left: The left operand expression.
    :param exp_right: The right operand expression.
    """

    def __init__(self, exp_left, exp_right):
        self.exp_left = exp_left
        self.exp_right = exp_right

    def accept(self, visitor, arg):
        return visitor.visit_add(self, arg)


# Visitor Interface and Evaluation Implementation
class Visitor(ABC):
    """
    Abstract base class for a visitor.
    """

    @abstractmethod
    def visit_var(self, var, arg):
        pass

    @abstractmethod
    def visit_num(self, num, arg):
        pass

    @abstractmethod
    def visit_let(self, let, arg):
        pass

    @abstractmethod
    def visit_assign(self, assign, arg):
        pass

    @abstractmethod
    def visit_address_of(self, address_of, arg):
        pass

    @abstractmethod
    def visit_dereference(self, dereference, arg):
        pass

    @abstractmethod
    def visit_add(self, add, arg):
        pass


class EvalVisitor(Visitor):
    """
    Visitor implementation for evaluating expressions.

    Example let x = 10 in x end
    >>> e0 = Let("x", Num(10), Var("x"))
    >>> v = EvalVisitor()
    >>> e0.accept(v, None)
    10

    let x = 42 in &x end
    >>> e = Let("x", Num(42), AddressOf("x"))
    >>> v = EvalVisitor()
    >>> e.accept(v, None)
    0

    !(let x = 42 in &x end)
    >>> e = Dereference(Let("x", Num(42), AddressOf("x")))
    >>> v = EvalVisitor()
    >>> e.accept(v, None)
    42

    let x = 1 in x := 2 end
    >>> e = Let("x", Num(1), Assign(Var("x"), Num(2)))
    >>> v = EvalVisitor()
    >>> e.accept(v, None)
    2

    let x = 1 in let y = 2 in &x := y end + x end
    >>> e0 = Let("y", Num(2), Assign(AddressOf("x"), Var("y")))
    >>> e1 = Let("x", Num(1), Add(e0, Var("x")))
    >>> v = EvalVisitor()
    >>> e1.accept(v, None)
    4

    let x = 1 in let y = 2 in 0 := y end + x end
    >>> e0 = Let("y", Num(2), Assign(Num(0), Var("y")))
    >>> e1 = Let("x", Num(1), Add(e0, Var("x")))
    >>> v = EvalVisitor()
    >>> e1.accept(v, None)
    4
    """

    def __init__(self):
        """
        Initializes the evaluation visitor with a context and memory store.
        """

        self.context = {}  # Variable context, e.g., {"x": loc}
        self.store = {}  # Memory store, e.g., {loc: value}
        self.next_location = 0  # To simulate fresh memory locations

    def fresh_location(self):
        """
        Generates a new memory location.

        :return: A unique memory location.
        """
        loc = self.next_location
        self.next_location += 1
        return loc

    def visit_var(self, var, _):  # No need for arg here
        """
        Retrieves the value of a variable.

        :param var: The variable expression.
        :param arg: Unused argument.
        :return: The value of the variable.
        """
        loc = self.context.get(var.name)
        if loc is None:
            raise ValueError(f"Variable '{var.name}' not found")
        return self.store[loc]

    def visit_num(self, num, _):
        """
        Returns the value of a numeric expression.

        :param num: The numeric expression.
        :param arg: Unused argument.
        :return: The numeric value.
        """
        return num.num

    def visit_let(self, let, arg):
        """
        Evaluates a let expression by binding a value to a variable and evaluating the body.

        :param let: The let expression.
        :param arg: Unused argument.
        :return: The result of evaluating the body expression.
        """
        value = let.exp_def.accept(self, arg)
        loc = self.fresh_location()
        self.context[let.name] = loc
        self.store[loc] = value
        return let.exp_body.accept(self, arg)

    def visit_assign(self, assign, arg):
        """
        Assigns a value to a memory location.

        :param assign: The assignment expression.
        :param arg: Unused argument.
        :return: The assigned value.
        """
        loc = assign.exp_target.accept(self, arg)
        value = assign.exp_value.accept(self, arg)
        self.store[loc] = value
        return value

    def visit_address_of(self, address_of, _):
        """
        Returns the memory location of a variable.

        :param address_of: The address-of expression.
        :param arg: Unused argument.
        :return: The memory location.
        """
        return self.context[address_of.name]

    def visit_dereference(self, dereference, arg):
        """
        Dereferences a memory location to retrieve its value.

        :param dereference: The dereference expression.
        :param arg: Unused argument.
        :return: The value at the memory location.
        """
        loc = dereference.exp.accept(self, arg)
        value = self.store.get(loc)
        if value is None:
            raise ValueError(f"Location {loc} not initialized")
        return value

    def visit_add(self, add, arg):
        """
        Evaluates an addition expression.

        :param add: The addition expression.
        :param arg: Unused argument.
        :return: The sum of the left and right operands.
        """
        left_val = add.exp_left.accept(self, arg)
        right_val = add.exp_right.accept(self, arg)
        return left_val + right_val

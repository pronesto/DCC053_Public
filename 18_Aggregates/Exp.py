from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def accept(self, visitor, arg):
        raise NotImplementedError

# Expressions
class Var(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        return visitor.visit_var(self, arg)

class Num(Expression):
    def __init__(self, num):
        self.num = num

    def accept(self, visitor, arg):
        return visitor.visit_num(self, arg)

class Let(Expression):
    def __init__(self, name, exp_def, exp_body):
        self.name = name
        self.exp_def = exp_def
        self.exp_body = exp_body

    def accept(self, visitor, arg):
        return visitor.visit_let(self, arg)

class Assign(Expression):
    def __init__(self, exp_target, exp_value):
        self.exp_target = exp_target
        self.exp_value = exp_value

    def accept(self, visitor, arg):
        return visitor.visit_assign(self, arg)

class AddressOf(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        return visitor.visit_address_of(self, arg)

class Dereference(Expression):
    def __init__(self, exp):
        self.exp = exp

    def accept(self, visitor, arg):
        return visitor.visit_dereference(self, arg)

class Add(Expression):
    def __init__(self, exp_left, exp_right):
        self.exp_left = exp_left
        self.exp_right = exp_right

    def accept(self, visitor, arg):
        return visitor.visit_add(self, arg)

# Visitor Interface and Evaluation Implementation
class Visitor(ABC):
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
        self.context = {}  # Variable context, e.g., {"x": loc}
        self.store = {}    # Memory store, e.g., {loc: value}
        self.next_location = 0  # To simulate fresh memory locations

    def fresh_location(self):
        loc = self.next_location
        self.next_location += 1
        return loc

    def visit_var(self, var, arg):
        loc = self.context.get(var.name)
        if loc is None:
            raise ValueError(f"Variable '{var.name}' not found")
        return self.store[loc]

    def visit_num(self, num, arg):
        return num.num

    def visit_let(self, let, arg):
        value = let.exp_def.accept(self, arg)
        loc = self.fresh_location()
        self.context[let.name] = loc
        self.store[loc] = value
        return let.exp_body.accept(self, arg)

    def visit_assign(self, assign, arg):
        loc = assign.exp_target.accept(self, arg)
        value = assign.exp_value.accept(self, arg)
        self.store[loc] = value
        return value

    def visit_address_of(self, address_of, arg):
        return self.context[address_of.name]

    def visit_dereference(self, dereference, arg):
        loc = dereference.exp.accept(self, arg)
        value = self.store.get(loc)
        if value is None:
            raise ValueError(f"Location {loc} not initialized")
        return value

    def visit_add(self, add, arg):
        left_val = add.exp_left.accept(self, arg)
        right_val = add.exp_right.accept(self, arg)
        return left_val + right_val


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

class Add(BinaryExpression):
    """
    This class represents addition of two expressions. The evaluation of such
    an expression is the addition of the two subexpression's values.
    """
    def accept(self, visitor, arg):
        return visitor.visit_add(self, arg)

class Sub(BinaryExpression):
    """
    This class represents subtraction of two expressions. The evaluation of such
    an expression is the subtraction of the two subexpression's values.
    """
    def accept(self, visitor, arg):
        return visitor.visit_sub(self, arg)

class Mul(BinaryExpression):
    """
    This class represents multiplication of two expressions. The evaluation of
    such an expression is the product of the two subexpression's values.
    """
    def accept(self, visitor, arg):
        return visitor.visit_mul(self, arg)

class Div(BinaryExpression):
    """
    This class represents the integer division of two expressions. The
    evaluation of such an expression is the integer quocient of the two
    subexpression's values.
    """
    def accept(self, visitor, arg):
        return visitor.visit_div(self, arg)

class And(BinaryExpression):
    """
    This class represents the logical disjunction of two boolean expressions.
    The evaluation of an expression of this kind is the logical AND of the two
    subexpression's values.
    """
    def accept(self, visitor, arg):
        return visitor.visit_and(self, arg)

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

    The let expression is the only expression where variable names can be
    associated with types. For instance, if we create an expression like:
    Let('v', int, e0, e1), then we are saying that variable 'v' must have
    type int.
    """
    def __init__(self, identifier, type_identifier, exp_def, exp_body):
        self.identifier = identifier
        self.tp_var = type_identifier
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
        if def_type == let_exp.tp_var:
            # Temporarily extend the environment with the new variable
            new_env = dict(env)
            new_env[let_exp.identifier] = let_exp.tp_var
            # Restore the environment
            return let_exp.exp_body.accept(self, new_env)
        else:
            epct_str = f"expected {let_exp.tp_var}"
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

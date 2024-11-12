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

    >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> v = VisitorEval()
    >>> print(e.accept(v, {}))
    1764
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
    
    def visit_sub(self, sub, env):
        return sub.left.accept(self, env) - sub.right.accept(self, env)
    
    def visit_mul(self, mul, env):
        return mul.left.accept(self, env) * mul.right.accept(self, env)
    
    def visit_div(self, div, env):
        return div.left.accept(self, env) // div.right.accept(self, env)

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
        new_env[let.identifier]= e0_val
        return let.exp_body.accept(self, new_env)

class TypeError(Exception):
    pass

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

def type_safe_eval(e):
    v = VisitorTypeSafeEval()
    try:
        return e.accept(v, {})
    except TypeError as tp_error:
        print(tp_error)

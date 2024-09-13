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

class VisitorStr:
    """
    Pretty print an expression based on its type.

    Example:
    >>> e = Let('v', Num(42), Var('v'))
    >>> v = VisitorStr()
    >>> print(e.accept(v, None))
    let v = 42 in v end

    >>> e = Let('v', Num(40), Let('w', Num(2), Add(Var('v'), Var('w'))))
    >>> v = VisitorStr()
    >>> print(e.accept(v, None))
    let v = 40 in let w = 2 in (v + w) end end

    >>> e = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> v = VisitorStr()
    >>> print(e.accept(v, None))
    let v = (40 + 2) in (v * v) end
    """
    def visit_var(self, var, arg):
        return var.identifier
    
    def visit_num(self, num, arg):
        return str(num.num)
    
    def visit_add(self, add, arg):
        return f"({add.left.accept(self, arg)} + {add.right.accept(self, arg)})"
    
    def visit_sub(self, sub, arg):
        return f"({sub.left.accept(self, arg)} - {sub.right.accept(self, arg)})"
    
    def visit_mul(self, mul, arg):
        return f"({mul.left.accept(self, arg)} * {mul.right.accept(self, arg)})"
    
    def visit_div(self, div, arg):
        return f"({div.left.accept(self, arg)} / {div.right.accept(self, arg)})"
    
    def visit_let(self, let, arg):
        def_str = let.exp_def.accept(self, arg)
        def_body = let.exp_body.accept(self, arg)
        return f"let {let.identifier} = {def_str} in {def_body} end"

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
    
    def visit_add(self, add, env):
        return add.left.accept(self, env) + add.right.accept(self, env)
    
    def visit_sub(self, sub, env):
        return sub.left.accept(self, env) - sub.right.accept(self, env)
    
    def visit_mul(self, mul, env):
        return mul.left.accept(self, env) * mul.right.accept(self, env)
    
    def visit_div(self, div, env):
        return div.left.accept(self, env) // div.right.accept(self, env)
    
    def visit_let(self, let, env):
        e0_val = let.exp_def.accept(self, env)
        new_env = dict(env)
        new_env[let.identifier]= e0_val
        return let.exp_body.accept(self, new_env)

class VisitorOptimize:
    """
    This visitor optimizes expressions, folding operations that involve only
    numbers.

    Example:
    >>> e0 = Add(Num(40), Num(2))
    >>> optimizer = VisitorOptimize()
    >>> e1 = e0.accept(optimizer, {})
    >>> printer = VisitorStr()
    >>> print(e1.accept(printer, None))
    42

    >>> e0 = Let('v', Add(Num(1), Num(1)), Add(Num(40), Var('v')))
    >>> optimizer = VisitorOptimize()
    >>> e1 = e0.accept(optimizer, {})
    >>> printer = VisitorStr()
    >>> print(e1.accept(printer, None))
    let v = 2 in (40 + v) end
    """
    def visit_var(self, var, env):
        return var
    
    def visit_num(self, num, env):
        return num
    
    def visit_add(self, add, env):
        left = add.left.accept(self, env)
        right = add.right.accept(self, env)
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.num + right.num)
        return Add(left, right)
    
    def visit_sub(self, sub, env):
        left = sub.left.accept(self, env)
        right = sub.right.accept(self, env)
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.num - right.num)
        return Sub(left, right)
    
    def visit_mul(self, mul, env):
        left = mul.left.accept(self, env)
        right = mul.right.accept(self, env)
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.num * right.num)
        return Mul(left, right)
    
    def visit_div(self, div, env):
        left = div.left.accept(self, env)
        right = div.right.accept(self, env)
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.num // right.num)
        return Div(left, right)
    
    def visit_let(self, let, env):
        new_def = let.exp_def.accept(self, env)
        new_body = let.exp_body.accept(self, env)
        return Let(let.identifier, new_def, new_body)

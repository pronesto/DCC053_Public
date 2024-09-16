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
    def __init__(self):
        # The environment mapping variable names to their types
        self.env = {}

    def visit_var(self, var_exp, arg):
        # Look up the variable's type in the environment
        if var_exp.identifier in self.env:
            return self.env[var_exp.identifier]
        else:
            raise TypeError(f"Variable {var_exp.identifier} is not defined")

    def visit_num(self, num_exp, arg):
        # Numbers are always of type 'int'
        return 'int'

    def visit_bln(self, bln_exp, arg):
        # Boolean literals are always of type 'bool'
        return 'bool'

    def visit_add(self, add_exp, arg):
        # Both operands must be of type 'int'
        left_type = add_exp.left.accept(self, arg)
        right_type = add_exp.right.accept(self, arg)
        if left_type == 'int' and right_type == 'int':
            return 'int'
        else:
            raise TypeError(f"Type error: {left_type} + {right_type}")

    def visit_sub(self, sub_exp, arg):
        # Both operands must be of type 'int'
        left_type = sub_exp.left.accept(self, arg)
        right_type = sub_exp.right.accept(self, arg)
        if left_type == 'int' and right_type == 'int':
            return 'int'
        else:
            raise TypeError(f"Type error: {left_type} - {right_type}")

    def visit_mul(self, mul_exp, arg):
        # Both operands must be of type 'int'
        left_type = mul_exp.left.accept(self, arg)
        right_type = mul_exp.right.accept(self, arg)
        if left_type == 'int' and right_type == 'int':
            return 'int'
        else:
            raise TypeError(f"Type error: {left_type} * {right_type}")

    def visit_div(self, div_exp, arg):
        # Both operands must be of type 'int'
        left_type = div_exp.left.accept(self, arg)
        right_type = div_exp.right.accept(self, arg)
        if left_type == 'int' and right_type == 'int':
            return 'int'
        else:
            raise TypeError(f"Type error: {left_type} / {right_type}")

    def visit_and(self, and_exp, arg):
        # Both operands must be of type 'bool'
        left_type = and_exp.left.accept(self, arg)
        right_type = and_exp.right.accept(self, arg)
        if left_type == 'bool' and right_type == 'bool':
            return 'bool'
        else:
            raise TypeError(f"Type error: {left_type} and {right_type}")

    def visit_lth(self, lth_exp, arg):
        # Both operands must be of type 'int' and result is of type 'bool'
        left_type = lth_exp.left.accept(self, arg)
        right_type = lth_exp.right.accept(self, arg)
        if left_type == 'int' and right_type == 'int':
            return 'bool'
        else:
            raise TypeError(f"Type error: {left_type} < {right_type}")

    def visit_let(self, let_exp, arg):
        # Type-check the definition and bind it to the environment
        def_type = let_exp.exp_def.accept(self, arg)
        if def_type == let_exp.tp_var:
            # Temporarily extend the environment with the new variable
            old_env = self.env.copy()
            self.env[let_exp.identifier] = let_exp.tp_var
            body_type = let_exp.exp_body.accept(self, arg)
            # Restore the environment
            self.env = old_env
            return body_type
        else:
            epct_str = f"expected {let_exp.tp_var}"
            raise TypeError(f"Type error in let: {epct_str} but got {def_type}")

    def visit_ifThenElse(self, if_exp, arg):
        # The condition must be of type 'bool', and both branches must have
        # the same type
        cond_type = if_exp.cond.accept(self, arg)
        if cond_type != 'bool':
            raise TypeError(f"Type error: expected bool but got {cond_type}")
        then_type = if_exp.e0.accept(self, arg)
        else_type = if_exp.e1.accept(self, arg)
        if then_type == else_type:
            return then_type
        else:
            then_str = f"then branch is {then_type}"
            else_str = f"else branch is {else_type}"
            raise TypeError(f"Type error: {then_str}, {else_str}")

# Example Usage
env = {'x': 'int', 'y': 'bool'}
checker = TypeChecker()
checker.env = env

# Example expressions:
expr = Add(Var('x'), Num(5))  # x + 5
print(expr.accept(checker, None))  # Should return 'int'

expr2 = IfThenElse(Var('y'), Num(1), Num(0))  # if y then 1 else 0
print(expr2.accept(checker, None))  # Should return 'int'

expr3 = Let('z', 'int', Num(3), Add(Var('z'), Num(2)))  # let z = 3 in z + 2
print(expr3.accept(checker, None))  # Should return 'int'

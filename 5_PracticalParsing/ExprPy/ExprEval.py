from ExprListener import ExprListener
from ExprParser import ExprParser

class ExprEval(ExprListener):

    def __init__(self):
        # Stack to store intermediate values during traversal
        self.stack = []

    def exitExpr(self, ctx: ExprParser.ExprContext):
        # Check if the expression is of the form expr + term
        if ctx.getChildCount() == 3:
            right = self.stack.pop()
            left = self.stack.pop()
            if ctx.getChild(1).getText() == '+':
                self.stack.append(left + right)
            else:
                raise ValueError(f"Unexpected operation {ctx.getChild(1).getText()}")

    def exitTerm(self, ctx: ExprParser.TermContext):
        # Check if the term is of the form term * factor
        if ctx.getChildCount() == 3:
            right = self.stack.pop()
            left = self.stack.pop()
            if ctx.getChild(1).getText() == '*':
                self.stack.append(left * right)
            else:
                raise ValueError(f"Unexpected operation {ctx.getChild(1).getText()}")

    def exitFactor(self, ctx: ExprParser.FactorContext):
        # Handle parentheses and numbers
        if ctx.getChildCount() == 3:
            # It's a parentheses expression like ( expr )
            value = self.stack.pop()  # The value inside the parentheses
            self.stack.append(value)
        elif ctx.NUMBER() is not None:
            # It's a number
            number = int(ctx.NUMBER().getText())
            self.stack.append(number)

    def getResult(self):
        # After parsing is complete, the result will be the last value in the stack
        return self.stack.pop()

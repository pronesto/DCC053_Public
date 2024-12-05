from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def accept(self, visitor, arg):
        raise NotImplementedError

class Var(Expression):
    def __init__(self, identifier):
        self.identifier = identifier
    def accept(self, visitor, arg):
        return visitor.visit_var(self, arg)

class Num(Expression):
    def __init__(self, num):
        self.num = num
    def accept(self, visitor, arg):
        return visitor.visit_num(self, arg)

class Let(Expression):
    def __init__(self, identifier, exp_def, exp_body):
        self.identifier = identifier
        self.exp_def = exp_def
        self.exp_body = exp_body
    def accept(self, visitor, arg):
        return visitor.visit_let(self, arg)

class Fn(Expression):
    def __init__(self, formal, body):
        self.formal = formal
        self.body = body
    def accept(self, visitor, arg):
        return visitor.visit_fn(self, arg)

class App(Expression):
    def __init__(self, function, actual):
        self.function = function
        self.actual = actual
    def accept(self, visitor, arg):
        return visitor.visit_app(self, arg)

class Visitor(ABC):
    @abstractmethod
    def visit_var(self, exp, arg):
        pass

    @abstractmethod
    def visit_num(self, exp, arg):
        pass

    @abstractmethod
    def visit_let(self, exp, arg):
        pass

    @abstractmethod
    def visit_fn(self, exp, arg):
        pass

    @abstractmethod
    def visit_app(self, exp, arg):
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

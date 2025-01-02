"""
This file contains the implementation of a simple interpreter of low-level
instructions. The interpreter takes a program, represented as its first
instruction, plus an environment, which is a stack of bindings. Bindings are
pairs of variable names and values. New bindings are added to the stack
whenever new variables are defined. Bindings are never removed from the stack.
In this way, we can inspect the history of state transformations caused by the
interpretation of a program.

This file uses doctests all over. To test it, just run Python 3 as follows:
`python3 -m doctest lang.py`. The program uses syntax that is excluive of
Python 3. It will not work with standard Python 2.
"""

from collections import deque
from abc import ABC, abstractmethod


class Env:
    """
    A table that associates variables with values. The environment is
    implemented as a stack, so that previous bindings of a variable V remain
    available in the environment if V is overassigned.

    Attributes:
    -----------
    initial_args : dict (optional)
        A dictionary of `var: value` mappings to initialize the environment
        with.

    Examples:
    ---------
    >>> e = Env()
    >>> e.set("a", 2)
    >>> e.set("a", 3)
    >>> e.get("a")
    3

    >>> e = Env({"b": 5})
    >>> e.set("a", 2)
    >>> e.get("a") + e.get("b")
    7
    """

    def __init__(s, initial_args=None):
        s.env = deque()

        if initial_args is not None:
            for var, value in initial_args.items():
                s.env.appendleft((var, value))

    def get(self, var):
        """
        Return the first occurence of variable `var` in the environment stack.

        Parameters:
        -----------
        var : str
            The variable to look for.

        Returns:
        --------
        val : int
            The value associated with `var` in the environment.

        Raises:
        -------
        LookupError
            Raised if `var` is not declared in this environment.
        """

        val = next((value for (e_var, value) in self.env if e_var == var), None)

        if val is not None:
            return val

        else:
            raise LookupError(f"Absent key {var}")

    def set(s, var, value):
        """
        Add `var` to the environment, and map it to `value`.

        The `var: value` binding is placed on the top of the environment stack.

        Parameters:
        -----------
        var : str
            The variable identifier.
        value : int
            The variable value.
        """

        s.env.appendleft((var, value))

    def dump(s):
        """
        Print the contents of the environment.

        This method is mostly used for debugging purposes.
        """

        for var, value in s.env:
            print(f"{var}: {value}")


class Inst(ABC):
    """
    The representation of instructions. All that an instruction has, that is
    common among all the instructions, is the `next_inst` attribute. This
    attribute determines the next instruction that will be fetched after this
    instruction runs. Also, every instruction has an index, which is always
    different. The index is incremented whenever a new instruction is created.

    Attributes:
    -----------
    nexts : list of Inst
        The next instructions.
    preds : list of Inst
        The previous instructions.
    ID : int
        The instruction identifier.
    """

    next_index = 0

    def __init__(self):
        self.nexts = []
        self.preds = []
        self.ID = Inst.next_index
        Inst.next_index += 1

    def add_next(self, next_inst):
        """
        Add the next instruction.

        This affects both this' `nexts` and `next_inst.preds` attributes.

        Parameters:
        -----------
        next_inst : Inst
            The next instruction.
        """

        self.nexts.append(next_inst)
        next_inst.preds.append(self)

    @classmethod
    @abstractmethod
    def definition(self):
        """
        Get the set of definitions of this instruction.

        Returns:
        --------
        : set of Inst
            The set of definitions of this instruction.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def uses(self):
        """
        Get the set of uses of this instruction.

        Returns:
        --------
        : set of Inst
            The set of uses of this instruction.
        """
        raise NotImplementedError

    @abstractmethod
    def eval(self, env):
        """
        Evaluate this instruction in some environment.

        Parameters:
        -----------
        env : dict
            The environment to evaluate this instruction in. The environment
            maps identifiers to values.

        Returns:
        --------
        : int or bool
            The result of the instruction evaluation.
        """

        raise NotImplementedError

    def get_next(self):
        """
        Get the next instruction.

        Returns:
        --------
        : Inst or None
            The next instruction, if any. If there isn't a next instruction
            (i.e., `self.nexts` is empty), return None.
        """

        if len(self.nexts) > 0:
            return self.nexts[0]

        else:
            return None


class BinOp(Inst):
    """
    The general class of binary instructions. These instructions defines a
    value, and uses two values. As such, it contains a routine to extract the
    defined value, and the list of used values.

    Attributes:
    -----------
    dst : Inst
        The destination.
    src0 : Inst
        The first used value.
    src1 : Inst
        The second used value.
    """

    def __init__(s, dst, src0, src1):
        s.dst = dst
        s.src0 = src0
        s.src1 = src1
        super().__init__()

    @classmethod
    @abstractmethod
    def get_opcode(self):
        """
        Get the operation code regarding this `BinOp`.

        Returns:
        --------
        : str
            The operation code.
        """

        raise NotImplementedError

    def definition(s):
        return set([s.dst])

    def uses(s):
        return set([s.src0, s.src1])

    def __str__(self):
        op = self.get_opcode()

        inst_s = f"{self.ID}: {self.dst} = {self.src0}{op}{self.src1}"
        pred_s = f"\n  P: {', '.join([str(inst.ID) for inst in self.preds])}"
        next_s = f"\n  N: {self.nexts[0].ID if len(self.nexts) > 0 else ''}"

        return inst_s + pred_s + next_s


class Add(BinOp):
    """
    This class represents the addition of two variables.

    Examples:
    ---------
    >>> a = Add("a", "b0", "b1")
    >>> e = Env({"b0": 2, "b1": 3})
    >>> a.eval(e)
    >>> e.get("a")
    5

    >>> a = Add("a", "b0", "b1")
    >>> a.get_next() == None
    True
    """

    def eval(self, env):
        env.set(self.dst, env.get(self.src0) + env.get(self.src1))

    def get_opcode(self):
        return "+"


class Mul(BinOp):
    """
    This class represents the multiplication of two variables.

    Examples:
    ---------
    >>> a = Mul("a", "b0", "b1")
    >>> e = Env({"b0": 2, "b1": 3})
    >>> a.eval(e)
    >>> e.get("a")
    6
    """

    def eval(s, env):
        env.set(s.dst, env.get(s.src0) * env.get(s.src1))

    def get_opcode(self):
        return "*"


class Lth(BinOp):
    """
    This class represents the "less than" comparison of two variables.

    Examples:
    ---------
    >>> a = Lth("a", "b0", "b1")
    >>> e = Env({"b0": 2, "b1": 3})
    >>> a.eval(e)
    >>> e.get("a")
    True

    >>> a = Lth("a", "b0", "b1")
    >>> e = Env({"b0": 23, "b1": 3})
    >>> a.eval(e)
    >>> e.get("a")
    False
    """

    def eval(s, env):
        env.set(s.dst, env.get(s.src0) < env.get(s.src1))

    def get_opcode(self):
        return "<"


class Geq(BinOp):
    """
    This class represents the "greater than or equal to" comparison of two
    variables.

    Examples:
    ---------
    >>> a = Geq("a", "b0", "b1")
    >>> e = Env({"b0": 2, "b1": 3})
    >>> a.eval(e)
    >>> e.get("a")
    False

    >>> a = Geq("a", "b0", "b1")
    >>> e = Env({"b0": 2, "b1": 2})
    >>> a.eval(e)
    >>> e.get("a")
    True

    >>> a = Geq("a", "b0", "b1")
    >>> e = Env({"b0": 23, "b1": 2})
    >>> a.eval(e)
    >>> e.get("a")
    True
    """

    def eval(s, env):
        env.set(s.dst, env.get(s.src0) >= env.get(s.src1))

    def get_opcode(self):
        return ">="


class Bt(Inst):
    """
    This is a Branch-If-True instruction, which diverts the control flow to the
    `true_dst` if the predicate `pred` is `True`, and to the `false_dst`
    otherwise.

    Examples:
    ---------
    >>> e = Env({"t": True, "x": 0})
    >>> a = Add("x", "x", "x")
    >>> m = Mul("x", "x", "x")
    >>> b = Bt("t", a, m)
    >>> b.eval(e)
    >>> b.get_next() == a
    True
    """

    def __init__(s, cond, true_dst=None, false_dst=None):
        super().__init__()

        s.cond = cond
        s.nexts = [true_dst, false_dst]

        if true_dst != None:
            true_dst.preds.append(s)

        if false_dst != None:
            false_dst.preds.append(s)

    def definition(s):
        return set()

    def uses(s):
        return set([s.cond])

    def add_true_next(s, true_dst):
        """
        Set the destination instruction if `cond` evaluates to `True`.

        Parameters:
        -----------
        true_dst : Inst
            The destination instruction.
        """

        s.nexts[0] = true_dst
        true_dst.preds.append(s)

    def add_next(s, false_dst):
        """
        Set the destination instruction if `cond` evaluates to `False`.

        Parameters:
        -----------
        true_dst : Inst
            The destination instruction.
        """

        s.nexts[1] = false_dst
        false_dst.preds.append(s)

    def eval(s, env):
        """
        Evaluate `cond` and determine the next instruction.

        The evaluation of the condition sets the `next_iter` to the instruction.
        This value determines which successor instruction is to be evaluated.
        Any values greater than 0 are evaluated as `True`, while 0 corresponds
        to False.

        Parameters:
        -----------
        env : dict
            The environment to evaluate this instruction in. The environment
            maps identifiers to values.
        """

        if env.get(s.cond):
            s.next_iter = 0
        else:
            s.next_iter = 1

    def get_next(s):
        return s.nexts[s.next_iter]

    def __str__(self):
        inst_s = f"{self.ID}: bt {self.cond}"
        pred_s = f"\n  P: {', '.join([str(inst.ID) for inst in self.preds])}"
        next_s = f"\n  NT:{self.nexts[0].ID} NF:{self.nexts[1].ID}"
        return inst_s + pred_s + next_s


def interp(instruction, environment):
    """
    Evaluate a program until there are no more instructions to evaluate.

    Parameters:
    -----------
    instruction : Inst
        The initial instruction of the program.
    environment : dict
        The initial environment of the program.

    Returns:
    --------
    environment : dict
        The final environment after interpreting the program.

    Examples:
    ---------
    >>> env = Env({"m": 3, "n": 2, "zero": 0})
    >>> m_min = Add("answer", "m", "zero")
    >>> n_min = Add("answer", "n", "zero")
    >>> p = Lth("p", "n", "m")
    >>> b = Bt("p", n_min, m_min)
    >>> p.add_next(b)
    >>> interp(p, env).get("answer")
    2
    """

    if instruction:
        instruction.eval(environment)
        return interp(instruction.get_next(), environment)
    else:
        return environment

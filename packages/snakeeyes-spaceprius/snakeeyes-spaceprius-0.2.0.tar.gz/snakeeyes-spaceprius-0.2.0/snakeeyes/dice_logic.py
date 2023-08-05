"""
Handles the actual logic of dice rolls

Classes
-------
Roll

Functions
---------
roll
"""
import math
import random
import re
import logging
from .elements import DiceGroup, Exploding, Successes, Die

import ast
import operator

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}


def arithmeticEval(s):
    """
    Evaluate an operator.

    Args:
        s: (todo): write your description
    """
    node = ast.parse(s, mode='eval')

    def _eval(node):
        """
        Evaluate an ast node.

        Args:
            node: (todo): write your description
        """
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Str):
            return node.s
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)


logger = logging.getLogger('snakeeyes.dicelogic')


op_dict = {
    ">": Successes,
    "x": Exploding,
}


def roll(die: Die):
    """
    Takes Die object and returns a tuple containing a list of results, and a total of of all rolls.

    Parameters
    ----------

    die : elements.Die
    """
    if die:
        dice_array = []
        for i in range(die.quantity):
            dice_array.append(math.ceil(random.random() * die.sides))
        dice_total = 0
        for r in dice_array:
            dice_total += r
        return (dice_array, dice_total)
    else:
        return False


class Roll():

    """A class which takes a string and outputs a dice roll

    Parameters
    ----------
    string : str
        The input string

    Attributes
    ----------
    dicer_regex : str
        Regex showing how to extract just the dice string from an object
    op_dict : dict
        dictionary containing the characters of an operator, and the assosciated class
    die : elements.Die
        Dice roll using string input
    results : list of int
        List of results from dice rolled
    total : int
        The total of all dice rolled

    Methods
    -------
    op_collection(die)
        Return operator class list
    op_evaluate(ops)
        Return the final result of all operators

    """

    dice_regex = re.compile(r"\d*d\d*(?:[^d\d\(\)+\-\*/]\d*)*")
    math_regex = re.compile(r"[\(\)+*-\/\d]+")

    @staticmethod
    def op_collection(die: Die):
        """
        Take die object and return list of operator classes.

        Parameters
        ----------
        die : elements.Die

        Returns
        -------
        ops : list of (elements.operator, int)
        """
        oper = []
        for o in die.ops:
            try:
                operator = op_dict[o[0]]
                op = (operator, o[1])
                oper.append(op)
            except KeyError:
                continue
        oper = sorted(oper, key=lambda op: op[0].priority)
        return oper

    @staticmethod
    def op_evaluate(die: Die, ops: list, results: list):
        """Take results and operators and return a final result."""
        last_output = results
        last_output = ops[0].evaluate(last_output, ops[1], die)
        return last_output

    def __init__(self, string: str):
        """
        Init results from the input string.

        Args:
            self: (todo): write your description
            string: (todo): write your description
        """
        self.string = string
        logger.debug("Trying!")
        self.die = DiceGroup(self.string)
        self.rolls = []
        self.total = 0
        self.results = []
        self.successes = False
        if self.die.dice:
            # If there are actual dice in the roll, then do this
            for d in self.die.dice:
                r = roll(d)
                self.rolls.append((r, d.string, d))
            for r in self.rolls:
                # This is here to basically turn all the rolls into usable stuff and then output it
                # in a way that actually makes sense
                tempstring = re.compile(rf"{r[1]}")
                if r[0]:
                    tempresults = r[0][0]
                    self.string = tempstring.sub(f"{r[0][1]}", self.string)
                    self.total += r[0][1]
                    if r[2].ops:
                        for o in self.op_collection(r[2]):
                            tempresults = self.op_evaluate(r[2], o, tempresults)
                            if o[0] is Successes:
                                self.successes = True
                                break
                    self.results.append((r[1], tempresults))
        self.final = arithmeticEval(self.string)

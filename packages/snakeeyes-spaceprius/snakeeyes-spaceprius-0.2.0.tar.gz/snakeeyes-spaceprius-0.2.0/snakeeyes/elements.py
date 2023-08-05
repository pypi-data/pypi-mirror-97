"""
Handles the Grammar of the document

Classes
-------
- DiceString
- Die
- Operator
    - LeftHandOperator
        - Successes
        - Exploding

"""
import logging
import math
import random
import re

logger = logging.getLogger('snakeeyes.elements')


class Die():
    """
    Generates the dice string to put through the system

        Attributes
        ----------
        parsestring : Pattern
            Regex pattern to detect the various attributes of a dice roll

        quantity : int
            Number of times die must be rolled

        sides : int
            Number of sides a die has

    """
    sides = 0
    quantity = 0

    def __init__(self, quantity: int, sides: int, oplist: list, string: str):
        """
        Initialize the string.

        Args:
            self: (todo): The instance
            quantity: (int): Number of dice to be rolled
            sides: (int): String which contains the sides of each die. Should be castable to int.
        """
        logger.debug("Initating DiceString")
        try:
            self.quantity = quantity
            self.sides = sides
            self.ops = oplist
            self.string = string
            logger.debug("Sides: %i \n Quantity: %i ",
                         self.sides, self.quantity)
        except (ValueError, AttributeError):
            pass


class DiceGroup():
    """Class that handles dice rolls using regular expressions.

    Attributes
    ----------
    string : str
        String to be processed
    dice : list
        List of dice rolled.
    """
    parsestring = re.compile(r"(?P<quantity> \d* (?=d\d*)) d (?P<sides>\d*)(?:[x\>]\d*)*", re.X)
    parseops = re.compile(r"(?P<operator>[x\>]) (?P<operands>\d*)", re.X)

    def __init__(self, string: str):
        """
        Initialize a group of dice from the string.

        Args:
            self: The Instance.
            string: (str): The string to be processed.
        """
        self.string = string
        logger.debug("String: %s", self.string)
        __dice = self.parsestring.finditer(string)
        self.dice = []
        for d in __dice:
            # Intiialize the dice
            quant = int(d.group('quantity'))
            sides = int(d.group('sides'))
            dstring = d.group()
            ops = self.parseops.finditer(dstring)
            opslist = []
            for o in ops:
                # initialize operator tuples
                optuple = (o.group('operator'), int(o.group('operands')))
                opslist.append(optuple)
            dicestring = Die(quant, sides, opslist, dstring)
            self.dice.append(dicestring)

            logger.debug(f"Oplist: {opslist}")
        logger.debug(f"Dice: {self.dice}")

    def __bool__(self):
        """
        Returns true if the dice is true false otherwise.

        Args:
            self:: The instance
        """
        if self.dice:
            logger.debug("Die is true")
            return True
        return False


class Operator():
    """Handles creating operators for use in rolls.

    ...

    Attributes
    ----------
    char : str
        character for operand
    regex : str
        raw string, by default just detects the character

    Functions
    -------
    parse - Take the string and output operator and operands
    evaluate - Blank method where the operator is processed

    """
    priority = 0
    char = r""

    @classmethod
    def evaluate(cls, results: list, operand: int, die: Die):
        """
        Evaluate the given dice.

        Args:
            cls: (callable): The class
            dice: (Die): The Die being rolled
        """


class LeftHandOperator(Operator):
    """Operators that act on the object to the left, using the object on the right, inherits from Operator.

    Attributes
    ----------
    operand : str
        The arguments taken by the operator

    """
    operand = r"\d*"


class Successes(LeftHandOperator):
    """Takes an operand and calculates how many successes there have been."""
    priority = 7
    char = r"\>"

    @classmethod
    def evaluate(cls, results: list, operand: int, die: Die):
        """
        Evaluate a list of results.

        Args:
            cls: (callable): The Class
            results: (list): List of Results.
            operand: (int): The threshold after which die count as successes.
            die: (Die): The Die roll.
        """
        dice_list = []
        logger.debug("Evaluating successes!")
        for d in results:
            if d > int(operand):
                dice_list.append((d, True))
            else:
                dice_list.append((d, False))

        return dice_list


class Exploding(LeftHandOperator):
    """
    Takes dice results, and if the value is greater than the threshold, rolls another die.
    """
    priority = 1
    char = r"x"

    @classmethod
    def evaluate(cls, results: list, operand: int, die: Die):
        """
        Evaluate the objective function.

        Args:
            cls: (callable): The class
            results: (list): The list of results
            operand: (int): The threshold at which the die is rerolled
            die: (Die): The Die being rolled
        """
        eval_results = results
        logger.debug("Evaluating Exploding!")
        for d in results:
            logger.debug("D is: %i", d)
            r = d
            logger.debug("Operand: %i", operand)
            while r >= operand:
                logger.debug("Exploded!")
                temp_roll = math.ceil(random.random() * die.sides)
                r = temp_roll
                logger.debug(" R is %i", r)
                eval_results.append(temp_roll)
                if r >= operand:
                    break
        logger.debug("Exploded dice: %s", str(eval_results))
        return eval_results

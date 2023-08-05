"""A python dice library."""
from .dice_logic import Roll
from .elements import Die, DiceGroup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('snakeeyes')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='snakeeyes.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

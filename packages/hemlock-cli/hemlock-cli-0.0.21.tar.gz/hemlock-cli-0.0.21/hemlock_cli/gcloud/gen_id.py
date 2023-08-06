"""Generate a random name"""

from string import ascii_lowercase, digits
from random import choice
import sys

chars = ascii_lowercase + digits
base = sys.argv[1]
print(base+'-'+''.join([choice(chars) for i in range(10)]))
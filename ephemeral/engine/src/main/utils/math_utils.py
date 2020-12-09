"""Library containing useful math utilities.
"""

import string
import random


def get_random_string(length):
    """Returns a random string containing letters and digits of length N.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

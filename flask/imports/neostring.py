import string
import random as rdm

def random(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(rdm.choice(chars) for _ in range(size))
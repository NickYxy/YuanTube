__author__ = 'nickyuan'

from enum import Enum,unique

@unique
class Week(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

w1 = Week.Friday

print(w1.value)
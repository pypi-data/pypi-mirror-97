# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:25
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :hut.py

from gameutils import bold


class Hut:
    """Class to create hut object(s) in the game Attack of the Ocrs"""

    def __init__(self, number, occupant):
        self.occupant = occupant
        self.number = number
        self.isacquired = False

    def acquire(self, new_occupant):
        """Update the occupant of the hut"""
        self.occupant = new_occupant
        self.isacquired = True
        print(bold(f"GOOD JOB! Hut {self.number} acquired"))

    def get_occupant_type(self):
        """Return a string giving info on the hut occupant"""
        if self.isacquired:
            occupant_type = "ACQUIRED"
        elif self.occupant is None:
            occupant_type = 'unoccupied'
        else:
            occupant_type = self.occupant.unit_type

        return occupant_type

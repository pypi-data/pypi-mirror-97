# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:23
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :abstractgameunit.py

import random
from abc import ABCMeta, abstractmethod
from gameutils import bold
from gameuniterror import HealthMeterException

class AbstractGameUnit(metaclass=ABCMeta):
    def __init__(self, name=''):
        self.name = name
        self.unit_type = None
        self.health_meter = None
        self.max_hp = None

    @abstractmethod
    def info(self):
        pass

    def attack(self, opponent):
        hurt_one = random.choice([self, opponent])
        hurt_one.health_meter = hurt_one.health_meter - random.randint(10, 15)
        print('ATTACK!', end='')

    def heal(self, heal_by=2, full_healing=True):
        """Heal the unit replenishing all the hit points"""
        if self.health_meter == self.max_hp:
            return
        if full_healing:
            self.health_meter = self.max_hp
        else:
            self.health_meter += heal_by
        # -------------------------------------------------------------------
        # raise a custom exception. Refer to chapter on exception handling
        # -------------------------------------------------------------------
        if self.health_meter > self.max_hp:
            raise HealthMeterException("health_meter > max_hp!")

        print(bold(f"You are HEALED!"), end=" ")
        self.show_health(bold_str=True, end='\r\n')

    def reset_health_meter(self):
        pass

    def show_health(self, bold_str=False, end=''):
        health_show = f"Health: {self.name}: {self.health_meter} "
        if bold_str:
            health_show = bold(health_show)
        print(health_show, end=end)
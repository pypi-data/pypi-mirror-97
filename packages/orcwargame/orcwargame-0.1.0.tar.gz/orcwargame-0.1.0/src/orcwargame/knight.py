# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:26
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :knight.py

from abstractgameunit import AbstractGameUnit
from gameutils import bold

class Knight(AbstractGameUnit):
    def __init__(self, name='Sir Foo'):
        AbstractGameUnit.__init__(self)
        self.name = name
        self.health_meter = 40
        self.max_hp = 40
        self.unit_type = 'friend'

    def info(self):
        pass

    def acquire_hut(self, hut):
        """Fight the combat (command line) to acquire the hut"""
        print(bold(f"Entering hut {hut.number},"), end=' ')
        is_enemy = (isinstance(hut.occupant, AbstractGameUnit)
                    and hut.occupant.unit_type == 'enemy')
        continue_attack = 'y'
        if is_enemy:
            print(bold("Enemy sighted!"))
            self.show_health(bold_str=True)
            hut.occupant.show_health(bold_str=True)
            while continue_attack:
                continue_attack = input("......continue attack?(y/n):")
                if continue_attack == 'n':
                    self.run_away()
                    break

                self.attack(hut.occupant)

                if hut.occupant.health_meter <= 0:
                    print("")
                    hut.acquire(self)
                    break
                if self.health_meter <= 0:
                    print("")
                    break

                self.show_health()
                hut.occupant.show_health()
        else:
            if hut.get_occupant_type() == 'unoccupied':
                print(bold('Hut is unoccupied'))
            else:
                print(bold("Friend sighted!"))
            hut.acquire(self)
            self.heal()

    def run_away(self):
        print(bold("RUNNING AWAY"))

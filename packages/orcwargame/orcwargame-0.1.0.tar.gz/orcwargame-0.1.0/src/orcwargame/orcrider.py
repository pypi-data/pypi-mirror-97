# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:27
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :orcrider.py

from abstractgameunit import AbstractGameUnit


class OrcRider(AbstractGameUnit):
    def __init__(self, name):
        AbstractGameUnit.__init__(self)
        self.unit_type = 'enemy'
        self.name = name
        self.health_meter = 30
        self.max_hp = 30

    def info(self):
        pass

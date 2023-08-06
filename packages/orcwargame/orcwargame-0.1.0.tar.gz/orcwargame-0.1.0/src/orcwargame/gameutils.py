# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:18
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :gameutils.py

def bold(string: str) -> str:
    """Print a string in 'bold' font"""
    return f"\033[1m{string}\033[0m"

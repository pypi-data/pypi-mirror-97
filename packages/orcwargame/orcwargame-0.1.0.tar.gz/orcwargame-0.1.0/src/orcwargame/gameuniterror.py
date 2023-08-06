# -*- coding: utf-8 -*-
# @Time    :2021/3/8 10:48
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :gameuniterror.py.py

class GameUnitError(Exception):
    """Custom exception class for the 'AbstractGameUnit' and its subclasses"""

    def __init__(self, message=''):
        super().__init__(message)
        self.padding = '~' * 50 + '\r\n'
        self.error_message = "Unspecified Error!"


class HealthMeterException(GameUnitError):
    """Custom exception to report Health Meter related problems"""

    def __init__(self, message=''):
        super(HealthMeterException, self).__init__(message)
        self.error_message = (self.padding +
                              "ERROR: Health Meter Problem" +
                              '\r\n' + self.padding)


class HutError(Exception):
    def __init__(self, code):
        self.error_message = ''
        self.error_dict = {
            000: "E000: Unspecified Error code",
            101: "E101: Out of range: Number > 5",
            102: "E102: Out of range, Negative number",
            103: "E103: Not a number!",
            104: "E104: You have already acquired this hut. Try again."
                 "<INFO: You can NOT get healed in already acquired hut.>",
        }
        try:
            self.error_message = self.error_dict[code]
        except KeyError:
            self.error_message = self.error_dict[000]
        print("Error message: ",self.error_message)

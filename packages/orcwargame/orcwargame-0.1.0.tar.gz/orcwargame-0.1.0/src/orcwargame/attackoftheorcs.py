# -*- coding: utf-8 -*-
# @Time    :2021/3/8 14:28
# @Author  :Ma Liang
# @Email   :mal818@126.com
# @File    :attackoftheorcs.py

import random
from hut import Hut
from knight import Knight
from orcrider import OrcRider
from gameutils import bold
from typing import List
from gameuniterror import HutError


class AttackOfTheOrcs:
    def __init__(self):
        self.huts: List[Hut] = []
        self.player = None

    def get_occupants(self):
        current_occupants = []
        for hut in self.huts:
            current_occupants.append(hut.get_occupant_type())
        return str(current_occupants)

    def show_game_mission(self):
        print(bold('Mission:'))
        print('\t1. Fight with the enemy.')
        print('\t2. Bring all the huts in the village under your control.')
        print('-' * 72)
        print()

    def _process_user_choice(self) -> int:
        """Process the user input for choice of hut to enter"""
        verifying_choice = True
        idx = 0
        print(f'Current occupants:{self.get_occupants()}')
        while verifying_choice:
            try:
                user_choice = input('Choose a hut number to enter (1-5): ')
                try:
                    idx = int(user_choice)
                except ValueError:
                    raise HutError(103)
                try:
                    if self.huts[idx - 1].isacquired:
                        raise HutError(104)
                except IndexError:
                    raise HutError(101)
                else:
                    if idx not in range(1, 6):
                        raise HutError(102)
            except HutError:
                continue
            else:
                verifying_choice = False

        return int(idx)

    def _occupy_huts(self):
        """Randomly occupy the huts with one of: friend enemy or 'None'"""
        for i in range(5):
            choice_lst = ['enemy', 'friend', None]
            computer_choice = random.choice(choice_lst)
            if computer_choice == 'enemy':
                name = 'enemy-' + str(i + 1)
                self.huts.append(Hut(i + 1, OrcRider(name)))
            elif computer_choice == 'friend':
                name = 'knight-' + str(i + 1)
                self.huts.append(Hut(i + 1, Knight(name)))
            else:
                self.huts.append(Hut(i + 1, computer_choice))

    def play(self):
        self.player = Knight()
        self._occupy_huts()
        acquired_hut_counter = 0

        self.show_game_mission()
        self.player.show_health(bold_str=True, end='\r\n')

        while acquired_hut_counter < 5:
            idx = self._process_user_choice()
            self.player.acquire_hut(self.huts[idx - 1])
            if self.player.health_meter <= 0:
                print(bold("YOU LOSE :( Better luck next time"))
                break

            if self.huts[idx - 1].isacquired:
                acquired_hut_counter += 1

        if acquired_hut_counter == 5:
            print(bold("Congratulations! YOU WIN!!!"))


if __name__ == '__main__':
    game = AttackOfTheOrcs()
    game.play()

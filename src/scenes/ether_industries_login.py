# -*- coding: utf-8 -*-
"""
This Scene will show login for an Ether Industries computer.
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#  Copyright (C) © 2020 Khaïs COLIN <logistic-bot@protonmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------
import curses
import logging
from time import sleep

from src.core.scene import FullScreenScene


class EtherIndustriesLogin(FullScreenScene):
    """
    Ask an user to login to an Ether Industries computer
    """

    def start(self) -> None:
        logger = logging.getLogger(__name__)
        """
        Show this scene
        """
        curses.flushinp()
        logger.debug("Start Logging in")

        login_prompt = "Login: "
        password_prompt = "Password: "

        expected_password = self.state.data["user"]["password"]
        logger.debug("Excepted password : "+excepted_password)
        expected_username = self.state.data["user"]["username"]
        logger.debug("Excepted username : "+excepted_username)
        logged_in = False
        logger.debug("Logged in : "+logged_in)
        while not logged_in:
            self.clear()
            self.addinto(1, 1, "Ether Industry EtherOS v6.2.4 (black-hole-01) (tty1)")

            username = self.prompt(1, 3, login_prompt)
            password = self.prompt(1, 4, password_prompt)

            sleep(0.2)

            if username == expected_username and password == expected_password:
                self.addinto(1, 5, f"Last login: {self.state.lastsave}")
                logged_in = True
                logger.debug("Logged in : "+logged_in)
            else:
                self.addinto(1, 5, "Login incorrect.")
                logger.debug("Login incorrect")
                sleep(1)

        self.get_key()

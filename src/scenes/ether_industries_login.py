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

from src.core.scene import Scene


class EtherIndustriesLogin(Scene):
    """
    Ask an user to login to an Ether Industries computer
    """
    def start(self) -> None:
        """
        Show this scene
        """
        login_prompt = "Login: "
        password_prompt = "Password: "

        self.clear()
        self.addinto(1, 1, "Ether Industry EtherOS v6.2.4")

        name = self.prompt(1, 3, login_prompt)
        password = self.prompt(1, 4, password_prompt)

        self.addinto(1, 5, f"'{name}'+'{password}'")
        self.get_key()

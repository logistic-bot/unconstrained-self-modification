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
    def start(self) -> None:
        LOGIN_PROMPT = "Login: "
        login_y = 3

        self.clear()
        self.addinto(1, 1, "Ether Industry EtherOS v6.2.4")

        text = self.prompt(login_y, 1, LOGIN_PROMPT)

        self.addinto(1, 5, text)
        self.get_key()

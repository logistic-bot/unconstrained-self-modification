"""
This file contains the GameState class, which is responsible for saving the current game state.
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
from src.core.state.save import Save


class GameState:
    """
    This class is responsible for saving the current game state.
    """

    def __init__(self) -> None:
        self.data = {}
        self.save = None

    def load_from_save(self, save: Save) -> None:
        """
        Load a saved game state into this object
        :param save: The Save object which has the saved game state
        """
        self.data = save.data
        self.save = save

    @property
    def lastsave(self) -> str:
        """
        Return a string describing the last time this state was saved. If it was not saved,
        return "Never".
        """
        if self.save is None:
            return "Never"
        else:
            return self.data["metadata"]["save_date"]
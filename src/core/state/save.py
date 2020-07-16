"""
This file contains tha Save class, which is responsible to save a GameState object to a file. To
get a Save object, please use a SaveManager object.
"""

import json
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
from pathlib import Path


class Save:
    """
    This class is responsible to save a GameState object to a file. To get a Save object,
    please use a SaveManager instance. It will ensure that it is saved in the right place.
    """

    def __init__(self, path: Path = None) -> None:
        self.path = path
        self.data = {}
        self.load()

    def load(self, path: Path = None) -> None:
        """
        Load a save file at a specified path into this save object.
        """
        if path is not None:
            self.path = path
        else:
            path = self.path

        with path.open("r") as f:
            self.data = json.load(f)

    def __repr__(self) -> str:
        return f"Save('{self.path}')"

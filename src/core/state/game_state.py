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

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

JSON = Any


class GameState:
    """
    This class is responsible for saving the current game state.
    """

    def __init__(self) -> None:
        self.data: JSON = {}

        logger.debug("Creating new empty GameState")

    def load(self, path: Path) -> None:
        """
        Load a save file at a specified path into this save object.
        """
        logger.info("Loading save file: '%s'", path)

        with path.open("r") as file:
            self.data = json.load(file)

        logger.info('New data: "%s"', self.data)

    @property
    def lastsave(self) -> str:
        """
        Return a string describing the last time this state was saved. If it was not saved,
        return "Never".
        """
        last_save = self.data["metadata"]["save_date"]
        assert isinstance(last_save, str)

        logger.debug("Lastsave: '%s'", last_save)
        return last_save

    def save(self, path: Path) -> None:
        """
        Save this game state to a given file, in JSON format.

        :param path: the path to the file.
        """
        logger.info("Saving state to file '%s'", path)
        logger.info('Current data: "%s"', self.data)

        path.touch(exist_ok=True)  # ensure that the file exists

        with path.open("w") as file:
            json.dump(self.data, file, indent=2, sort_keys=True)

        logger.info("Done saving state")

    def update(self, data: JSON) -> None:
        """
        Update the game state data with the provided data.
        See dict.update() for more details.

        :param data: The data that should be updated
        :return: None
        """
        self.data.update(data)

    def __str__(self) -> str:
        return self.data["name"]

    def __len__(self) -> int:
        return len(self.data["name"])

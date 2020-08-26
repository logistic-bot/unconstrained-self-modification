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
from typing import Any, cast, Optional

logger = logging.getLogger(__name__)

JSON = Any


class GameState:
    """
    This class is responsible for saving the current game state.

    It has two properties: data and filepath. data contains the actual JSON data
    loaded from the save file. filepath contains the path where the save is
    stored.

    At init time, filepath is set to None.

    See the documentation for load() and save() for information on how filepath
    behaves.
    """

    def __init__(self) -> None:
        self.data: JSON = {}
        self.filepath: Optional[Path] = None

        logger.debug("Creating new empty GameState")

    def load(self, path: Path) -> None:
        """
        Load a save file at a specified path into this save object. The internal
        path is then set to the given <path>.
        """
        self.filepath = path

        logger.info("Loading save file: '%s'", path)

        with path.open("r") as file:
            self.data = json.load(file)

        logger.info('New data: "%s"', self.data)

    @property
    def lastsave(self) -> str:
        """
        Return a string describing the last time this state was saved. If it was
        not saved, return "Never".
        """
        last_save = self.data["metadata"]["save_date"]
        assert isinstance(last_save, str)

        logger.debug("Lastsave: '%s'", last_save)
        return last_save

    def save(self, path: Optional[Path] = None) -> None:
        """
        Save this game state to a given file, in JSON format. Does not update
        the internal path.

        :param path: the path to the file.
        """
        if path is None:
            assert (
                self.filepath is not None
            ), "You need to provide load() or set the filepath manually at least once."
            path = self.filepath
            logger.info("Using last loaded filepath '%s'", path)
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
        return cast(str, self.data["name"])

    def __len__(self) -> int:
        return len(self.data["name"])

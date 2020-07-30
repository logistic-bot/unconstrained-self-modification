"""
This file contains the SaveManager class, which manages a group of Saves
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
import logging
from typing import List

from src import GAME_ROOT_DIR
from src.core.state.game_state import GameState

SAVEFILE_EXTENSION = ".json"

SAVE_DIRECTORY = GAME_ROOT_DIR / "saves"
SAVE_DIRECTORY.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)


class SaveManager:
    """
    This class manages a group of Saves.
    """

    def __init__(self) -> None:
        self.save_dir = SAVE_DIRECTORY
        logger.info("Creating new SaveManager with save dir '%s'", self.save_dir)

    @property
    def saves(self) -> List[GameState]:
        """
        Return an unordered (as in: in no particular order) list of all saves in self.save_dir
        """
        logger.info("Getting save list")

        saves = []
        for savefile_path in self.save_dir.iterdir():
            if savefile_path.suffix == SAVEFILE_EXTENSION:
                logger.info("Found save file at '%s", savefile_path)

                save = GameState()
                save.load(savefile_path)
                saves.append(save)
            else:
                logger.warning("Found non-savefile file at '%s'", savefile_path)

        logger.info("All saves: '%s'", saves)
        return saves

    def save_state(self, state: GameState) -> None:
        """
        Save a given state into a file. The filename is determined by the 'name' attribute of the
        state data.

        :param state: The state to save
        :return: None
        """


        path = self.save_dir / f"{state.data['name']}.json"

        logger.info("saving state of GameState '%s' at file '%s'", state, path)

        # TODO: See if this is still needed, maybe replace by state.save(path)
        state_duplicate = GameState()
        state_duplicate.data = state.data
        state_duplicate.save(path)

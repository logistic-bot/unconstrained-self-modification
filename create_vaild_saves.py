"""
When executed, this file will create a configurable number of valid save files, for testing
purposes. The username and password are the same as the save file's name.
"""

# TODO: Update copyright

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

from random import randint

from src.core.state.game_state import GameState
from src.core.state.save_manager import SaveManager

NUM_SAVES = 5

manager = SaveManager()

for number in range(NUM_SAVES):
    state = GameState()
    save_creation = "Created by create_valid_saves.py"
    rnd = randint(0, 10000)
    rnd = str(rnd)

    state.data["name"] = str(rnd)
    state.data["metadata"]["save_creation"] = str(save_creation)
    state.data["metadata"]["save_date"] = str(save_creation)
    state.data["name"] = rnd
    state.data["user"]["password"] = rnd
    state.data["user"]["username"] = rnd

    manager.save_state(state)

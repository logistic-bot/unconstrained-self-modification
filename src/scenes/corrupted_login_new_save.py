"""This file contains the CorruptedLoginNewSave FullScreenScene. It is called if no save is
found, and a new save should be created. """

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
import datetime
import logging
from time import sleep
from typing import Optional

from src.animations import ether_industries_password_corrupt
from src.core.scene import FullScreenScene, Scene
from src.core.state.save_manager import SaveManager
from src.scenes.start_computer import StartComputer

logger = logging.getLogger(__name__)


class CorruptedLoginNewSave(FullScreenScene):
    """
    This FullScreenScene will tell the user that the login file is corrupt, and walk it through
    the new superuser creation process. It will then create a new save.
    """

    def start(self) -> Optional[Scene]:  # pylint: disable=R1711
        """
        See above
        """
        start_computer_scene = StartComputer(self.renderer, self.state)
        start_computer_scene.start()

        self.clear()
        curses.flushinp()

        password_corrupt_animation = ether_industries_password_corrupt.create_animation(
            self.renderer
        )
        password_corrupt_animation.start()
        logger.debug("Start FullScreenScene: CorruptedLoginNewSave")

        username_prompt = "New superuser name: "
        password_prompt = "New superuser password: "
        password_confirm = "Confirm new superuser password: "

        logged_in = False
        logger.debug("Starting login process")
        username = ""
        password = ""
        while not logged_in:

            username = self.prompt(1, 5, username_prompt)
            password = self.prompt(1, 6, password_prompt)
            confirmed_password = self.prompt(1, 7, password_confirm)

            if password == confirmed_password:
                # noinspection PyUnusedLocal
                logged_in = True
                logger.debug(
                    "Logged in! User: '%s', Password: '%s'", username, password
                )
            elif password == "":
                self.addinto(1, 9, "Password is empty.")
                logger.info("Password is empty.")
            elif username == " ":
                self.addinto(1, 9, "Username is empty.")
                logger.info("Username is empty.")
            else:
                self.addinto(1, 9, "Passwords do not match.")
                logger.info("Passwords do not match.")

            sleep(1)

        far_away_future = datetime.timedelta(days=365 * 126)
        save_creation = datetime.date.today() + far_away_future

        self.state.data.update()
        self.state.data["metadata"]["save_creation"] = str(save_creation)
        self.state.data["metadata"]["save_date"] = str(save_creation)
        self.state.data["name"] = username
        self.state.data["user"]["password"] = password
        self.state.data["user"]["username"] = username

        logger.debug("State data: '%s'", self.state.data)

        self.addinto(1, 9, "[ether-login c198762] Creating new user database...")

        save_manager = SaveManager()
        save_manager.save_state(self.state)
        logger.debug("State Saved!")

        self.addinto(1, 10, "[ether-login c198762] Done.")
        self.addinto(1, 12, "Welcome! Type 'help' for help!")

        self.get_key()

        # TODO: This should return the scene with the command line
        return None

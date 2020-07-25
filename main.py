#!/usr/bin/env python

"""
Run this file to start the game
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
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

from src.core.engine import Engine

logger = logging.getLogger(__name__)


def main() -> None:
    """
    main
    """
    engine = Engine()
    engine.start()
    logger.info("This should be the last log line. If it is not, please contact the developers")


if __name__ == "__main__":
    logger.info("Starting game")
    main()

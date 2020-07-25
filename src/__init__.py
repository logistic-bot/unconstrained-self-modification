"""
Define Game-wide Constants
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
from pathlib import Path

GAME_ROOT_DIR = Path(__file__).parent.parent.absolute().resolve()

log_file_dir = GAME_ROOT_DIR / "log"
log_file = log_file_dir / "unconstrained_self_modification.log"

log_file_dir.mkdir(exist_ok=True)
log_file.touch(exist_ok=True)

logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(pathname)s:%(name)s:%(funcName)s:%(lineno)d:%(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Logger configured")
logger.debug("game root: %s", GAME_ROOT_DIR)
logger.debug("log file: %s", log_file)

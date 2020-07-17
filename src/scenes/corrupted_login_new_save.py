"""
This file contains the CorruptedLoginNewSave FullScreenScene. It is called if no save is found, and a new
save should be created.
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

from src.core.scene import FullScreenScene


class CorruptedLoginNewSave(FullScreenScene):
    """
    This FullScreenScene will tell the user that the login file is corrupt, and walk it through the new
    superuser creation process. It will then create a new save.
    """
    def start(self):
        """
        See above
        """
        pass

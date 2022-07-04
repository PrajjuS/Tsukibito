#
#  Copyright (c) 2022 PrajjuS.
#
#  This file is part of Tsukibito
#  (see https://github.com/PrajjuS/Tsukibito).
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from pathlib import Path

from Tsukibito import LOGGER

ALL_MODULES = [
    f.stem
    for f in Path(__file__).parents[0].iterdir()
    if f.is_file() and f.name.endswith(".py") and not f.name.startswith("__init__.py")
]

LOGGER.info(f"Modules to load: {', '.join(ALL_MODULES)}")

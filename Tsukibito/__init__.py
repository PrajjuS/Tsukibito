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

import asyncio
import time
from configparser import ConfigParser
from pathlib import Path

from NoobStuffs.liblogging import setup_logging
from telegram.ext import ApplicationBuilder

__version__ = "1.0.0"

LOGGER = setup_logging(name="Tsukibito", verbose=True)

parser = ConfigParser()
parser.read(f"{Path(__file__).parents[1]}/config.ini")

try:
    config = parser["tsukibito"]
except KeyError:
    LOGGER.error(
        "Please create config.ini and fill all the vars. Missing file: config.ini / Missing section: [tsukibito]",
    )
    exit(0)


def check_vars(class_name):
    all_vars = [
        var
        for var in dir(class_name)
        if not callable(getattr(class_name, var)) and not var.startswith("__")
    ]
    for var in all_vars:
        if getattr(class_name, var) is None or getattr(class_name, var) == "":
            LOGGER.error(f"Please fill all the vars in config.ini. Missing var: {var}")
            exit(0)


class Config:
    VERSION: int = __version__
    BOT_TOKEN: str = config.get("BOT_TOKEN")
    OWNER_ID: int = config.getint("OWNER_ID")
    GH_TOKEN: str = config.get("GH_TOKEN")
    USERNAME: str = config.get("USERNAME")
    EMAIL: str = config.get("EMAIL")
    ROM_BUILDERS_REPO: str = config.get("ROM_BUILDERS_REPO")


check_vars(Config())
dir_name = Path(__file__).parents[0].parts[-1]
StartTime = time.time()
loop = asyncio.get_event_loop()
application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

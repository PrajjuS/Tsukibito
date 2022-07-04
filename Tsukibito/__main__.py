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

from importlib import import_module
from pathlib import Path
from typing import Optional

from NoobStuffs.libformatter import HTML
from telegram import Update
from telegram.ext import ContextTypes

from Tsukibito import LOGGER, Config, application, loop
from Tsukibito.helpers.decorators import HELP_DICT, botcmd
from Tsukibito.modules import ALL_MODULES

for module in ALL_MODULES:
    import_module(f"{Path(__file__).parents[0].parts[-1]}.modules.{module}")


@botcmd(command="start", command_help="Start the bot")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        text=f"Konichiwa! I'm Tsukibito and I'm alive\nVersion {Config.VERSION}",
    )


@botcmd(command="help", command_help="Get bot help")
async def bot_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_TEXT = f"{HTML.bold('Available commands:')}\n"
    for command, command_help in get_help().items():
        HELP_TEXT += f"/{command} - {command_help}\n"
    await update.effective_message.reply_html(
        text=HELP_TEXT,
    )


# Do some magic: Rearranges the help dict in the way which I want
def get_help(is_tuple: Optional[bool] = False):
    NEW_DICT = dict(reversed(HELP_DICT.items()))
    NEW_DICT["help"] = NEW_DICT.pop("help")
    NEW_DICT["start"] = NEW_DICT.pop("start")
    FINAL_DICT = dict(reversed(NEW_DICT.items()))
    if is_tuple:
        return tuple((k, v) for k, v in FINAL_DICT.items())
    else:
        return FINAL_DICT


def main():
    loop.run_until_complete(
        application.bot.set_my_commands(get_help(is_tuple=True)),
    )
    if Path(".restartmsg").is_file():
        with open(".restartmsg") as remsg:
            chat_id, msg_id = map(int, remsg)
        loop.run_until_complete(
            application.bot.edit_message_text(
                text="Restarted bot successfully.",
                chat_id=chat_id,
                message_id=msg_id,
            ),
        )
        Path(".restartmsg").unlink(missing_ok=True)
    LOGGER.info(f"Successfully loaded modules: {', '.join(ALL_MODULES)}")
    LOGGER.info("Using long polling.")
    application.run_polling()


if __name__ == "__main__":
    main()
    LOGGER.info("Stopping long polling.")

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

from datetime import timedelta
from os import execl, getpid, kill
from signal import SIGTERM
from sys import executable
from time import time

from NoobStuffs.libformatter import HTML
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from Tsukibito import LOGGER, StartTime, application, dir_name
from Tsukibito.helpers import CustomFilters, botcmd, parse_command


@botcmd(
    command="ping",
    command_help="Check how long it takes to ping the bot",
    filters=CustomFilters.OWNER,
)
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time()
    message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Pinging...')}",
    )
    end_time = time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3))
    uptime = str(timedelta(seconds=round(time() - StartTime)))
    PING_TEXT = f"PONG!\n"
    PING_TEXT += f"{HTML.bold('Time Taken:')} {HTML.mono(f'{telegram_ping} ms')}\n"
    PING_TEXT += f"{HTML.bold('Uptime:')} {HTML.mono(uptime)}"
    await message.edit_text(text=PING_TEXT, parse_mode=ParseMode.HTML)


@botcmd(
    command="logs",
    command_help="Get a log file of the bot [Flag: d|debug(Optional)]",
    filters=CustomFilters.OWNER,
)
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    owo = parse_command(update.effective_message.text)
    if len(owo) != 0:
        if "d" in list(owo.keys()) or "debug" in list(owo.keys()):
            with open(f"{LOGGER.name}-DEBUG.log", "rb") as log:
                await update.effective_message.reply_document(
                    document=log,
                    filename=f"{LOGGER.name}-DEBUG.log",
                )
    else:
        with open(f"{LOGGER.name}.log", "rb") as log:
            await update.effective_message.reply_document(
                document=log,
                filename=f"{LOGGER.name}.log",
            )


@botcmd(command="restart", command_help="Restart the bot", filters=CustomFilters.OWNER)
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restart_message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Restarting bot...')}",
    )
    LOGGER.info("Restarting bot...")
    with open(".restartmsg", "w") as remsg:
        remsg.truncate(0)
        remsg.write(f"{restart_message.chat_id}\n{restart_message.message_id}")
    execl(executable, executable, "-m", dir_name)


@botcmd(
    command="shutdown",
    command_help="Shutdown the bot",
    filters=CustomFilters.OWNER,
)
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Shutting down bot...')}",
    )
    LOGGER.info("Shutting down bot...")
    kill(getpid(), SIGTERM)
    await application.bot.edit_message_text(
        text="Shut down bot successfully.",
        chat_id=message.chat_id,
        message_id=message.message_id,
    )

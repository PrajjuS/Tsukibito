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

import os
import subprocess

from NoobStuffs.libformatter import HTML
from telegram import Update
from telegram.constants import MessageLimit, ParseMode
from telegram.ext import ContextTypes

from Tsukibito.helpers import CustomFilters, botcmd


@botcmd(
    command="shell",
    command_help="To execute a command in the bot's environment",
    filters=CustomFilters.OWNER,
)
async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split(" ", 1)
    if len(command) == 1:
        return await update.effective_message.reply_html(
            text="Plox give any command to execute.",
        )
    command = command[1]
    message = await update.effective_message.reply_html(
        text=f"{HTML.bold('Executing:')} {HTML.mono(f'{command}...')}",
    )
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    return_code = process.wait()
    stdout, stderr = process.communicate()
    if stdout:
        output = stdout.decode()
    if stderr:
        output = stderr.decode()
    TEXT = f"{HTML.bold('Command:')} {HTML.mono(f'{command}')}\n"
    TEXT += f"{HTML.bold('Return Code:')} {HTML.mono(f'{return_code}')}\n\n"
    if len(output) + len(TEXT) < MessageLimit.TEXT_LENGTH:
        TEXT += f"{HTML.bold('Output:')}\n"
        TEXT += f"{HTML.mono(f'{output}')}"
        await message.edit_text(text=TEXT, parse_mode=ParseMode.HTML)
    else:
        with open("output.txt", "w") as out:
            out.write(output)
        TEXT += f"{HTML.bold('Output:')} {HTML.mono('Sent as document')}"
        await message.delete()
        with open("output.txt", "rb") as out:
            await update.effective_message.reply_document(
                document=out,
                filename="output.txt",
                caption=TEXT,
                parse_mode=ParseMode.HTML,
            )
        os.remove("output.txt")

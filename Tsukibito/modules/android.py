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

from NoobStuffs.libandroid import get_all_magisks
from NoobStuffs.libformatter import HTML
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from Tsukibito.helpers import botcmd


@botcmd(command="magisk", command_help="Get latest magisk releases")
async def magisk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.effective_message.reply_html(
        text=HTML.mono("Pulling latest magisk releases..."),
    )
    magisks = get_all_magisks()
    TEXT = f"{HTML.bold('Latest Magisk Releases')}\n"
    TEXT += f"Stable v{magisks['Stable']['version']}: {HTML.hyperlink('Changelog', magisks['Stable']['changelog'])} | {HTML.hyperlink('Download', magisks['Stable']['download'])}\n"
    TEXT += f"Beta v{magisks['Beta']['version']}: {HTML.hyperlink('Changelog', magisks['Beta']['changelog'])} | {HTML.hyperlink('Download', magisks['Beta']['download'])}\n"
    TEXT += f"Canary v{magisks['Canary']['version']}: {HTML.hyperlink('Changelog', magisks['Canary']['changelog'])} | {HTML.hyperlink('Download', magisks['Canary']['download'])}\n"
    await message.edit_text(
        text=TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

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

from NoobStuffs.libdatetime import dtnow
from NoobStuffs.libformatter import HTML
from NoobStuffs.libgithub import GithubHelper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from Tsukibito import Config
from Tsukibito.helpers import CustomFilters, botcmd, parse_command

github = GithubHelper(
    gh_token=Config.GH_TOKEN,
    username=Config.GH_USERNAME,
    email=Config.GH_EMAIL,
)


@botcmd(
    command="trigger",
    command_help="Trigger rom build in ROM-builders repository [Flags: b|branch, m|message(Optional)]",
    filters=CustomFilters.OWNER,
)
async def trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Triggerring build...')}",
    )
    owo = parse_command(update.effective_message.text)
    branch = next((val for key, val in owo.items() if key in ["b", "branch"]), None)
    c_message = next(
        (val for key, val in owo.items() if key in ["m", "message"]),
        "Trigger build",
    )
    commit_message = f"{branch}: {c_message}"
    if not branch:
        return await message.edit_text("Please provide branch name.")
    output = github.commit_changes(
        repo=Config.ROM_BUILDERS_REPO,
        content="build_rom.sh",
        message=commit_message,
        branch=branch,
    )
    commit_url = (
        f"https://github.com/{Config.ROM_BUILDERS_REPO}/commit/{output['commit'].sha}"
    )
    TEXT = "#BUILD_TRIGGER\n"
    TEXT += f"{HTML.bold('Build Triggered Successfully!')}\n"
    TEXT += f"{HTML.bold('Branch:')} {HTML.mono(branch)}\n"
    TEXT += f"{HTML.bold('Commit Message:')} {HTML.mono(commit_message)}\n"
    TEXT += f"{HTML.bold('Time:')} {HTML.mono(f'''{dtnow()['time']} IST''')}"
    keyboard = [
        [
            InlineKeyboardButton(text="Commit URL", url=commit_url),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.edit_text(
        text=TEXT,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )

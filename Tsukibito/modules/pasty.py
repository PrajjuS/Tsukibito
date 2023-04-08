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

import re
from pathlib import Path

from NoobStuffs.libdatetime import fromtimestamp
from NoobStuffs.libformatter import HTML
from NoobStuffs.libpasty import get_content, paste_content
from telegram import Update
from telegram.constants import MessageLimit, ParseMode
from telegram.ext import ContextTypes

from Tsukibito import LOGGER
from Tsukibito.helpers import botcmd

PASTY_REGEX = re.compile(r"(https://)?(pasty\.lus\.pm/)?([A-Za-z0-9]\w+)")


@botcmd(command="paste", command_help="Paste content to pasty")
async def paste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_to = update.effective_message.reply_to_message
    args = context.args
    message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Processing content...')}",
    )
    if len(args) >= 1:
        content = " ".join(args)
    elif reply_to and reply_to.text:
        content = reply_to.text
    elif reply_to and reply_to.document:
        doc = await context.bot.get_file(reply_to.document.file_id)
        await doc.download(custom_path="contenttopaste.txt")
        with open("contenttopaste.txt") as cf:
            content = cf.read()
    else:
        return await message.edit_text(
            text="Give anything to paste or reply to any document.",
        )
    try:
        LOGGER.info("Pasting to pasty...")
        pastee = paste_content(content)
    except Exception as e:
        LOGGER.error(e)
        return await message.edit_text(text="Failed to paste to pasty.lus.pm")
    message = await message.edit_text(
        text=f"{HTML.mono('Pasting content to pasty...')}",
        parse_mode=ParseMode.HTML,
    )
    TEXT = f"{HTML.bold('Pasted content to pasty successfully.')}\n"
    TEXT += f"{HTML.bold('URL:')} {HTML.hyperlink('Here', pastee['url'])}\n"
    TEXT += f"{HTML.bold('Raw:')} {HTML.hyperlink('Here', pastee['raw'])}\n"
    TEXT += f"{HTML.bold('Paste ID:')} {HTML.mono(pastee['url'].split('/')[-1])}"
    await message.edit_text(
        text=TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    Path("contenttopaste.txt").unlink(missing_ok=True)


@botcmd(command="getpaste", command_help="Get content from pasty")
async def getpaste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.effective_message.reply_to_message
    args = context.args
    if not len(args) == 1:
        return await update.effective_message.reply_html(
            "Please give any pasty URL or ID.",
        )
    message = await update.effective_message.reply_html(
        text=f"{HTML.mono('Getting content from pasty...')}",
    )
    content_id = re.match(PASTY_REGEX, context.args[0]).group(3)
    try:
        LOGGER.info("Getting content from pasty...")
        content = get_content(content_id)
    except Exception as e:
        LOGGER.error(e)
        return await message.edit_text(text="Failed to get content from pasty.lus.pm")
    TEXT = f"{HTML.bold('Got content from pasty successfully.')}\n"
    TEXT += f"{HTML.bold('URL:')} {HTML.hyperlink('Here', content['url'])}\n"
    TEXT += f"{HTML.bold('Created:')} {HTML.mono(f'''{fromtimestamp(content['created'], None)['date']}''')}\n"
    if len(content["content"]) < MessageLimit.MAX_TEXT_LENGTH:
        TEXT += f"{HTML.bold('Content:')} {HTML.mono(content['content'])}"
        await message.edit_text(
            text=TEXT,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    else:
        TEXT += f"{HTML.bold('Content:')} {HTML.mono('Sent as file.')}"
        with open("content.txt", "w+") as cf:
            cf.write(content["content"])
        await message.delete()
        await update.effective_message.reply_document(
            document=open("content.txt", "rb"),
            filename="content.txt",
            caption=TEXT,
            reply_to_message_id=update.effective_message.message_id,
            parse_mode=ParseMode.HTML,
        )
        Path("content.txt").unlink(missing_ok=True)

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

# Man this was pain
# Reference: https://gitlab.com/Justasic/shadowhawk/-/blob/master/shadowhawk/utils/Command.py#L14
COMMAND_REGEX = re.compile(
    r'\s+--?(?P<flag>\w+)(?:\s*(?:=\s*)?(?:(?P<arg>\w+[\-\w]+)|"(?P<string>(?:(?!")\n*?.\n*?)*)"))?',
)


def parse_command(message: str):
    owo = {}
    for match in COMMAND_REGEX.finditer(message):
        flag = match.group("flag")
        arg = match.group("arg")
        string = match.group("string")
        if string:
            owo[flag] = string
        else:
            owo[flag] = arg
    return owo

#!/usr/bin/env python3

from sprun import spr

commands = []
commands.append(["echo", " "])
commands.append(["echo   "])
commands.append(["echo"])
result = spr.run(commands, spr.Proceed.ASK, spr.Silent.OK)
assert(result.commands_error == [["echo   "]])

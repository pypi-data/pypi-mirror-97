import sys

from unittest import TestCase, runner
from sprun import spr

class TestExecution(TestCase):
    def test_all_pass(self):
        commands = []
        commands.append(["echo", " "])
        commands.append(["echo"])
        result = spr.run(commands, spr.Proceed.CONTINUE)
        self.assertTrue(len(result.commands_ok) == 2)
        self.assertTrue(result.success())
        self.assertFalse(result.failure())

    def test_second_fails_and_continues(self):
        commands = []
        commands.append(["echo", " "])
        commands.append(["echo  "])
        commands.append(["echo"])
        result = spr.run(commands, spr.Proceed.CONTINUE)
        self.assertFalse(result.success())
        self.assertTrue(result.failure())
        self.assertTrue(len(result.commands_ok) == 2)
        self.assertTrue(len(result.commands_error) == 1)

    def test_second_fails_and_break(self):
        commands = []
        commands.append(["echo", " "])
        commands.append(["echo   "])
        commands.append(["echo"])
        result = spr.run(commands, spr.Proceed.STOP, spr.Silent.ALL)
        self.assertFalse(result.success())
        self.assertTrue(result.failure())
        self.assertTrue(len(result.commands_ok) == 1)
        self.assertTrue(len(result.commands_error) == 1)

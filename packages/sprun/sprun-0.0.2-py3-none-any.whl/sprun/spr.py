"""
    An opinionated subprocess execution module for some special use cases

"""
import subprocess
import sys
from enum import Enum
from typing import List

Command = List[str]
CommandList = List[Command]


class Proceed(Enum):
    """ Continuation strategy for failing commands in run_commands call
    """
    CONTINUE = 1
    STOP = 2
    ASK = 3


class Silent(Enum):
    """ Continuation strategy for failing commands in run_commands call
    """
    NONE = 0
    ALL = 1
    OK = 2
    FAILURE = 3


class Result():
    """ Carrier for returning the result of the run calls
    """

    def __init__(self) -> None:
        self.commands_ok: CommandList = []
        self.commands_error: CommandList = []

    def success(self) -> bool:
        """ returns True if no command was reported returning an error
        """
        return not self.commands_error

    def failure(self) -> bool:
        """ returns True if some command was reported returning an error
        """
        return self.commands_error


def report_command(prefix: str, command: Command, *args, **kwargs) -> None:
    """ Use print to write out a command
        The command will simply be joined by space
        All other arguments will be forwarded to print
    """
    print(prefix, " ".join(command), args, kwargs)


def run(commands: CommandList, on_error: Proceed,
        silent: Silent = Silent.NONE):
    """ Run given commands.

        commands is a list of subprocess commands
        on_error must be a Proceed value

        If a command fails, the given Proceeds strategy is a applied

        Silent sets up the report strategy.

        Retruns a Result containing the successful and failed Command calls
    """
    silent_error = silent in [Silent.ALL, Silent.FAILURE]
    silent_ok = silent in [Silent.ALL, Silent.OK]

    def report_success(cmd: Command) -> None:
        report_command("OK:", cmd, file=sys.stdout)

    def report_error(cmd: Command) -> None:
        report_command("FAIL:", cmd, file=sys.stderr)

    def resume():
        return input("Command failed, continue with execution? (y/n): ") == "y"

    result = Result()
    for cmd in commands:
        call_rc = 1
        try:
            call_rc = subprocess.call(cmd)
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        if call_rc == 0:
            if not silent_ok:
                report_success(cmd)
            result.commands_ok.append(cmd)
        else:
            if not silent_error:
                report_error(cmd)
            result.commands_error.append(cmd)
            if on_error == Proceed.CONTINUE:
                continue
            if on_error == Proceed.STOP:
                return result
            if on_error == Proceed.ASK:
                if not resume():
                    return result

    return result

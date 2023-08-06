# Patch execution of multiple commands via subprocess

Sometimes you just want to run some commands via the python subprocess module,
and if any of those commands fails choose if you continue, stop or ask for continuation.
Finally, when command processing is done, a list of succeeded and failed commands is nice to have.

This is what `sprun`, subprocess run, is good for.






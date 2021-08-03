import os
import subprocess
import fileinput
import pwd


class CommandExecuter():
    def __init__(self, cmd: str):
        self._cmd = cmd

    def _execute(self):
        return subprocess.run(
            self._cmd, shell=True, capture_output=True, text=True)

    def get_result(self) -> str:
        if (res := self._execute()).returncode == 0:
            output = res.stdout
        else:
            output = res.stderr

        return output.removesuffix("\n")


a = CommandExecuter("l")
print(a.result)

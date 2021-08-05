import subprocess
from subprocess import CompletedProcess


class CommandExecuter():
    def __init__(self, cmd: str):
        self._cmd = cmd
        self._result = self._clean_result()
        self._is_stderr = False

    def _execute(self) -> CompletedProcess:
        return subprocess.run(
            self._cmd, shell=True, capture_output=True, text=True)

    def _clean_result(self) -> str:
        if (res := self._execute()).returncode == 0:
            output = res.stdout
        else:
            output = res.stderr
            self._is_stderr = True

        return output.removesuffix("\n")

    @property
    def result(self) -> str:
        return self._result

	def is_stderr(self) -> bool:
		return self._is_stderr

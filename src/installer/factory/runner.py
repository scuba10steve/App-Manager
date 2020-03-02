import sys
import os
from subprocess import run
from typing import List


class CommandRunner:
    def run(self, installer, install_dir: str = None):
        if sys.platform == 'win32':
            default_params = [installer, '/VERYSILENT']
            if install_dir:
                default_params.append('/DIR=' + install_dir)
                run(default_params, check=True)
            else:
                run(default_params, check=True)

    def run_cmd(self, cmd: str, args: List[str]):
        params = [cmd]
        params.extend(args)
        run(params, check=True)


class ChocoRunner(CommandRunner):
    def __init__(self):
        super()
        self.choco_root = "C:\\ProgramData\\chocolatey"

    def run(self, packages: List[str], install_dir: str = None):
        if sys.platform != "win32":
            raise Exception("Not running on a windows platform!!! Chocolatey doesn't currently run on Unix/Linux!!!")

        cmd = os.path.join(self.choco_root, "bin", "choco")

        super().run_cmd(cmd, packages)

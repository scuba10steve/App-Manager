import sys
from subprocess import run


class CommandRunner:
    def run(self, installer, install_dir=None):
        if sys.platform == 'win32':
            default_params = [installer, '/VERYSILENT']
            if install_dir:
                default_params.append('/DIR=' + install_dir)
                run(default_params)
            else:
                run(default_params)

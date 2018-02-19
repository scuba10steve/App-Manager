import os

class ApplicationInitializer:
    # def __init__(self):
    #     self.determine_os()

    def determine_os(self):
        osname = os.name
        if 'nt' in osname:
            self.os_type = 'Windows'
        elif 'unix' in osname:
            self.os_type = 'Unix/Linux'
    
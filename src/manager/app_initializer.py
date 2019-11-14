import os

class ApplicationInitializer:
    def __init__(self):
        osname = os.name
        if 'nt' in osname:
            self.os_type = 'Windows'
        elif 'unix' in osname:
            self.os_type = 'Unix/Linux'

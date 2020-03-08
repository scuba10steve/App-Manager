import platform

from src.repository.repo_initializer import AppRepositoryInitializer


class ApplicationInitializer:
    def __init__(self, repo: AppRepositoryInitializer):
        self.repo = repo
        self.os_type = platform.system()
        self.version = platform.version()
        if self.os_type == 'Windows':
            # self.os_version: str = os
            self.package_manager = 'choco'
        elif self.os_type == 'Linux':
            #TODO Find available package managers and determine defaults
            self.package_manager = 'apt'
        elif self.os_type == 'Darwin':
            self.package_manager = 'brew'

    def initialize(self):
        self.repo.store_sys_metadata(self.os_type, self.version, self.package_manager)

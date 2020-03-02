# external
import json
from json import JSONEncoder


class Application:
    def __init__(self, name: str, source_url: str, system: str, app_id: int = 0, installed: bool = False):
        self.name: str = name
        self.source_url: str = source_url
        self.system: str = system
        self.app_id: int = app_id
        self.installed: bool = installed
        self.has_installer: bool = False
        self.has_uninstaller: bool = False

    def get_name(self) -> str:
        return self.name

    def set_name(self, name) -> None:
        if name:
            self.name = name
        else:
            pass

    def set_source_url(self, source_url) -> None:
        if source_url:
            self.source_url = source_url
        else:
            pass

    def get_source_url(self) -> str:
        return self.source_url

    def set_system(self, system) -> None:
        if system:
            self.system = system
        else:
            pass

    def get_system(self) -> str:
        return self.system

    def set_app_id(self, app_id) -> None:
        if app_id:
            self.app_id = app_id
        else:
            pass

    def get_app_id(self) -> int:
        return self.app_id

    def set_installed(self, installed) -> None:
        self.installed = installed

    def is_installed(self) -> bool:
        return self.installed

    def get_has_installer(self) -> bool:
        return self.has_installer

    def get_has_uninstaller(self) -> bool:
        return self.has_uninstaller

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def serialize(self) -> dict:
        return self.__dict__


# pylint: disable=no-else-return
class ApplicationEncoder(JSONEncoder):
    def default(self, o) -> dict:
        if isinstance(o, Application):
            return o.__dict__
        else:
            raise TypeError("invalid type for encoding" + o)


class ApplicationDecoder:
    def decode(self, app):
        if not isinstance(app, str):
            raise TypeError('Invalid type for Application: {}'.format(app))

        jsobject = json.loads(app)

        return Application(jsobject['name'], jsobject['source_url'], jsobject['system'])

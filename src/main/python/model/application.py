# external
import json
from json import JSONEncoder


class Application:
    def __init__(self, name, source_url, system, app_id=0, installed=False):
        self.name = name
        self.source_url = source_url
        self.system = system
        self.app_id = app_id
        self.installed = installed
        self.has_installer = False
        self.has_uninstaller = False

    def get_name(self):
        return self.name

    def set_name(self, name):
        if name:
            self.name = name
        else:
            pass

    def set_source_url(self, source_url):
        if source_url:
            self.source_url = source_url
        else:
            pass

    def get_source_url(self):
        return self.source_url

    def set_system(self, system):
        if system:
            self.system = system
        else:
            pass

    def get_system(self):
        return self.system

    def set_app_id(self, app_id):
        if app_id:
            self.app_id = app_id
        else:
            pass

    def get_app_id(self):
        return self.app_id

    def set_installed(self, installed):
        self.installed = installed

    def is_installed(self):
        return self.installed

    def get_has_installer(self):
        return self.has_installer

    def get_has_uninstaller(self):
        return self.has_uninstaller

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def serialize(self):
        return self.__dict__


# pylint: disable=no-else-return
class ApplicationEncoder(JSONEncoder):
    def default(self, o):
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

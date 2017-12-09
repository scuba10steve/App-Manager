#external
from json import JSONEncoder
import json

class Application():
    def __init__(self, name, sourceUrl, system, app_id=0):
        self.name = name
        self.sourceUrl = sourceUrl
        self.system = system
        self.app_id = app_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        if name:
            self.name = name
        else:
            pass
    
    def set_sourceUrl(self, sourceUrl):
        if sourceUrl:
            self.sourceUrl = sourceUrl
        else:
            pass
        
    def get_sourceUrl(self):
        return self.sourceUrl

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

class ApplicationEncoder(JSONEncoder):
    def __init__(self):
        self.ensure_ascii=False
        super().__init__(ensure_ascii=False)

    def default(self, o):
        if type(o) == Application:
            return o.__dict__


class ApplicationDecoder():
    def __init__(self):
        self.foo = ""

    def decode(self, app):
        if not type(app) == str:
            raise TypeError('Invalid type for Application: {}'.format(app))

        jsobject = json.loads(app)
        
        return Application(jsobject['name'], jsobject['sourceUrl'], jsobject['system'])

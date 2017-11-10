from json import JSONEncoder

class Application():
    def __init__(self, name, source_url):
        self.name = name
        self.source_url = source_url

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

class ApplicationEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == Application:
            return o.__dict__

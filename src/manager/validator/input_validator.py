import re


class Validator:
    def __init__(self):
        self.pattern = r'https?:\/\/.+'

    def validate_url(self, url: str):
        if not isinstance(url, str):
            raise TypeError('Source Url must be string: {}'.format(url))
        if not re.match(self.pattern, url):
            raise Exception(
                'Source Url is in an invalid format: {}'.format(url))

    def validate_sys(self, system: str):
        if not isinstance(system, str):
            raise TypeError('system must be string: {}'.format(system))
        if not system:
            raise Exception('system must be set')

import re

URL_PATTERN = r'https?:\/\/.+'

def validate_url(sourceUrl):
    if not type(sourceUrl) == str:
        raise TypeError('Source Url must be string: {}'.format(sourceUrl))
    if not re.match(URL_PATTERN, sourceUrl):
        raise Exception('Source Url is in an invalid format: {}'.format(sourceUrl))

def validate_sys(system):
    if not type(system) == str:
        raise TypeError('system must be string: {}'.format(system))
    if not system:
        raise Exception('system must be set')

import re

URL_PATTERN = r"http://.+"

def validate(source_url):
    if not type(source_url) == str:
        raise TypeError('Source Url must be string: {}'.format(source_url))
    if not re.match(URL_PATTERN, source_url):
        raise Exception('Source Url is in an invalid format: {}'.format(source_url))
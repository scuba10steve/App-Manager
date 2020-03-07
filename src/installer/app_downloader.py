# external
import os
import re

import requests


class ApplicationDownloader:
    def __init__(self):
        self.installer_cache = "./working/cache/installers/"
        if not os.path.exists(self.installer_cache):
            os.makedirs(self.installer_cache)

    def download(self, url: str, app_name: str, extension: str) -> str:
        location = self.installer_cache + app_name

        if extension:
            location = location + '.' + extension

        if not os.path.isfile(location):
            response = requests.get(url, stream=True)

            if not extension:
                extension = re.findall("filename=(.+)", response.headers['content-disposition'])

            location = location + '.' + extension

            with open(location, 'wb') as handle:
                for block in response.iter_content(1024):
                    # print("chunk written..")
                    handle.write(block)

        return location

# external
import os
import re

import requests


class ApplicationDownloader:
    def __init__(self):
        self.installer_cache = "./working/cache/installers/"
        if not os.path.exists(self.installer_cache):
            os.makedirs(self.installer_cache)

    def download(self, url, app_name, extention):
        location = self.installer_cache + app_name

        if extention:
            location = location + '.' + extention

        if not os.path.isfile(location):
            response = requests.get(url, stream=True)

            if not extention:
                extention = re.findall("filename=(.+)", response.headers['content-disposition'])

            location = location + '.' + extention

            with open(location, 'wb') as handle:
                for block in response.iter_content(1024):
                    # print("chunk written..")
                    handle.write(block)

        return location

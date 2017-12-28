# external
import os
import requests


class ApplicationDownloader():
    def __init__(self):
        self.installer_cache = "./installers/"
        if not os.path.exists(self.installer_cache):
            os.makedirs(self.installer_cache)

    def download(self, url, app_name, extention='.exe'):
        location = self.installer_cache + app_name + extention
        if not os.path.isfile(location):
            response = requests.get(url, stream=True)

            with open(location, 'wb') as handle:
                for block in response.iter_content(1024):
                    # print("chunk written..")
                    handle.write(block)

        return location

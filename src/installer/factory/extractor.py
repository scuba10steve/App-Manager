import os
import zipfile
import libarchive


class Extractor:
    def __init__(self):
        self.working_dir = './working/cache/extracted'
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

    def extract(self, archive):
        print('extracting archive: ' + str(archive) + ' to working directory ' + self.working_dir)


class ZipExtractor(Extractor):
    def extract(self, archive):
        super().extract(archive)

        expanded = self.working_dir + os.path.basename(archive)
        zipped = zipfile.ZipFile(archive, mode='r')
        zipped.extractall(path=expanded)

        return expanded


class SevenZipExtractor(Extractor):
    def extract(self, archive):
        super().extract(archive)

        expanded = self.working_dir + '/' + os.path.basename(archive)
        if not os.path.exists(expanded):
            os.makedirs(expanded)

        with libarchive.file_reader(archive) as expanded_archive:
            for entry in expanded_archive:
                with open(expanded + '/' + str(entry), 'wb') as file:
                    for block in entry.get_blocks():
                        file.write(block)

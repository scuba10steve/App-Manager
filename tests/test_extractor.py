import os
import tempfile
import unittest
from typing import List

from src.installer.factory.extractor import SevenZipExtractor, ZipExtractor


class ExtractorTests(unittest.TestCase):
    def test_7z(self):
        #setup
        working_dir = tempfile.TemporaryDirectory()
        extractor = SevenZipExtractor()
        extractor.working_dir = working_dir.name

        #when
        extractor.extract('tests/resources/foo.7z')

        #then
        root_dir: List[os.DirEntry] = [entry for entry in os.scandir(extractor.working_dir) if 'foo' in entry.name]

        assert len(root_dir) == 1
        assert os.path.exists(os.path.join(root_dir[0].path, 'foo.txt'))

        working_dir.cleanup()

    def test_zip(self):
        #setup
        working_dir = tempfile.TemporaryDirectory()
        extractor = ZipExtractor()
        extractor.working_dir = working_dir.name

        #when
        extractor.extract('tests/resources/foozip.zip')

        #then
        root_dir: List[os.DirEntry] = [entry for entry in os.scandir(extractor.working_dir) if 'foo' in entry.name]

        assert len(root_dir) == 1
        assert os.path.exists(os.path.join(root_dir[0].path, 'foo.txt'))

        working_dir.cleanup()

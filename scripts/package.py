import os
import zipfile
import tarfile
import sys


PROJECT_DIR = '.'
DEST_DIR = PROJECT_DIR + '/build'
EXCLUDE = ''
VERSION = ''


def main(args):
    if args and len(args) > 1:
        VERSION = args[1]

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    OUTPUT_FILE = DEST_DIR + '/package-' + VERSION

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    zipf = zipfile.ZipFile(os.path.abspath(OUTPUT_FILE) + '.zip', 'w', zipfile.ZIP_BZIP2)
    tarf = tarfile.open(os.path.abspath(OUTPUT_FILE) + '.tar.bz2', 'w:bz2')
    # pylint: disable=unused-variable

    for root, dirs, files in os.walk(PROJECT_DIR + '/src'):
        for file in files:
            zipf.write(os.path.join(root, file))
            tarf.add(os.path.join(root, file))

    zipf.write(os.path.join(os.path.abspath(PROJECT_DIR), 'app.py'))
    tarf.add(os.path.join(os.path.abspath(PROJECT_DIR), 'app.py'))
    zipf.write(os.path.join(os.path.abspath(PROJECT_DIR), 'environment.yml'))
    tarf.add(os.path.join(os.path.abspath(PROJECT_DIR), 'environment.yml'))
    zipf.close()
    tarf.close()
    print('Package: \'' + zipf.filename + '\' created successfully!')
    print('Package: \'' + tarf.name + '\' created successfully!')


if __name__ == "__main__":
    main(sys.argv)

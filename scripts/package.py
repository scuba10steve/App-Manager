import os
import sys
import tarfile
import zipfile

PROJECT_DIR = '.'
DEST_DIR = PROJECT_DIR + '/build'
EXCLUDE = ''


def main(args):
    if args and len(args) > 1:
        version = args[1]

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    output_file = DEST_DIR + '/package-' + version

    if os.path.exists(output_file):
        os.remove(output_file)

    zipf = zipfile.ZipFile(output_file + '.zip', 'w', zipfile.ZIP_BZIP2)
    tarf = tarfile.open(output_file + '.tar.bz2', 'w:bz2')
    # pylint: disable=unused-variable

    for root, dirs, files in os.walk('src'):
        for file in files:
            zipf.write(os.path.join(root, file))
            tarf.add(os.path.join(root, file))

    zipf.write('app.py')
    tarf.add('app.py')
    zipf.write('environment.yml')
    tarf.add('environment.yml')
    zipf.close()
    tarf.close()
    print("Package: '" + os.path.abspath(zipf.filename) + "' created successfully!")
    print("Package: '" + os.path.abspath(tarf.name) + "' created successfully!")


if __name__ == "__main__":
    main(sys.argv)

import os, zipfile


PROJECT_DIR = '.'
DEST_DIR = PROJECT_DIR + '/build'
EXCLUDE = ''
VERSION = '0.1.0'
OUTPUT_FILE = DEST_DIR + '/package-' + VERSION + '.zip'


def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    zipf = zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_BZIP2)
    for root, dirs, files in os.walk(PROJECT_DIR + '/src'):
        for f in files:
            zipf.write(os.path.join(root, f))
    zipf.write(PROJECT_DIR + '/app.py')
    zipf.write(PROJECT_DIR + '/environment.yml')
    zipf.close()
    print('Package: \'' + zipf.filename + '\' created successfully!')


if __name__ == "__main__":
    main()

"""Script to deploy the TSL library to N-Drive."""
import os
import shutil
import zipfile

DEPLOY_PATH = r"\\DE001.itgr.net\PS\RF-UnitPSMUC\Benutzer\TSL\TSL-" \
              r"LIB\TSL-Library.zip"

if __name__ == '__main__':
    print("Zipping tsl library")
    ZIP_NAME = os.path.join(os.path.abspath(os.curdir), f'TSL-Library.zip')
    try:
        os.remove(ZIP_NAME)
    except FileNotFoundError:
        pass

    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("tsl"):
            for file in files:
                print("Zipping: " + os.path.join(root, file))
                zipf.write(os.path.join(root, file))
        zipf.write("setup.py")

    shutil.copyfile(ZIP_NAME, DEPLOY_PATH)

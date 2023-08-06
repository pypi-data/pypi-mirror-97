#!/usr/bin/python3
import os
from argparse import ArgumentParser
from .app import App
from .libs.setuptools import get_file_content


def _handle_args():
    version = get_file_content(os.path.join(os.path.dirname(__file__), "VERSION"))
    parser = ArgumentParser(description="Scan Image WEB UI v{version}".format(version=version))
    parser.add_argument("-p", "--port", dest="port", default=7800, type=int, help="APP server port")
    parser.add_argument("-d", "--scan-directory", dest="scan_diretory", type=str, help="Directory where scanned images will be stored.")

    args = parser.parse_args()
    args.__setattr__("version", version)

    if not args.scan_diretory:
        home = os.path.expanduser("~")
        args.scan_diretory = os.path.join(home, "Pictures/scanimage")
        if not os.path.exists(args.scan_diretory):
            os.makedirs(args.scan_diretory, exist_ok=True)

    return args


def main():
    app_args = _handle_args()
    print("Images will scanned into folder: '{}'".format(app_args.scan_diretory))
    app = App()
    app.init(port=app_args.port, scan_folder_path=app_args.scan_diretory, version=app_args.version)
    app.run()


if __name__ == '__main__':
    main()

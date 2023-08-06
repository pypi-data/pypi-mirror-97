#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from PySide2.QtGui import QGuiApplication  # type: ignore

from qmenta.gui.view import MainView


def main():
    parser = argparse.ArgumentParser(
        description='Front-end for the QMENTA Python client lib.'
    )
    parser.add_argument(
        '--base-url', default='https://platform.qmenta.com',
        help='The base URL of the platform to connect to. ' +
             'Default value = https://platform.qmenta.com'
    )
    parser.add_argument(
        '--keep-tmp-files', action='store_true',
        help='After uploading, keep the temporary zip files generated to '
             'archive directories or anonymise files.'
    )
    args = parser.parse_args()

    # Always use Material styling for the App
    sys_argv = sys.argv
    sys_argv += ['--style', 'Material']

    # Set up the application window
    app = QGuiApplication(sys_argv)
    app.setOrganizationName("QMENTA")
    app.setOrganizationDomain("qmenta.com")
    app.setApplicationName("QMENTA Uploader")

    engine = MainView(args.base_url)
    engine.q_account.keepTmpFiles = args.keep_tmp_files

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

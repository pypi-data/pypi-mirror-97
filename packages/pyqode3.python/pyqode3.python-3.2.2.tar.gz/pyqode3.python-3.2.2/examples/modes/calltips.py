"""
Minimal example showing the use of the CalltipsMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import CalltipsMode


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(CalltipsMode()))
    editor.show()
    editor.appendPlainText(
        'import os\nos.path.join')
    app.exec_()
    editor.close()
    del editor
    del app

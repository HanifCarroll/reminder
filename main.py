import sys
import random
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import Slot, Qt


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setWindowIcon(QtGui.QIcon('./assets/icon.png'))
        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('./assets/icon.png'), parent=self)
        self.tray_icon.setToolTip('Current quote goes here.')
        self.tray_icon.show()

        self.tray_menu = QtWidgets.QMenu()
        exit_action = self.tray_menu.addAction('Exit')
        exit_action.triggered.connect(sys.exit)

        self.tray_icon.setContextMenu(self.tray_menu)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

        self.popup = QtWidgets.QMessageBox()
        self.popup.setText('A doctor a day keeps the apple away.')

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        self.popup.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setWindowTitle('Reminders')
    widget.show()

    sys.exit(app.exec_())
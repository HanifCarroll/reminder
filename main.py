import sys
import random
import sqlite3
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QPushButton,\
                            QLabel, QMessageBox, QVBoxLayout, QApplication
from PySide2.QtCore import Slot, Qt, QTimer


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.db = sqlite3.connect('reminder.db')
        self.reminders = None
        self.active_reminder = None
        self.initialize_db()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_menu = QMenu()
        self.initialize_tray_icon()

        self.disambiguate_timer = QTimer(self)
        self.disambiguate_timer.setSingleShot(True)
        self.disambiguate_timer.timeout.connect(
            self.disambiguate_timer_timeout)

        self.button = QPushButton('Random Reminder')
        self.text = QLabel(self.active_reminder)
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.choose_new_reminder)

        self.popup = QMessageBox()
        self.popup.setText(self.active_reminder)

    @Slot()
    def on_button_press(self):
        self.choose_new_reminder()

    def disambiguate_timer_timeout(self):
        self.popup.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguate_timer.start(150)
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguate_timer.stop()
            print('double click')

    def initialize_db(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS reminder
                            (text text)''')
        self.reminders = list(map(lambda row: row[0], self.db.execute('SELECT * FROM reminder')\
            .fetchall()))
        self.active_reminder = random.choice(self.reminders)

    def initialize_tray_icon(self):
        self.tray_icon.setIcon(QIcon('./assets/icon.png'))
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setToolTip(self.active_reminder)
        self.tray_icon.show()

        exit_action = self.tray_menu.addAction('Exit')
        exit_action.triggered.connect(sys.exit)

        self.tray_icon.setContextMenu(self.tray_menu)

    def choose_new_reminder(self):
        self.active_reminder = random.choice(self.reminders)
        self.text.setText(self.active_reminder)
        self.tray_icon.setToolTip(self.active_reminder)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon('./assets/icon.png'))

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setWindowTitle('Reminders')
    widget.show()

    sys.exit(app.exec_())
import sys
import random
import sqlite3
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QPushButton,\
                            QLabel, QMessageBox, QVBoxLayout, QApplication,\
                            QHBoxLayout
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

        self.new_reminder_button = QPushButton('New')
        self.random_reminder_button = QPushButton('Random Reminder')
        self.reminder_text = QLabel(self.active_reminder)
        self.reminder_text.setAlignment(Qt.AlignCenter)

        self.v_box = QVBoxLayout()
        self.h_box1 = QHBoxLayout()
        self.h_box1.addWidget(self.new_reminder_button, alignment=Qt.AlignRight)
        self.h_box2 = QHBoxLayout()
        self.h_box2.addWidget(self.reminder_text)
        self.h_box3 = QHBoxLayout()
        self.h_box3.addWidget(self.random_reminder_button, alignment=Qt.AlignHCenter)
        self.v_box.addLayout(self.h_box1)
        self.v_box.addLayout(self.h_box2)
        self.v_box.addLayout(self.h_box3)
        self.setLayout(self.v_box)

        # Connecting the signal
        self.random_reminder_button.clicked.connect(self.choose_random_reminder)

        self.popup = QMessageBox()
        self.popup.setText(self.active_reminder)

    @Slot()
    def on_button_press(self):
        self.choose_random_reminder()

    def disambiguate_timer_timeout(self):
        print('single click')

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguate_timer.start(150)
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguate_timer.stop()
            print('double click')

    def initialize_db(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS reminder
                            (id INTEGER PRIMARY KEY, text TEXT)''')
        self.reminders = list(map(lambda row: row[0], self.db.execute('SELECT * FROM reminder')\
            .fetchall()))
        if len(self.reminders):
            self.active_reminder = random.choice(self.reminders)
        else:
            self.active_reminder = 'No saved reminders.  Try adding one now :)'

    def initialize_tray_icon(self):
        self.tray_icon.setIcon(QIcon('./assets/icon.png'))
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setToolTip(self.active_reminder)
        self.tray_icon.show()

        exit_action = self.tray_menu.addAction('Exit')
        exit_action.triggered.connect(sys.exit)

        self.tray_icon.setContextMenu(self.tray_menu)

    def choose_random_reminder(self):
        if not len(self.reminders):
            self.show_alert('Please add a new reminder.')
            return
        self.active_reminder = random.choice(self.reminders)
        self.reminder_text.setText(self.active_reminder)
        self.tray_icon.setToolTip(self.active_reminder)

    def show_alert(self, text):
        self.popup.setText(text)
        self.popup.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon('./assets/icon.png'))

    widget = MyWidget()
    widget.resize(400, 300)
    widget.setWindowTitle('Reminders')
    widget.show()

    sys.exit(app.exec_())
import sys
import random
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QPushButton, \
    QLabel, QMessageBox, QVBoxLayout, QApplication, \
    QHBoxLayout, QPlainTextEdit, QListWidget
from PySide2.QtCore import Slot, Qt, QTimer
import db


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

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

        self.view_reminders_button = QPushButton('View')
        self.view_reminders_button.clicked.connect(self.on_view_reminders_button_clicked)

        self.new_reminder_button = QPushButton('New')
        self.new_reminder_button.clicked.connect(self.on_new_reminder_button_clicked)

        self.random_reminder_button = QPushButton('Random Reminder')
        self.random_reminder_button.clicked.connect(self.on_random_reminder_button_clicked)

        self.reminder_text = QLabel(self.active_reminder)
        self.reminder_text.setAlignment(Qt.AlignCenter)

        self.v_box = QVBoxLayout()
        self.h_box1 = QHBoxLayout()
        self.h_box1.addWidget(self.view_reminders_button, alignment=Qt.AlignLeft)
        self.h_box1.addWidget(self.new_reminder_button, alignment=Qt.AlignRight)
        self.h_box2 = QHBoxLayout()
        self.h_box2.addWidget(self.reminder_text)
        self.h_box3 = QHBoxLayout()
        self.h_box3.addWidget(self.random_reminder_button, alignment=Qt.AlignHCenter)
        self.v_box.addLayout(self.h_box1)
        self.v_box.addLayout(self.h_box2)
        self.v_box.addLayout(self.h_box3)
        self.setLayout(self.v_box)

        self.popup = QMessageBox()
        self.popup.setText(self.active_reminder)

        self.new_reminder_window = NewReminderWindow()
        self.new_reminder_window.save_button.clicked.connect(self.on_save_clicked)

        self.view_reminders_window = ViewRemindersWindow()

    @Slot()
    def on_random_reminder_button_clicked(self):
        self.choose_random_reminder()

    @Slot()
    def on_new_reminder_button_clicked(self):
        self.new_reminder_window.show()
        self.new_reminder_window.new_reminder_text_input.setFocus()

    @Slot()
    def on_view_reminders_button_clicked(self):
        for reminder in db.get_reminders():
            self.view_reminders_window.reminders_list.addItem(reminder[1])
        self.view_reminders_window.show()

    @Slot()
    def disambiguate_timer_timeout(self):
        print('single click')

    @Slot()
    def on_save_clicked(self):
        db.save_new_reminder(self.new_reminder_window.new_reminder_text_input.toPlainText())
        self.new_reminder_window.new_reminder_text_input.clear()
        self.new_reminder_window.hide()

    @Slot()
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguate_timer.start(150)
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguate_timer.stop()
            print('double click')

    def initialize_db(self):
        db.initialize()
        self.reminders = db.get_reminders()

        if len(self.reminders):
            self.active_reminder = random.choice(self.reminders)[1]
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
        self.reminder_text.setText(self.active_reminder[1])
        self.popup.setText(self.active_reminder[1])
        self.tray_icon.setToolTip(self.active_reminder[1])

    def show_alert(self, text):
        self.popup.setText(text)
        self.popup.show()


class NewReminderWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(500, 250)
        self.setWindowTitle('Add New Reminder')

        self.new_reminder_text_input = QPlainTextEdit()
        self.new_reminder_text_input.setFixedHeight(90)
        self.new_reminder_text_input.setFixedWidth(500)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFixedWidth(self.cancel_button.minimumSizeHint().width())
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.save_button = QPushButton('Save')
        self.save_button.setFixedWidth((self.save_button.minimumSizeHint().width()))

        self.v_box = QVBoxLayout()
        self.h_box1 = QHBoxLayout()
        self.h_box1.addWidget(self.new_reminder_text_input, alignment=Qt.AlignHCenter)
        self.h_box2 = QHBoxLayout()
        self.h_box2.addWidget(self.cancel_button)
        self.h_box2.addWidget(self.save_button)
        self.v_box.addLayout(self.h_box1)
        self.v_box.addLayout(self.h_box2)
        self.setLayout(self.v_box)

    @Slot()
    def on_cancel_clicked(self):
        self.hide()
        self.new_reminder_text_input.clear()


class ViewRemindersWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(400, 600)
        self.setWindowTitle('View Reminders')
        self.reminders_list = QListWidget()

        self.v_box = QVBoxLayout()
        self.h_box1 = QHBoxLayout()

        self.h_box1.addWidget(self.reminders_list)

        self.v_box.addLayout(self.h_box1)

        self.setLayout(self.v_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon('./assets/icon.png'))

    widget = MainWindow()
    widget.resize(400, 300)
    widget.setWindowTitle('Reminders')
    widget.show()

    sys.exit(app.exec_())

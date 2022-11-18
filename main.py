from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from plyer import notification
from PIL import Image
import sys, time, pyttsx3, ast, re, pystray


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui_main.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("rotina.py")

        self.addButton.clicked.connect(self.add_task)
        self.startButton.clicked.connect(self.start_routine)
        self.stopButton.clicked.connect(self.stop_routine)
        self.closeButton.mouseReleaseEvent = lambda event: sys.exit()
        self.minButton.mouseReleaseEvent = self.hide_win
        self.saveButton.mouseReleaseEvent = self.save_routine
        self.loadButton.mouseReleaseEvent = self.load_routine

        self.tasks = []
        self.thread = {}
        self.notification = True
        self.mapping_widget = {}

    def add_task(self):
        print("Adding task...")
        self.info_label.close()
        self.title = self.input_title.text()
        if self.title == '':
            self.title = '--'
        self.description = self.input_description.text()
        if self.description == '':
            self.description = '--'
        self.hour = self.input_time.text()
        self.add_widget()
        self.tasks.append({'title': self.title, 'description': self.description, 'hour': self.hour, 'check': False, 'button': self.closeButton})

    def add_widget(self):
        print("Adding widgets...")
        self.new_frame = QFrame(None)
        self.new_frame.setMinimumSize(80, 80)
        self.new_frame.setMaximumSize(340, 80)
        self.new_frame.setStyleSheet('QFrame{ background-color: transparent;} QFrame:hover{ background-color: rgb(29, 43, 56);}')

        self.verticalLayout_3.addWidget(self.new_frame)
        self.new_layout = QGridLayout(self.new_frame)

        self.uni_sans_bold = QtGui.QFont()
        self.uni_sans_bold.setFamily("Uni Sans")
        self.uni_sans_bold.setPointSize(12)
        self.uni_sans_bold.setBold(True)
        self.uni_sans_bold.setWeight(75)

        self.new_label_title = QLabel(self.title)
        self.new_label_title.setFont(self.uni_sans_bold)
        self.new_label_title.setMinimumSize(QtCore.QSize(150, 30))
        self.new_label_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)

        self.uni_sans_thin = QtGui.QFont()
        self.uni_sans_thin.setFamily("Uni Sans")
        self.uni_sans_thin.setPointSize(8)
        self.uni_sans_thin.setWeight(45)

        self.new_label_description = QLabel(self.description)
        self.new_label_description.setFont(self.uni_sans_thin)
        self.new_label_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.uni_sans = QtGui.QFont()
        self.uni_sans.setFamily("Uni Sans")
        self.uni_sans.setPointSize(22)

        self.new_label_time = QLabel(self.hour)
        self.new_label_time.setFont(self.uni_sans)
        self.new_label_time.setMinimumSize(QtCore.QSize(0, 50))
        self.new_label_time.setAlignment(Qt.AlignCenter)

        self.closeButton = QPushButton(self.new_frame)
        self.closeButton.setMaximumSize(QtCore.QSize(20, 20))
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setText("x")
        self.closeButton.clicked.connect(self.handle_delete_clicked)
        self.mapping_widget[self.closeButton] = self.new_frame

        self.new_layout.addWidget(self.new_label_time, 0, 0, 2, 1)
        self.new_layout.addWidget(self.new_label_title, 0, 1, 1, 1)
        self.new_layout.addWidget(self.new_label_description, 1, 1, 1, 1)
        self.new_layout.addWidget(self.closeButton, 0, 2, 1, 1)

    def handle_delete_clicked(self):
        button = self.sender()
        if not isinstance(button, QPushButton):
            return

        label = self.mapping_widget.get(button)
        if label is None:
            return

        del self.mapping_widget[button]
        for row in self.tasks:
            if button == row['button']:
                row['hour'] = None
                del row

        button.deleteLater()
        label.deleteLater()

    def start_routine(self):
        print("Starting routine...")
        self.notif_label.setText("[notifications: on]")
        self.notification = True
        self.thread[0] = ThreadClass(parent=None, index=1)
        self.thread[0].start()

    def stop_routine(self):
        print("Stopping thread...")
        self.notification = False
        self.notif_label.setText("[notifications: off]")

    def save_routine(self, event):
        print("Saving routine...")
        self.saving_tasks = self.tasks
        for row in self.saving_tasks:
            row['button'] = 0

        filename = QFileDialog.getSaveFileName(self, 'Save File', '', "Text (*.txt)")
        if filename[0] == '':
            return

        with open(f'{filename[0]}', 'w') as f:
            f.write(str(self.saving_tasks))

    def load_routine(self, event):
        print("Loading routine...")
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', "Text (*.txt)")

        if filename[0] == '':
            return

        for i in reversed(range(self.verticalLayout_3.count())):
            self.verticalLayout_3.itemAt(i).widget().close()

        f = open(f'{filename[0]}', 'r')
        f = str(f.read())
        self.tasks = ast.literal_eval(f)

        for row in self.tasks:
            if row['check']:
                row['check'] = False


        for row in self.tasks:
            if row['hour'] == None:
                continue

            self.new_frame = QFrame(None)
            self.new_frame.setMinimumSize(80, 80)
            self.new_frame.setMaximumSize(340, 80)
            self.new_frame.setStyleSheet('QFrame{ background-color: transparent;} QFrame:hover{ background-color: rgb(29, 43, 56);}')

            self.verticalLayout_3.addWidget(self.new_frame)
            self.new_layout = QGridLayout(self.new_frame)

            self.uni_sans_bold = QtGui.QFont()
            self.uni_sans_bold.setFamily("Uni Sans")
            self.uni_sans_bold.setPointSize(12)
            self.uni_sans_bold.setBold(True)
            self.uni_sans_bold.setWeight(75)

            self.new_label_title = QLabel(row['title'])
            self.new_label_title.setFont(self.uni_sans_bold)
            self.new_label_title.setMinimumSize(QtCore.QSize(150, 30))
            self.new_label_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)

            self.uni_sans_thin = QtGui.QFont()
            self.uni_sans_thin.setFamily("Uni Sans")
            self.uni_sans_thin.setPointSize(8)
            self.uni_sans_thin.setWeight(45)

            self.new_label_description = QLabel(row['description'])
            self.new_label_description.setFont(self.uni_sans_thin)
            self.new_label_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

            self.uni_sans = QtGui.QFont()
            self.uni_sans.setFamily("Uni Sans")
            self.uni_sans.setPointSize(22)

            self.new_label_time = QLabel(row['hour'])
            self.new_label_time.setFont(self.uni_sans)
            self.new_label_time.setMinimumSize(QtCore.QSize(0, 50))
            self.new_label_time.setAlignment(Qt.AlignCenter)

            self.closeButton = QPushButton(self.new_frame)
            self.closeButton.setMaximumSize(QtCore.QSize(20, 20))
            self.closeButton.setObjectName("closeButton")
            self.closeButton.setText("x")
            self.closeButton.clicked.connect(self.handle_delete_clicked)
            self.mapping_widget[self.closeButton] = self.new_frame

            self.new_layout.addWidget(self.new_label_time, 0, 0, 2, 1)
            self.new_layout.addWidget(self.new_label_title, 0, 1, 1, 1)
            self.new_layout.addWidget(self.new_label_description, 1, 1, 1, 1)
            self.new_layout.addWidget(self.closeButton, 0, 2, 1, 1)

    def hide_win(self, event):

        import ctypes
        import win32gui, win32con
        from pynput.keyboard import Key, Controller

        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        titles = []

        def enumHandler(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                if 'rotina.py' in win32gui.GetWindowText(hwnd):
                    titles.append(hwnd)

        win32gui.EnumWindows(enumHandler, None)

        for i in range(len(titles)):
            print(titles[i])

        def focus_win():
            win32gui.SetForegroundWindow(titles[0])

        def open_window(icon, item):
            self.show()
            icon.stop()
            focus_win()

        self.showMinimized()
        self.hide()
        image = Image.open("icon.ico")
        icon = pystray.Icon("Rotina", image, menu=pystray.Menu(
            pystray.MenuItem("Open", open_window, default=True)
            ))
        icon.run()


class ThreadClass(QThread):
    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        print("Running thread...")

        while win.notification:

            t = time.localtime()
            current_time = time.strftime("%H:%M", t)

            for row in win.tasks:
                if row['hour'] == current_time and row['check'] == False:
                    row['check'] = True
                    notification.notify(title=f"{row['title']}",
                                                 message=f"{row['description']}",
                                                 app_icon="icons/bell.ico",
                                                 timeout=10,
                                                 toast=False)
                    engine = pyttsx3.init()
                    for voice in engine.getProperty('voices'):
                        if "Zira" in voice.name:
                            break
                    engine.setProperty('voice', voice.id)
                    engine.say(f"It's time to {row['title']}")
                    engine.runAndWait()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

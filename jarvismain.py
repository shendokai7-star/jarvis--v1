from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtCore import QMetaType
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from tryinggui import Ui_MainWindow
from Body.listen import MicExecution
from Body.speak2 import Speak
from Brain.clap import Tester
from Features.greet import greetMe
from Main import EveryTask
from Normal.time import Time
from Normal.temperature import Temper
import sys
from Brain.main import get_response
#from Features.guicopy import Ui_MainWindow
class MainThread(QtCore.QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.MainExecution()

    def MainExecution(self):
        Speak("Initializing Jarvis")
        Speak("Calibrating and examining all the core processors")
        Time()
        greetMe()

        while True:
            Data = MicExecution()
            Data = str(Data)

            ValueReturn = EveryTask(Data)
            if ValueReturn:
                pass
            elif len(Data) < 3:
                pass
            elif "shutdown" in Data or "bye bye " in Data:
                Speak("Good Night, MasterKai")
                break
            else:
                pass
                Reply = get_response(Data)
                Speak(Reply)

class CheckClap(QtCore.QThread):
    def __init__(self):
        super(CheckClap, self).__init__()

    def run(self):
        self.ClapDetect()

    def ClapDetect(self):
        query = Tester()
        if "True-Mic" in query:
            print("")
            start = MainThread()
            start.MainExecution()


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon("imagen-jarvis-mark-theme-0ori.ico")
        self.setWindowIcon(icon)
        self.movie2 = QMovie("guifile/00b6c716490c3ec6fe4c9bef2b595f43.gif")
        self.ui.gif.setMovie(self.movie2)
        self.movie2.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.startExecution = None
        self.startTask()
        
        self.sleep_mode = False
        self.main_thread = None
        # Redirect stdout and stderr to QTextBrowser
        sys.stdout = StdoutRedirector(self.ui.terminal)
        sys.stderr = StderrRedirector(self.ui.terminal)

    def __del__(self):
        if self.startExecution:
            self.startExecution.quit()
            self.startExecution.wait()
            
    def enableSleepMode(self):
        self.sleep_mode = True

    def disableSleepMode(self):
        self.sleep_mode = False

        if self.main_thread is not None:
            self.main_thread.resume_execution()
            
    def startTask(self):
        self.startExecution = CheckClap()
        self.startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.ui.time2023.setText(label_time)
        # Scroll to the bottom of the QTextBrowser
        self.ui.terminal.moveCursor(QTextCursor.End)

    def resizeEvent(self, event):
        # Call the base class resizeEvent method
        super().resizeEvent(event)

        # Get the new size of the main window
        new_size = event.size()

        # Calculate the scale factors for the widgets
        width_scale = new_size.width() / 1322
        height_scale = new_size.height() / 851

        # Adjust the positions and sizes of the widgets based on the scale factors
        self.ui.label.setGeometry(QtCore.QRect(int(-60 * width_scale), int(-40 * height_scale), int((1381 + 120) * width_scale), int((911 + 80) * height_scale)))
        self.ui.label_2.setGeometry(QtCore.QRect(0, 0, new_size.width(), new_size.height()))
        self.ui.gif.setGeometry(QtCore.QRect(int(160 * width_scale), int(20 * height_scale), int(1091 * width_scale), int(801 * height_scale)))
        self.ui.terminal.setGeometry(QtCore.QRect(int(40 * width_scale), int(570 * height_scale), int(381 * width_scale), int(221 * height_scale)))
        self.ui.time2023.setGeometry(QtCore.QRect(int(1010 * width_scale), int(760 * height_scale), int(291 * width_scale), int(81 * height_scale)))
    
   
            
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.append(text)

    def flush(self):
        pass

class StderrRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.append(text)

    def flush(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())

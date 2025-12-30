from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1322, 851)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-60, -40, 1381, 911))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label.setText("")
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1322, 851))
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 0, 0);\n"
"border : 3px Solid orange;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gif = QtWidgets.QLabel(self.centralwidget)
        self.gif.setGeometry(QtCore.QRect(160, 20, 1091, 801))
        self.gif.setText("")
        self.gif.setPixmap(QtGui.QPixmap("guifile/00b6c716490c3ec6fe4c9bef2b595f43.gif"))
        self.gif.setScaledContents(True)
        self.gif.setStyleSheet("border : 1px solid blue;")
        self.gif.setObjectName("gif")
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        self.terminal.setGeometry(QtCore.QRect(40, 570, 381, 221))
        self.terminal.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border : 1px solid blue;\n"
"color: rgb(255, 255, 255);\n"
"font: 10pt \"Open Sans\";")
        self.terminal.setObjectName("terminal")
        self.time2023 = QtWidgets.QTextBrowser(self.centralwidget)
        self.time2023.setGeometry(QtCore.QRect(1010, 760, 291, 81))
        self.time2023.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border : 2px solid white;\n"
"color: rgb(255, 255, 255);\n"
"font: 25pt \"MS Shell Dlg 2\";")
        self.time2023.setObjectName("time2023")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon("imagen-jarvis-mark-theme-0ori.ico")
        self.setWindowIcon(icon)
    def resizeEvent(self, event):
        # Get the new size of the main window
        new_size = event.size()

        # Calculate the scale factor based on the original size (1322, 851)
        width_scale = new_size.width() / 1322
        height_scale = new_size.height() / 851

        # Adjust the position of the elements based on the scale factor
        self.ui.label.setGeometry(QtCore.QRect(int(-60 * width_scale), int(-40 * height_scale), int((1381 + 120) * width_scale), int((911 + 80) * height_scale)))
        self.ui.label_2.setGeometry(QtCore.QRect(0, 0, new_size.width(), new_size.height()))
        self.ui.gif.setGeometry(QtCore.QRect(int(160 * width_scale), int(20 * height_scale), int(1091 * width_scale), int(801 * height_scale)))
        self.ui.terminal.setGeometry(QtCore.QRect(int(40 * width_scale), int(570 * height_scale), int(381 * width_scale), int(221 * height_scale)))
        self.ui.time2023.setGeometry(QtCore.QRect(int(1010 * width_scale), int(760 * height_scale), int(291 * width_scale), int(81 * height_scale)))

        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

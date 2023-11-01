# -*- coding: utf-8 -*-
import sys
import time

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication
from vcr_gui import Ui_MainWindow

# from Graphics import plot_graphics, data_read # тут логика графиков
# from MplForWidget import MyMplCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


# file_path = 'salesmonthly.csv'

import warnings
warnings.filterwarnings("ignore")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
        print(int(self.pushButton.text()))
        one = 1


        self.add_functions()

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(int(self.pushButton.text())))
        # self.view_graphic.clicked.connect(lambda: self.plot())
        # self.view_graphic.clicked.connect(self.prepare_canvas_and_toolbar)
        # self.comboBox_2.currentIndexChanged.connect(self.prepare_canvas_and_toolbar)

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


main()


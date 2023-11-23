# -*- coding: utf-8 -*-
import datetime
import sys
import time
from collections import defaultdict

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from vcr_gui_v014 import Ui_MainWindow
import server as srv

# from Graphics import plot_graphics, data_read # тут логика графиков
# from MplForWidget import MyMplCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


# file_path = 'salesmonthly.csv'

import warnings
warnings.filterwarnings("ignore")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.reload()

    def reload(self):
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("img\moon.png"))
        # self.showMaximized()

        pBtn_style_sheet = "background-color: rgb(177, 255, 170);\n border-radius: 40px;\n color: rgb(43, 89, 250);\n border: 1px solid rgb(43, 89, 250);}\n QPushButton:hover{    \n background-color: #9CDF96;}"

        self.pBtn_production_acc.setStyleSheet(pBtn_style_sheet)
        self.pBtn_production_sales_acc.setStyleSheet(pBtn_style_sheet)
        self.pBtn_an_sales.setStyleSheet(pBtn_style_sheet)
        self.pBtn_recipe.setStyleSheet(pBtn_style_sheet)
        self.pBtn_products.setStyleSheet(pBtn_style_sheet)
        self.pBtn_an_sales_product.setStyleSheet(pBtn_style_sheet)
        self.pBtn_an_sales_production.setStyleSheet(pBtn_style_sheet)

        self.add_functions()
        self.btn_navigation()
        self.btn_back()
        self.date_select()

    def add_functions(self):
        self.calendarWidget_5.clicked.connect(self.date_select)
        self.calendarWidget_6.clicked.connect(self.date_select)
        self.calendarWidget.clicked.connect(self.date_select)
        self.calendarWidget_2.clicked.connect(self.date_select)

        self.pushButton_8.clicked.connect(lambda: self.add_combox(self.verticalLayout_6, db_products_accounting))
        self.pushButton_8.clicked.connect(self.add_spinbox)
        # добавляем запись в таблицу справа
        # self.pushButton_8.clicked.connect(lambda: self.add_tablerow(self.tableWidget, db_recipe_cost))
        self.pushButton_10.clicked.connect(lambda: self.add_tablerow(self.tableWidget, db_recipe_cost))

        self.pushButton_9.clicked.connect(lambda: self.add_combox(self.verticalLayout_19, db_sales_accounting))


    def add_spinbox(self):
        self.spinBox = QtWidgets.QSpinBox()

        self.spinBox.setMinimumSize(QtCore.QSize(300, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.spinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "color: rgb(43, 89, 250);")
        self.spinBox.setMaximum(999999)

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        self.spinBox.setFont(font)

        self.spinBox.setObjectName(f'{self.verticalLayout_11.objectName()}_{len(self.verticalLayout_11)}')

        self.verticalLayout_11.addWidget(self.spinBox)

        # print(self.spinBox.value())
        # print(self.spinBox.objectName())

    def add_combox(self, layout, db_name):
        # print("click")
        self.comboBox = QtWidgets.QComboBox()

        combox = self.comboBox

        combox.setMinimumSize(QtCore.QSize(300, 0))
        combox.setMaximumSize(QtCore.QSize(300, 16777215))
        combox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "color: rgb(43, 89, 250);")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        combox.setFont(font)

        self.fill_combox(db_name, combox)

        # устанавливаем имя добавляемого комбобокса как  "имя лэйаута" + "порядковый номер(начиная с 0)"
        combox.setObjectName(f'{layout.objectName()}_{len(layout)}')

        layout.addWidget(combox)
        # print(combox.objectName())
        # print(combox.currentText())

        combox.addItem("first")
        # print(combox.currentText())

        # verticalScrollBar()->setValue(ui.textEdit->verticalScrollBar()->maximum());
        # не получается
        # self.scrollArea_2.verticalScrollBar().setValue(self.scrollArea_2.maximum())

    def date_select(self):
        self.textEdit_4.setText(self.calendarWidget_5.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_5.setText(self.calendarWidget_6.selectedDate().toString('dd-MM-yyyy'))

        self.textEdit_2.setText(self.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
        self.textEdit_3.setText(self.calendarWidget_2.selectedDate().toString('dd-MM-yyyy'))

    def btn_navigation(self):
        self.pBtn_production_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.pBtn_production_sales_acc.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pBtn_production_sales_acc.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_an_sales.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pBtn_an_sales.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_recipe.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        self.pBtn_products.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.pBtn_products.clicked.connect(lambda: self.load_info(self.stackedWidget.currentIndex()))

        self.pBtn_an_sales_product.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))
        self.pBtn_an_sales_product.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))
        self.pBtn_an_sales_production.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.pBtn_an_sales_production.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))

    def load_info(self, current_page):
        match current_page:
            case 1:
                print("1")

            case 2:
                print("Учёт продаж собственной продукции")
                self.add_combox(self.verticalLayout_6, db_products_accounting)
                self.add_spinbox()

                # recept = srv.select_from_table(connection, db_recipe_cost)
                # print(recept)
                # self.tableWidget.clearContents()
                #
                # self.tableWidget.setRowCount(len(recept))
                #
                # # # составляем отдельный список id
                # # for row in recept:
                # #     select_production.append(row[1])
                #
                # rows = len(self.verticalLayout_6)
                # # rows = self.tableWidget.rowCount()
                # # cols = self.tableWidget.columnCount()
                #
                # for row in range(rows):
                #     self.tableWidget.setItem(row, 0, QTableWidgetItem("Тут продукция"))
                #     self.tableWidget.setItem(row, 1, QTableWidgetItem("Тут граммы"))
                #     self.tableWidget.setItem(row, 2, QTableWidgetItem("Тут цена"))
                # self.tableWidget.cellWidget(row, 1)
                # self.tableWidget.insertRow()
                # self.fill_combox(db_products_accounting, self.comboBox_6)

            case 3:
                print("Анализ продаж")

            case "3-1":
                print("Анализ продаж продукции")
                self.add_combox(self.verticalLayout_19, db_sales_accounting)
                # self.fill_combox(db_sales_accounting, self.comboBox)

            case "3-2":
                print("Анализ продаж продуктов")
                self.fill_combox(db_products_accounting, self.comboBox_2)

            case 4:
                print("4")

            case 5:
                print("Учёт продуктов на изготовление собственной продукции")
                self.fill_combox(db_recipe, self.comboBox_3)

    def add_tablerow(self, table, db_name):
        recipe = srv.select_from_table(connection, db_name)
        recipe_cost_list = defaultdict(list)
        for row in recipe:
            recipe_cost_list[row[1]].append(row[2])

        print(recipe_cost_list)
        # print(recept)
        table.clearContents()

        table.setRowCount(len(self.verticalLayout_6))

        rows = len(self.verticalLayout_6)

        # index = self.verticalLayout_6.count()

        #########################################################################
        # РАБОТАЕТ !!!!!!!!!!!!!!!!!!!!!!!!!!
        # print(self.verticalLayout_6.itemAt(0).widget().currentText())
        #########################################################################

        # print(self.comboBox.objectName() + "это в add_row")
        # print(self.verticalLayout_11.itemAt(0).widget().value())

        for row in range(rows):
            name_production = self.verticalLayout_6.itemAt(row).widget().currentText()
            gram = self.verticalLayout_11.itemAt(row).widget().value()
            table.setItem(row, 0, QTableWidgetItem(name_production))
            table.setItem(row, 1, QTableWidgetItem(str(gram)))
            if name_production in recipe_cost_list:
                table.setItem(row, 2, QTableWidgetItem("Это имя есть"))
                print(gram * (recipe_cost_list[name_production]))
                # table.setItem(row, 2, QTableWidgetItem(str(gram * float(recipe_cost_list[name_production]))))

    def fill_combox(self, db_name, combox):
        # print("тут fill_combox")
        # получаем всю информацию из таблицы
        select_data_from_table = srv.select_from_table(connection, db_name)
        select_production = []

        # составляем отдельный список id
        for row in select_data_from_table:
            select_production.append(row[1])

        # удаляем лишние id
        select_production_id = set(select_production)

        # превратим индексы продукции в наименование
        select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
        select_production_name = []

        # ищем имена по индексам
        for id in select_production_id:
            for row in select_data_from_table:
                if id == row[0]:
                    select_production_name.append(row[1])

        # combox.clear()
        for name in select_production_name:
            combox.addItem(str(name))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        combox.setFont(font)

    def btn_back(self):
        self.pBtn_back_to_main_9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_9.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        # сдесь установление стандартных параметров страницы
        self.pBtn_back_to_main_2.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_3.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_4.clicked.connect(lambda: self.reload())

        self.pBtn_back_to_main_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pBtn_back_to_main_5.clicked.connect(lambda: self.reload())

        #################################################################################################
        # тут нужно вернуться на выбор анализа

        self.pBtn_back_to_main_6.clicked.connect(lambda: self.reload())
        self.pBtn_back_to_main_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.pBtn_back_to_main_7.clicked.connect(lambda: self.reload())
        self.pBtn_back_to_main_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        #################################################################################################


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

db_products = "products"
db_products_accounting = "products_accounting"
db_recipe = "recipe"
db_recipe_cost = "recipe_cost"
db_sales_accounting = "sales_accounting"

connection = None
connection = srv.set_connection(connection)
connection.autocommit = True
srv.check_connection(connection)

main()

# КОД НЕ ДОХОДИТ ДО ЗАКРЫТИЯ СОЕДИНЕНИЯ
srv.close_connection(connection)
srv.check_connection(connection)

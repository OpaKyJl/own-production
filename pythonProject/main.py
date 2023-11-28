# -*- coding: utf-8 -*-
import datetime
import sys
import threading

import time
from collections import defaultdict
from math import ceil

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from vcr_gui_v021 import Ui_MainWindow
import server as srv

from MplForWidget import MyMplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd
import mplcursors as mplc

# from Graphics import plot_graphics, data_read # тут логика графиков
# from MplForWidget import MyMplCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


# file_path = 'salesmonthly.csv'
# путь к датасету
file_path = 'salesmonthly.csv'

import warnings
warnings.filterwarnings("ignore")
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.reload()
        # data = defaultdict(list)
        # self.canvas = MyMplCanvas(self.get_graphic(data))
        # self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget_2)
        # self.companovka_for_mpl.addWidget(self.canvas)
        #
        # # self.toolbar.hide()
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # self.addToolBar(Qt.Qt.TopToolBarArea, self.toolbar)

    def reload(self):
        self.setupUi(self)
        self.set_default_status_bar()

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

        # продукты
        data = defaultdict(list)
        self.canvas = MyMplCanvas(self.get_graphic(data, db_products_accounting))
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget_2)

        # сначала добавляем тулбар
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka_for_mpl.addWidget(self.toolbar)

        self.companovka_for_mpl.addWidget(self.canvas)

        # продукция (не работает совместно)  может добавить_2
        data_2 = defaultdict(list)
        self.canvas_2 = MyMplCanvas(self.get_graphic(data_2, db_sales_accounting))
        self.companovka_for_mpl_2 = QtWidgets.QVBoxLayout(self.widget)

        # сначала добавляем тулбар
        self.toolbar_2 = NavigationToolbar(self.canvas_2, self)
        self.companovka_for_mpl_2.addWidget(self.toolbar_2)

        self.companovka_for_mpl_2.addWidget(self.canvas_2)

        self.add_functions()
        self.btn_navigation()
        self.btn_back()
        self.date_select()

    def closeEvent(self, event):
        # закрытие соединения с БД
        srv.close_connection(connection)
        srv.check_connection(connection)

    def add_functions(self):
        self.calendarWidget_5.clicked.connect(self.date_select)
        self.calendarWidget_6.clicked.connect(self.date_select)
        self.calendarWidget.clicked.connect(self.date_select)
        self.calendarWidget_2.clicked.connect(self.date_select)

        self.pushButton_8.clicked.connect(lambda: self.add_combox(self.verticalLayout_6, db_products_accounting))
        self.pushButton_8.clicked.connect(self.add_spinbox)
        # добавляем запись в таблицу справа
        self.pushButton_10.clicked.connect(lambda: self.add_tablerow(self.tableWidget, db_recipe_cost, self.stackedWidget.currentIndex()))

        self.pushButton_9.clicked.connect(lambda: self.add_combox(self.verticalLayout_19, db_sales_accounting))

        self.pushButton_5.clicked.connect(lambda: self.add_tablerow(self.tableWidget_2, db_recipe, self.stackedWidget.currentIndex()))

        self.comboBox_2.currentIndexChanged.connect(lambda: self.load_info("3-2"))

        # добавляем данные в таблицу
        self.pushButton_6.clicked.connect(lambda: self.insert_data_to_table(db_products_accounting))
        self.pushButton_7.clicked.connect(lambda: self.insert_data_to_table(db_sales_accounting))

        # строим графики для анализа
        self.pushButton_3.clicked.connect(lambda: self.get_graphics(db_products_accounting))
        # self.pushButton_3.clicked.connect(lambda: self.prepare_canvas_and_toolbar(data))
        # self.prepare_canvas_and_toolbar(data)
        self.pushButton.clicked.connect(lambda: self.get_graphics(db_sales_accounting) )

        self.checkBox_2.stateChanged.connect(self.get_all_products)

    def set_default_status_bar(self):
        self.statusBar.clearMessage()
        self.statusBar.setStyleSheet("background-color: #b1ffaa")

    def set_status_bar(self, msg):
        interval = 5
        match msg:
            case "сохранить":
                self.statusBar.showMessage("Данные сохранены")
                self.statusBar.setStyleSheet("background-color: #00FF7F")

            case "анализ":
                self.statusBar.showMessage("Данные предоставлены для анализа")
                self.statusBar.setStyleSheet("background-color: #00FF7F")

            case "дата":
                self.statusBar.showMessage("Некорректная дата")
                self.statusBar.setStyleSheet("background-color: red")

        clear = self.set_default_status_bar

        # #b1ffaa
        t = threading.Timer(interval, clear)
        t.start()


    def get_all_products(self):
        layout = self.verticalLayout_43
        products_from_table = srv.select_from_table(connection, db_products)

        if self.checkBox_2.checkState() == 2:
            self.clear_layout(layout)
            for row in products_from_table:
                self.add_checkbox(row[1])
        else:
            self.load_info("3-2")

    def add_spinbox(self):
        self.spinBox = QtWidgets.QSpinBox()

        self.spinBox.setMinimumSize(QtCore.QSize(300, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.spinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "color: rgb(43, 89, 250);")
        self.spinBox.setMinimum(50)
        self.spinBox.setMaximum(999999)

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        self.spinBox.setFont(font)
        self.spinBox.setObjectName(f'{self.verticalLayout_11.objectName()}_{len(self.verticalLayout_11)}')
        self.verticalLayout_11.addWidget(self.spinBox)


    def add_combox(self, layout, db_name):
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


    def add_checkbox(self, text):
        # print("click")

        layout = self.verticalLayout_43
        self.checkBox = QtWidgets.QCheckBox()
        checkbox = self.checkBox

        checkbox.setMinimumSize(QtCore.QSize(300, 0))
        checkbox.setMaximumSize(QtCore.QSize(300, 16777215))
        checkbox.setStyleSheet("background-color: rgb(255, 233, 190);\n"
                                      "color: rgb(43, 89, 250);")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        checkbox.setFont(font)

        checkbox.setObjectName(f'{layout.objectName()}_{len(layout)}')
        checkbox.setText(text)
        layout.addWidget(checkbox)


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
        # загрузка комбобокса
        self.pBtn_an_sales_product.clicked.connect(lambda: self.fill_combox(db_products_accounting, self.comboBox_2))
        self.pBtn_an_sales_product.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))
        self.pBtn_an_sales_production.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.pBtn_an_sales_production.clicked.connect(lambda: (self.load_info(f'{self.stackedWidget.currentIndex()}-{self.stackedWidget_2.currentIndex()}')))

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    def load_info(self, current_page):
        match current_page:
            case 1:
                print("1")

            case 2:
                print("Учёт продаж собственной продукции")
                self.add_combox(self.verticalLayout_6, db_products_accounting)
                self.add_spinbox()
                self.add_tablerow(self.tableWidget, db_recipe_cost, self.stackedWidget.currentIndex())

            case 3:
                print("Анализ продаж")

            case "3-1":
                print("Анализ продаж продукции")
                self.add_combox(self.verticalLayout_19, db_sales_accounting)
                production_acc = srv.select_from_table(connection, db_products_accounting)
                production_acc_list = defaultdict(list)

                for row in production_acc:
                    production_acc_list[row[1]].append([row[2], row[3],float(row[4]), float(row[5])])

                products_from_table = srv.select_from_table(connection, db_products)
                product_list = defaultdict(list)

                for row in products_from_table:
                    product_list[row[0]].append([row[1], float(row[2])])

            case "3-2":
                print("Анализ продаж продуктов")
                layout = self.verticalLayout_43
                products_from_table = srv.select_from_table(connection, db_products)
                if self.checkBox_2.checkState() == 0:
                    self.clear_layout(layout)

                    production_acc = srv.select_from_table(connection, db_products_accounting)
                    production_acc_list = defaultdict(list)
                    product_id_list = defaultdict(list)

                    for row in production_acc:
                        production_acc_list[row[1]].append([row[2], row[3], float(row[4]), float(row[5])])
                        product_id_list[row[1]].append(row[2])

                    # products_from_table = srv.select_from_table(connection, db_products)
                    product_list = defaultdict(list)

                    for row in products_from_table:
                        product_list[row[0]].append([row[1], float(row[2])])

                    recipe = srv.select_from_table(connection, db_recipe_cost)
                    recipe_list = defaultdict(list)

                    for row in recipe:
                        recipe_list[row[0]].append(row[1])

                    for id in product_id_list:
                        product_id_list[id] = set(product_id_list[id])

                    for index in product_id_list: # 1 2
                        for id in product_id_list[index]:
                            # print(id)
                            if self.comboBox_2.currentText() == recipe_list[index][0]:
                                self.add_checkbox(product_list[id][0][0])
                    # print(production_acc_list)
                    # print(product_list)
                    # print(product_id_list)
                    # print(recipe_list)

                # сюда загрузку графика

            case 4:
                print("4")

            case 5:
                print("Учёт продуктов на изготовление собственной продукции")
                self.fill_combox(db_recipe, self.comboBox_3)
                self.add_tablerow(self.tableWidget_2, db_recipe, self.stackedWidget.currentIndex())

    def insert_data_to_table(self, db_name):
        match db_name:
            case "products_accounting":
                print("тут insert to "+ db_name)
                insert_data = defaultdict(list)
                rows = self.tableWidget_2.rowCount()

                #id продукции
                # insert_data[0] = 0
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                for row in select_data_from_table:
                    if row[1] == self.comboBox_3.currentText():
                        insert_data[0].append(row[0])

                #id продукта
                select_data_from_table = srv.select_from_table(connection, db_products)

                for row_table in range(rows):
                    for row in select_data_from_table:
                        if row[1] == self.tableWidget_2.item(row_table, 0).text():
                            insert_data[1].append(row[0])

                #дата
                insert_data[2] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                #использовано продукта
                for row in range(rows):
                    insert_data[3].append(float(self.tableWidget_2.item(row, 1).text()))

                #цена использованного продукта
                for row_table in range(rows):
                    for row in select_data_from_table:
                        if row[1] == self.tableWidget_2.item(row_table, 0).text():
                            insert_data[4].append((float(self.tableWidget_2.item(row_table, 1).text()) * float(row[2])) / 100)

                # проверяем, что запишется в БД
                # for row in range(len(insert_data[1])):
                #      print(f'{insert_data[0][0]}, {insert_data[1][row]}, {insert_data[2]}, {insert_data[3][row]}, {insert_data[4][row]}')

                # записываем в БД
                srv.insert_into_table(connection, db_name, insert_data)

                self.set_status_bar("сохранить")

            case "sales_accounting":
                print("тут insert to " + db_name)
                insert_data = defaultdict(list)
                rows = self.tableWidget.rowCount()

                # id продукции
                # брать имя из таблицы
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                for row_table in range(rows):
                    for row in select_data_from_table:
                        if row[1] == self.tableWidget.item(row_table, 0).text():
                            insert_data[0].append(row[0])

                # дата
                insert_data[1] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                for row in range(rows):
                    # продаём продукции
                    insert_data[2].append(float(self.tableWidget.item(row, 1).text()))
                    # цена продукции
                    insert_data[3].append(float(self.tableWidget.item(row, 2).text()))

                srv.insert_into_table(connection, db_name, insert_data)
                self.set_status_bar("сохранить")

    def get_graphic(self, data, db_name):
        match db_name:
            case "products_accounting":
                # fig = plot_graphics(file_path, "M01AB")
                # return fig

                # получаем данные и строим по тим график
                # fig = plt.figure()
                fig, ax = plt.subplots()

                # axes.plot()
                date_list = []
                # gram_list = []
                data_list = defaultdict(list)

                for row in data:
                    # выбираем продукцию
                    for id in data[row]:
                        data_list[id[0]].append([[id[1].strftime('%Y-%m-%d')], [float(id[2])]])
                    print("---------------")

                x = ["2023-11-26 00:00:00", "2023-11-27 00:00:00"]
                y = [5.00, 5.00]

                print(data_list)

                df = pd.DataFrame()

                # название продукта по id
                select_data_from_table = srv.select_from_table(connection, db_products)
                product_name = defaultdict(list)

                for row in select_data_from_table:
                    product_name[row[0]].append(row[1])

                for value in data_list:
                    print(value)
                    date_list = []
                    gram_list = []
                    date_gram_list = defaultdict(list)
                    for row in data_list[value]:
                        # print(row[0][0], row[1][0])
                        # print("Проверка" + row[0][0])
                        # print(date_list)
                        if datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date() in date_list:
                            # print("уже есть")
                            for date in date_list:
                                # print(row[0][0] + "=" + date)
                                if datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date() == date:
                                    # print("тут схоже")
                                    # print(date_gram_list[date])
                                    date_gram_list[date][0] += row[1][0]
                        else:
                            d = datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date()
                            date_list.append(d)
                            gram_list.append(row[1][0])
                            date_gram_list[d].append(row[1][0])
                    date_list.sort()

                    # print(date_list)
                    # print(date_gram_list)

                    for id in range(len(date_list)):
                        # print(id)
                        gram_list[id] = date_gram_list[date_list[id]][0]
                    print(date_list)
                    print(gram_list)

                    # mplc.cursor(hover=True)
                    ax.plot(date_list, gram_list, label=product_name[value][0])
                    ax.legend( loc='upper left', prop={'size': 10})
                    ax.scatter(date_list, gram_list, color='green', s=40, marker='o')

                    # plt.plot(date_list, gram_list)


                    # ax = plt.plot(date_list, gram_list)
                    # ax.set_xlabel('Дата')
                    # ax.set_ylabel('Средний объём продаж')
                    #
                    # plt.grid(which='major')
                    # plt.grid(which='minor')
                    print("----")

                # plt.show()
                plt.grid(which='major')
                plt.grid(which='minor')
                print("конец построения графиков для продуктов")

                # self.statusBar.showMessage("График построен")
                # self.statusBar.setStyleSheet("background-color: yellow")

                # axes.plot()
                return fig
            case "sales_accounting":
                print("тут анализ для продукции")

                fig, ax = plt.subplots()
                date_list = []

                data_list = defaultdict(list)

                print(data)
                for row in data:
                    # выбираем продукцию
                    # print(row)
                    for id in data[row]:
                        # print(id)
                        data_list[row].append([[id[0].strftime('%Y-%m-%d')], [float(id[1])]])
                    print("---------------")

                print(data_list)

                # название продукции по id
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                production_name = defaultdict(list)

                for row in select_data_from_table:
                    production_name[row[0]].append(row[1])

                for value in data_list:
                    print(value)
                    date_list = []
                    gram_list = []
                    date_gram_list = defaultdict(list)
                    for row in data_list[value]:
                        if datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date() in date_list:
                            for date in date_list:
                                if datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date() == date:
                                    date_gram_list[date][0] += row[1][0]
                        else:
                            d = datetime.datetime.strptime(row[0][0], '%Y-%m-%d').date()
                            date_list.append(d)
                            gram_list.append(row[1][0])
                            date_gram_list[d].append(row[1][0])
                    date_list.sort()

                    # print(date_list)

                    for id in range(len(date_list)):
                        # print(id)
                        gram_list[id] = date_gram_list[date_list[id]][0]
                    print(date_list)
                    print(gram_list)

                    # mplc.cursor(hover=True)
                    # print(production_name[value][0])

                    ax.plot(date_list, gram_list, label=production_name[value][0])
                    ax.legend(loc='upper left', prop={'size': 10})
                    ax.scatter(date_list, gram_list, color='green', s=40, marker='o')

                    print("----")

                plt.grid(which='major')
                plt.grid(which='minor')
                print("конец построения графиков для продукции")
                return fig


    def prepare_canvas_and_toolbar(self, data, db_name, n):
        match n:
            case 1:
                self.companovka_for_mpl.removeWidget(self.canvas)
                self.canvas.hide()
                self.canvas = MyMplCanvas(self.get_graphic(data, db_name))

                #сначала добавляем тулбар
                self.toolbar.hide()
                self.toolbar = NavigationToolbar(self.canvas, self)
                self.companovka_for_mpl.addWidget(self.toolbar)

                self.companovka_for_mpl.addWidget(self.canvas)
            case 2:
                self.companovka_for_mpl_2.removeWidget(self.canvas_2)
                self.canvas_2.hide()
                self.canvas_2 = MyMplCanvas(self.get_graphic(data, db_name))

                # сначала добавляем тулбар
                self.toolbar_2.hide()
                self.toolbar_2 = NavigationToolbar(self.canvas_2, self)
                self.companovka_for_mpl_2.addWidget(self.toolbar_2)

                self.companovka_for_mpl_2.addWidget(self.canvas_2)

    def get_graphics(self, db_name):
        match db_name:
            case "products_accounting":
                print("тут данные из таблицы " + db_name)
                date = defaultdict(list)
                production_id = defaultdict(list)
                product_id = defaultdict(list)
                data_for_an = defaultdict(list)
                data = defaultdict(list)

                date[0] = self.calendarWidget_5.selectedDate()
                date[1] = self.calendarWidget_6.selectedDate()

                if date[0] > date[1]:
                    self.set_status_bar("дата")
                else:
                    # if self.checkBox_2.checkState() == 2:
                    #     self.clear_layout(self.verticalLayout_43)
                    #     print("показываем все продукты")
                    # if self.checkBox_3.checkState() == 2:
                    #     print("анализируем все продукты без учёта продукции")

                    # if self.checkBox.checkState() == 2:
                    #     print("делаем анализ продуктов без учёта продукции")

                    # чтобы по десять раз не бегать к серверу, запросим сразу все данные
                    # (перенести этот код, что при загрузке страницы делался)

                    ##########################################################################
                    # код повторяется (можно в функцию)
                    # id продукции
                    select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                    for row in select_data_from_table:
                        production_id[row[1]].append(row[0])

                    # id продукта
                    select_data_from_table = srv.select_from_table(connection, db_products)

                    for row in select_data_from_table:
                        product_id[row[1]].append(row[0])
                    ##########################################################################
                    layout = self.verticalLayout_43

                    # if self.checkBox_2.checkState() == 2:
                    #     self.clear_layout(layout)
                    #     for row in select_data_from_table:
                    #         self.add_checkbox(row[1])
                    #     print("показываем все продукты")

                    # соотносим имена продукции с id
                    for name in production_id:
                        # если не указано, то выбираем по выбранной продукции
                        # иначе для всей продукции анализируем
                        if self.checkBox_3.checkState() == 0:
                            print("не для всей")
                            if name == self.comboBox_2.currentText():
                                data_for_an["продукция"].append([name, production_id[name][0]])
                        else:
                            print("для всей")
                            data_for_an["продукция"].append([name, production_id[name][0]])

                    # print(data_for_an)
                    # соотносим имена продуктов с id
                    for row in range(layout.count()):
                        for name in product_id:
                            if layout.itemAt(row).widget().checkState() == 2:
                                if name == layout.itemAt(row).widget().text():
                                    data_for_an["продукты"].append([name, product_id[name][0]])

                    # теперь выбрать данные по дате
                    select_data_from_table = srv.select_from_table(connection, db_name)
                    for row in select_data_from_table:
                        # выбираем строки по id продукции и продукта
                        for production in range(len(data_for_an["продукция"])):
                            for id in range(len(data_for_an["продукты"])):
                                if ((row[1] == data_for_an["продукция"][production][1]) and (row[2] == data_for_an["продукты"][id][1]) and
                                        ((row[3] >= date[0]) and (row[3] <= date[1]))):
                                    data[row[1]].append([row[2], row[3], row[4], row[5]])

                    # print(data)

                    # осталось построить графики по выбранной информации
                    # рисуем наш плот
                    self.prepare_canvas_and_toolbar(data, db_name, 1)
                    self.set_status_bar("анализ")

            case "sales_accounting":
                print("тут данные из таблицы " + db_name)
                date = defaultdict(list)
                production_id = defaultdict(list)
                data_for_an = defaultdict(list)
                data = defaultdict(list)

                date[0] = self.calendarWidget.selectedDate()
                date[1] = self.calendarWidget_2.selectedDate()

                if date[0] > date[1]:
                    self.set_status_bar("дата")
                else:
                    ##########################################################################
                    # код повторяется (можно в функцию)
                    # id продукции
                    select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                    for row in select_data_from_table:
                        production_id[row[1]].append(row[0])
                    ##########################################################################
                    layout = self.verticalLayout_19
                    # соотносим имена продукции с id
                    for row in range(layout.count()):
                        for name in production_id:
                            if name == layout.itemAt(row).widget().currentText():
                                data_for_an["продукция"].append([name, production_id[name][0]])

                    # теперь выбрать данные по дате
                    select_data_from_table = srv.select_from_table(connection, db_name)
                    for row in select_data_from_table:
                        # выбираем строки по id продукции и продукта
                        for id in range(len(data_for_an["продукция"])):
                            if (row[1] == data_for_an["продукция"][id][1]) and ((row[2] >= date[0]) and (row[2] <= date[1])):
                                data[row[1]].append([row[2], row[3], row[4]])

                    print(data)

                    # осталось построить графики по выбранной информации
                    self.prepare_canvas_and_toolbar(data, db_name, 2)

                    self.set_status_bar("анализ")

    def add_tablerow(self, table, db_name, page):
        match page:
            case 2:
                recipe = srv.select_from_table(connection, db_name)
                recipe_cost_list = defaultdict(list)

                for row in recipe:
                    recipe_cost_list[row[1]].append(float(row[2]))

                table.clearContents()
                table.setRowCount(len(self.verticalLayout_6))
                rows = len(self.verticalLayout_6)

                #########################################################################
                # РАБОТАЕТ !!!!!!!!!!!!!!!!!!!!!!!!!!
                # print(self.verticalLayout_6.itemAt(0).widget().currentText())
                #########################################################################
                sum = 0

                name_list = []
                for row in range(rows):
                    name_production = self.verticalLayout_6.itemAt(row).widget().currentText()
                    # print(name_list)
                    if name_production in name_list:
                        # print("1")
                        for row_in_table in range(table.rowCount()):
                            # print("тут запись")
                            # print(row_in_table)
                            if table.item(row_in_table, 0).text() == name_production:
                                print("1")
                            #     table.itemAt(row_in_table, 1).
                            #     float(self.tableWidget.item(row, 2).text())
                                print(row_in_table)
                                # print(float(table.item(0, 1).text()))
                            #     print(table.itemAt(row_in_table, 1).text())
                            #     print(self.verticalLayout_11.itemAt(row).widget().value() + float(table.itemAt(row_in_table, 1).text()))
                            #     gram = self.verticalLayout_11.itemAt(row).widget().value() + float(table.item(row_in_table, 1).text())
                            #     # print("2")
                            # #     # table.setItem(row, 0, QTableWidgetItem(name_production))
                            # #     table.editItem()
                            #     table.itemAt(row_in_table, 1).setText(str(gram))
                            #     # table.setItem(row_in_table, 1, QTableWidgetItem(str(gram)))
                            # if name_production in recipe_cost_list:
                            #     cost = recipe_cost_list[name_production]
                            #     value = (gram * cost[0]) / 100
                            #     # table.setItem(row_in_table, 2, QTableWidgetItem(str(value)))
                            #     table.itemAt(row_in_table, 2).setText(str(value))
                            #     sum = sum + value
                            # print("2")
                    else:
                        name_list.append(name_production)
                        gram = self.verticalLayout_11.itemAt(row).widget().value()
                        table.setItem(row, 0, QTableWidgetItem(name_production))
                        table.setItem(row, 1, QTableWidgetItem(str(gram)))
                        if name_production in recipe_cost_list:
                            cost = recipe_cost_list[name_production]
                            value = (gram * cost[0]) / 100
                            table.setItem(row, 2, QTableWidgetItem(str(value)))
                            sum = sum + value

                    print(name_list)

                self.label_14.setText("СУММА: " + str(sum))
            case 5:
                recipe = srv.select_from_table(connection, db_name)
                recipe_list = defaultdict(list)

                for row in recipe:
                    recipe_list[row[1]].append([row[2], float(row[3])])

                table.clearContents()

                ####################################################################################
                # получаем всю информацию из таблицы рецепты
                select_data_from_table = srv.select_from_table(connection, db_recipe_cost)
                select_production = defaultdict(list)

                # составляем отдельный список id
                for row in select_data_from_table:
                    select_production[row[0]].append(row[1])

                name = self.comboBox_3.currentText()
                product = srv.select_from_table(connection, db_products)
                product_list = defaultdict(list)

                for row in product:
                    product_list[row[0]].append([row[1], float(row[2])])

                text_of_recipe = "Тут рецепт на 100 грамм продукции"

                # 100 грамм - одна порция
                for id in recipe_list.keys():
                    if name == select_production[id][0]:
                        text_of_recipe = f'{text_of_recipe}\n ------<{name}>------'
                        table.setRowCount(len(recipe_list[id]))
                        for row in range(len(recipe_list[id])):
                            product_name = str(product_list[recipe_list[id][row][0]][0][0])
                            table.setItem(row, 0, QTableWidgetItem(product_name))
                            text_of_recipe = f'{text_of_recipe} \n {product_name} - '
                            gram_of_product = recipe_list[id][row][1]
                            value = (gram_of_product * self.spinBox_3.value()) / 100
                            text_of_recipe = f'{text_of_recipe}{ceil(recipe_list[id][row][1])} гр.\n'
                            table.setItem(row, 1, QTableWidgetItem(str(ceil(value))) )
                self.textEdit.setText(text_of_recipe)

    def fill_combox(self, db_name, combox):
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


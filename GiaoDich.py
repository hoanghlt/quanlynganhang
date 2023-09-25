import mysql.connector
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mysql.connector import Error
from SqlHelper import close_db_connection, create_db_connection

# Sử dụng trong ứng dụng:
# some_object = SomeClass()
# some_object.perform_database_operation()
# some_object.close_connection()

class ThemGiaoDich(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(ThemGiaoDich, self).__init__()
        uic.loadUi('UI/ThemGiaoDich.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_save_button)
        self.pushButton_2.clicked.connect(self.on_click_cancel_button)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)

        self.textEdit_3.setDisabled(False)
        self.textEdit_4.setDisabled(True)

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            if self.comboBox.currentText() == "Khách hàng cá nhân":
                res = mycursor.callproc("TaoMaGDCN", [0, ])
            else:
                res = mycursor.callproc("TaoMaGDTCDN", [0, ])
            self.textEdit.setPlainText(str(res[0]))            
            close_db_connection(mycursor)        

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.textEdit_3.setDisabled(False)
            self.textEdit_4.setDisabled(True)

            self.textEdit_4.clear()
        else:
            self.textEdit_4.setDisabled(False)
            self.textEdit_3.setDisabled(True)

            self.textEdit_3.clear()

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            if self.comboBox.currentText() == "Khách hàng cá nhân":
                res = mycursor.callproc("TaoMaGDCN", [0, ])
            else:
                res = mycursor.callproc("TaoMaGDTCDN", [0, ])
            self.textEdit.setPlainText(str(res[0]))

            close_db_connection(mycursor)        

    def on_click_save_button(self):
        try:
            ma_gd = self.textEdit.toPlainText().rstrip()
            loai_gd = self.textEdit_2.toPlainText().rstrip()
            ma_tktd = self.textEdit_3.toPlainText().rstrip()
            ma_tkgt = self.textEdit_4.toPlainText().rstrip()
            ma_tkvt = self.textEdit_5.toPlainText().rstrip()
            phuong_thuc = self.textEdit_6.toPlainText().rstrip()
            ma_kh = self.textEdit_7.toPlainText().rstrip()
            so_tien = self.textEdit_8.toPlainText().rstrip()
            ma_nv = self.textEdit_9.toPlainText().rstrip()

            if self.comboBox.currentText() == "Khách hàng cá nhân":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemGiaoDichCaNhan",
                                    [ma_gd, so_tien, loai_gd, phuong_thuc, ma_kh, ma_tktd, ma_tkgt, ma_nv, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)
            else:
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemGiaoDichToChucDoanhNghiep",
                                    [ma_gd, so_tien, loai_gd, phuong_thuc, ma_kh, ma_tkgt, ma_tkvt, ma_nv, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Thêm thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()

    def on_click_cancel_button(self):
        self.close()

class TimKiemGiaoDich(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(TimKiemGiaoDich, self).__init__()
        uic.loadUi('UI/TimKiemGiaoDich.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_search_button)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.tableWidget.setHorizontalHeaderLabels(
                ["Mã giao dịch", "Số tiền", "Loại giao dịch", "Phương thức", "Thời gian", "Mã KHCN", "Mã TKTD", "Mã TKGT", "Mã NV"])
        else:
            self.tableWidget.setHorizontalHeaderLabels(
                ["Mã giao dịch", "Số tiền", "Loại giao dịch", "Phương thức", "Thời gian", "Mã KHCN", "Mã TKGT", "Mã TKVT", "Mã NV"])

        self.on_click_search_button()

    def on_click_search_button(self):
        try:
            ma_gd = self.textEdit.toPlainText().rstrip()
            ma_tk = self.textEdit_2.toPlainText().rstrip()
            ma_kh = self.textEdit_3.toPlainText().rstrip()
            ma_nv = self.textEdit_3.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()

                if self.comboBox.currentText() == "Khách hàng cá nhân":
                    mycursor.callproc("TimKiemGiaoDichCaNhan", [ma_gd, ma_kh, ma_nv, ma_tk, ])
                else:
                    mycursor.callproc("TimKiemGiaoDichToChucDoanhNghiep", [ma_gd, ma_kh, ma_nv, ma_tk, ])

                myresult = mycursor.stored_results()

                self.tableWidget.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)

                        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))
                        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(x[2])))
                        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[3])))
                        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[4])))
                        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(str(x[5])))
                        self.tableWidget.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(str(x[6])))
                        self.tableWidget.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(str(x[7])))
                        self.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem(str(x[8])))

                        self.tableWidget.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 2).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 3).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 4).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 5).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 6).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 7).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 8).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    
                close_db_connection(mycursor)

        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()




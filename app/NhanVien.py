from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView
import sys
import mysql.connector
from mysql.connector import Error
from data.SqlHelper import create_db_connection, close_db_connection
from common import common

class ThemNhanVien(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(ThemNhanVien, self).__init__()
        uic.loadUi('ui/ThemNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_save_button)
        self.pushButton_2.clicked.connect(self.on_click_cancel_button)

        if self.db_connection:
            mycursor = self.db_connection.cursor()
            res = mycursor.callproc("TaoMaNV", [0, ])            
            self.textEdit.setPlainText(str(res[0]))
            self.textEdit.setDisabled(True)
            close_db_connection(mycursor)

        self.show()

    def on_click_save_button(self):
        try:
            ma_nv = self.textEdit.toPlainText().rstrip()
            ten_nhan_vien = self.textEdit_2.toPlainText().rstrip()
            dia_chi = self.textEdit_3.toPlainText().rstrip()
            sdt = self.textEdit_4.toPlainText().rstrip()
            cap_bac = self.textEdit_5.toPlainText().rstrip()
            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("ThemNhanVien", [ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
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


class SuaNhanVien(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(SuaNhanVien, self).__init__()
        uic.loadUi('ui/SuaNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_save_button)
        self.pushButton_2.clicked.connect(self.on_click_delete_button)
        self.pushButton_3.clicked.connect(self.on_click_cancel_button)

        self.openDialog = None

        self.show()

    def on_click_save_button(self):
        try:
            ma_nv = self.textEdit.toPlainText().rstrip()
            ten_nhan_vien = self.textEdit_2.toPlainText().rstrip()
            dia_chi = self.textEdit_3.toPlainText().rstrip()
            sdt = self.textEdit_4.toPlainText().rstrip()
            cap_bac = self.textEdit_5.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("SuaNhanVien", [ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
                self.db_connection.commit()                
                close_db_connection(mycursor)
                
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Sửa thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()
        self.openDialog.on_click_search_button()

    def on_click_delete_button(self):
        try:
            ma_nv = self.textEdit.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("XoaNhanVien", [ma_nv, ])
                self.db_connection.commit()
                close_db_connection(mycursor)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thông báo")
            msg.setText("Xoá thành công")
            msg.exec_()
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

        self.close()
        self.openDialog.on_click_search_button()

    def on_click_cancel_button(self):
        self.close()


class TimKiemNhanVien(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(TimKiemNhanVien, self).__init__()
        uic.loadUi('ui/TimKiemNhanVien.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_search_button)
        self.tableWidget.clicked.connect(self.on_click_table)

        self.show()

    def on_click_search_button(self):
        try:
            ma_nv = self.textEdit.toPlainText().rstrip()
            ten_nhan_vien = self.textEdit_2.toPlainText().rstrip()
            dia_chi = self.textEdit_3.toPlainText().rstrip()
            sdt = self.textEdit_4.toPlainText().rstrip()
            cap_bac = self.textEdit_5.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()
                mycursor.callproc("TimKiemNhanVien", [ma_nv, ten_nhan_vien, dia_chi, cap_bac, sdt, ])
                myresult = mycursor.stored_results()
                self.tableWidget.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)

                        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))
                        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(x[2])))
                        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[5])))
                        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[3])))

                        self.tableWidget.item(rowPosition, 0).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableWidget.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                close_db_connection(mycursor)
            
            common.autosizeColumns(self.tableWidget)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

    def on_click_table(self, item):
        dialog = SuaNhanVien()
        dialog.openDialog = self

        dialog.textEdit.setPlainText(self.tableWidget.item(item.row(), 0).text())
        dialog.textEdit_2.setPlainText(self.tableWidget.item(item.row(), 1).text())
        dialog.textEdit_3.setPlainText(self.tableWidget.item(item.row(), 2).text())
        dialog.textEdit_4.setPlainText(self.tableWidget.item(item.row(), 3).text())
        dialog.textEdit_5.setPlainText(self.tableWidget.item(item.row(), 4).text())

        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TimKiemNhanVien()
    app.exec_()

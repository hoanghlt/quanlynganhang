import mysql.connector
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView
from mysql.connector import Error
from data.SqlHelper import close_db_connection, create_db_connection
from common import common

# Sử dụng trong ứng dụng:
# some_object = SomeClass()
# some_object.perform_database_operation()
# some_object.close_connection()


class ThemGiaoDich(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()
        super(ThemGiaoDich, self).__init__()
        uic.loadUi('ui/ThemGiaoDich.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Save.clicked.connect(self.on_click_save_button)
        self.btn_Huy.clicked.connect(self.on_click_cancel_button)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)

        self.txt_MaTKTD.setDisabled(False)
        self.txt_MaTKVT.setDisabled(True)

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                res = mycursor.callproc("TaoMaGDCN", [0, ])
            else:
                res = mycursor.callproc("TaoMaGDTCDN", [0, ])
            self.txt_MaGD.setPlainText(str(res[0]))
            self.txt_MaGD.setDisabled(True)
            close_db_connection(mycursor)
            self.db_connection.close()

        self.show()

    def on_combobox_changed(self, value):
        self.db_connection = create_db_connection()
        if value == "Khách hàng cá nhân":
            self.txt_MaTKTD.setDisabled(False)
            self.txt_MaTKVT.setDisabled(True)

            self.txt_MaTKVT.clear()
        else:
            self.txt_MaTKVT.setDisabled(False)
            self.txt_MaTKTD.setDisabled(True)

            self.txt_MaTKTD.clear()

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                res = mycursor.callproc("TaoMaGDCN", [0, ])
            else:
                res = mycursor.callproc("TaoMaGDTCDN", [0, ])
            self.txt_MaGD.setPlainText(str(res[0]))

            close_db_connection(mycursor)
            self.db_connection.close()

    def on_click_save_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_gd = self.txt_MaGD.toPlainText().rstrip()
            loai_gd = self.txt_LoaiGD.toPlainText().rstrip()
            ma_tktd = self.txt_MaTKTD.toPlainText().rstrip()
            ma_tkgt = self.txt_MaTKGT.toPlainText().rstrip()
            ma_tkvt = self.txt_MaTKVT.toPlainText().rstrip()
            phuong_thuc = self.txt_PhuongThuc.toPlainText().rstrip()
            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            so_tien = self.txt_SoTien.toPlainText().rstrip()
            ma_nv = self.txt_MaNV.toPlainText().rstrip()

            if (ma_tktd != "" and ma_tkgt != "") or (ma_tkvt != "" and ma_tkgt != ""):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Thông báo")
                msg.setText("Mỗi giao dịch chỉ có 1 thông tin tài khoản!")
                msg.exec_()
                self.close()

            if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemGiaoDichCaNhan",
                                      [ma_gd, so_tien, loai_gd, phuong_thuc, ma_kh, ma_tktd, ma_tkgt, ma_nv, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)
                    self.db_connection.close()
            else:
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemGiaoDichToChucDoanhNghiep",
                                      [ma_gd, so_tien, loai_gd, phuong_thuc, ma_kh, ma_tkgt, ma_tkvt, ma_nv, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)
                    self.db_connection.close()

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
        super(TimKiemGiaoDich, self).__init__()
        uic.loadUi('ui/TimKiemGiaoDich.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.btn_Search.clicked.connect(self.on_click_search_button)
        self.cbx_TypeKH.currentTextChanged.connect(self.on_combobox_changed)

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.tb_Result.setHorizontalHeaderLabels(
                ["Mã giao dịch", "Số tiền", "Loại giao dịch", "Phương thức", "Thời gian", "Mã KHCN", "Mã TKTD", "Mã TKGT", "Mã NV"])
        else:
            self.tb_Result.setHorizontalHeaderLabels(
                ["Mã giao dịch", "Số tiền", "Loại giao dịch", "Phương thức", "Thời gian", "Mã KHCN", "Mã TKGT", "Mã TKVT", "Mã NV"])

        self.on_click_search_button()

    def on_click_search_button(self):
        try:
            self.db_connection = create_db_connection()

            ma_gd = self.txt_MaGD.toPlainText().rstrip()
            ma_tk = self.txt_MaTK.toPlainText().rstrip()
            ma_kh = self.txt_MaKH.toPlainText().rstrip()
            ma_nv = self.txt_MaNV.toPlainText().rstrip()

            if self.db_connection:
                mycursor = self.db_connection.cursor()

                if self.cbx_TypeKH.currentText() == "Khách hàng cá nhân":
                    mycursor.callproc("TimKiemGiaoDichCaNhan", [
                                      ma_gd, ma_kh, ma_nv, ma_tk, ])
                else:
                    mycursor.callproc("TimKiemGiaoDichToChucDoanhNghiep", [
                                      ma_gd, ma_kh, ma_nv, ma_tk, ])

                myresult = mycursor.stored_results()

                self.tb_Result.setRowCount(0)

                for m in myresult:
                    for x in m.fetchall():
                        rowPosition = self.tb_Result.rowCount()
                        self.tb_Result.insertRow(rowPosition)

                        self.tb_Result.setItem(
                            rowPosition, 0, QtWidgets.QTableWidgetItem(str(x[0])))
                        self.tb_Result.setItem(
                            rowPosition, 1, QtWidgets.QTableWidgetItem(str(x[1])))
                        self.tb_Result.setItem(
                            rowPosition, 2, QtWidgets.QTableWidgetItem(str(x[2])))
                        self.tb_Result.setItem(
                            rowPosition, 3, QtWidgets.QTableWidgetItem(str(x[3])))
                        self.tb_Result.setItem(
                            rowPosition, 4, QtWidgets.QTableWidgetItem(str(x[4])))
                        self.tb_Result.setItem(
                            rowPosition, 5, QtWidgets.QTableWidgetItem(str(x[5])))
                        self.tb_Result.setItem(
                            rowPosition, 6, QtWidgets.QTableWidgetItem(str(x[6])))
                        self.tb_Result.setItem(
                            rowPosition, 7, QtWidgets.QTableWidgetItem(str(x[7])))
                        self.tb_Result.setItem(
                            rowPosition, 8, QtWidgets.QTableWidgetItem(str(x[8])))

                        self.tb_Result.item(rowPosition, 0).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 1).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 2).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 3).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 4).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 5).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 6).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 7).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tb_Result.item(rowPosition, 8).setTextAlignment(
                            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

                close_db_connection(mycursor)
                self.db_connection.close()

            common.autosizeColumns(self.tb_Result)
            self.tb_Result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi")
            msg.setText(e.msg)
            msg.exec_()

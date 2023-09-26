from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mysql.connector import Error
from data.SqlHelper import close_db_connection, create_db_connection

class ThemTaiKhoan(QtWidgets.QDialog):
    def __init__(self):   
        self.db_connection = create_db_connection()     
        super(ThemTaiKhoan, self).__init__()
        uic.loadUi('ui/ThemTaiKhoan.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_save_button)
        self.pushButton_2.clicked.connect(self.on_click_cancel_button)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.comboBox_2.currentTextChanged.connect(self.on_combobox_changed2)

        if self.db_connection:
            mycursor = self.db_connection.cursor()

            res = mycursor.callproc("TaoMaTK", [0, ])
            self.textEdit.setPlainText(str(res[0]))
            self.textEdit.setDisabled(True)
            close_db_connection(mycursor)  

        self.textEdit_3.setDisabled(False)
        self.textEdit_6.setDisabled(False)
        self.textEdit_4.setDisabled(True)
        self.textEdit_5.setDisabled(True)

        self.textEdit_4.clear()
        self.textEdit_5.clear()

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.comboBox_2.clear()
            self.comboBox_2.addItem("Tài khoản tín dụng")
            self.comboBox_2.addItem("Tài khoản gửi tiền")

            self.comboBox_2.setCurrentText("Tài khoản tín dụng")
        else:
            self.comboBox_2.clear()
            self.comboBox_2.addItem("Tài khoản gửi tiền")
            self.comboBox_2.addItem("Tài khoản vay tiền")

            self.comboBox_2.setCurrentText("Tài khoản gửi tiền")

        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.textEdit_6.clear()

    def on_combobox_changed2(self, value):
        if value == "Tài khoản tín dụng":
            self.textEdit_3.setDisabled(False)
            self.textEdit_6.setDisabled(False)
            self.textEdit_4.setDisabled(True)
            self.textEdit_5.setDisabled(True)

            self.textEdit_4.clear()
            self.textEdit_5.clear()

        if value == "Tài khoản gửi tiền":
            self.textEdit_4.setDisabled(False)
            self.textEdit_5.setDisabled(False)
            self.textEdit_3.setDisabled(True)
            self.textEdit_6.setDisabled(True)

            self.textEdit_3.clear()
            self.textEdit_6.clear()

        if value == "Tài khoản vay tiền":
            self.textEdit_4.setDisabled(False)
            self.textEdit_6.setDisabled(False)
            self.textEdit_3.setDisabled(True)
            self.textEdit_5.setDisabled(True)

            self.textEdit_3.clear()
            self.textEdit_5.clear()

    def on_click_save_button(self):
        try:
            ma_tk = self.textEdit.toPlainText().rstrip()
            hang_tk = self.textEdit_2.toPlainText().rstrip()
            han_muc = self.textEdit_3.toPlainText().rstrip()
            lai_suat = self.textEdit_4.toPlainText().rstrip()
            so_du = self.textEdit_5.toPlainText().rstrip()
            so_no = self.textEdit_6.toPlainText().rstrip()
            ma_kh = self.textEdit_7.toPlainText().rstrip()
            ma_nv = self.textEdit_8.toPlainText().rstrip()

            if self.comboBox_2.currentText() == "Tài khoản tín dụng":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemTaiKhoanTinDung", [ma_kh, ma_nv, ma_tk, hang_tk, han_muc, so_no, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)

            if self.comboBox_2.currentText() == "Tài khoản vay tiền":
                if self.db_connection:
                    mycursor = self.db_connection.cursor()

                    mycursor.callproc("ThemTaiKhoanVayTien", [ma_kh, ma_nv, ma_tk, hang_tk, lai_suat, so_no, ])

                    self.db_connection.commit()
                    close_db_connection(mycursor)

            if self.comboBox_2.currentText() == "Tài khoản gửi tiền":
                if self.comboBox.currentText() == "Khách hàng cá nhân":
                    if self.db_connection:
                        mycursor = self.db_connection.cursor()

                        mycursor.callproc("ThemTaiKhoanGuiTienCaNhan", [ma_kh, ma_nv, ma_tk, hang_tk, so_du, lai_suat, ])

                        self.db_connection.commit()
                        close_db_connection(mycursor)
                else:
                    if self.db_connection:
                        mycursor = self.db_connection.cursor()

                        mycursor.callproc("ThemTaiKhoanGuiTienToChucDoanhNghiep",
                                        [ma_kh, ma_nv, ma_tk, hang_tk, so_du, lai_suat, ])

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


class TimKiemTaiKhoan(QtWidgets.QDialog):
    def __init__(self):
        self.db_connection = create_db_connection()     
        super(TimKiemTaiKhoan, self).__init__()
        uic.loadUi('ui/TimKiemTaiKhoan.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))

        self.pushButton.clicked.connect(self.on_click_search_button)
        self.tableWidget.clicked.connect(self.on_click_table)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.comboBox_2.currentTextChanged.connect(self.on_combobox_changed2)

        self.show()

    def on_combobox_changed(self, value):
        if value == "Khách hàng cá nhân":
            self.comboBox_2.clear()
            self.comboBox_2.addItem("Tài khoản tín dụng")
            self.comboBox_2.addItem("Tài khoản gửi tiền")

            self.comboBox_2.setCurrentText("Tài khoản tín dụng")
        else:
            self.comboBox_2.clear()
            self.comboBox_2.addItem("Tài khoản gửi tiền")
            self.comboBox_2.addItem("Tài khoản vay tiền")

            self.comboBox_2.setCurrentText("Tài khoản gửi tiền")

        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.textEdit_6.clear()
        self.on_click_search_button()

    def on_combobox_changed2(self, value):
        if value == "Tài khoản tín dụng":
            self.textEdit_3.setDisabled(False)
            self.textEdit_6.setDisabled(False)
            self.textEdit_4.setDisabled(True)
            self.textEdit_5.setDisabled(True)

            self.textEdit_4.clear()
            self.textEdit_5.clear()

        if value == "Tài khoản gửi tiền":
            self.textEdit_4.setDisabled(True)
            self.textEdit_5.setDisabled(True)
            self.textEdit_3.setDisabled(False)
            self.textEdit_6.setDisabled(False)

            self.textEdit_3.clear()
            self.textEdit_6.clear()

        if value == "Tài khoản vay tiền":
            self.textEdit_4.setDisabled(True)
            self.textEdit_6.setDisabled(True)
            self.textEdit_3.setDisabled(False)
            self.textEdit_5.setDisabled(False)

            self.textEdit_3.clear()
            self.textEdit_5.clear()

        self.on_click_search_button()


import sys

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

import GiaoDich
import KhachHang
import NhanVien
import TaiKhoan
import TruyVan


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('UI/MainMenu.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('assets/icon/icon.png'))

        self.action_add_staff.setIcon(QtGui.QIcon('assets/icon/staff.png'))
        self.action_search_staff.setIcon(
            QtGui.QIcon('assets/icon/searchstaff.png'))
        self.action_payroll.setIcon(QtGui.QIcon('assets/icon/salary.png'))
        self.action_add_customer.setIcon(
            QtGui.QIcon('assets/icon/customer.png'))
        self.action_search_customer.setIcon(
            QtGui.QIcon('assets/icon/searchcutomer.png'))
        self.action_create_account.setIcon(
            QtGui.QIcon('assets/icon/addaccount.png'))
        self.action_create_transaction.setIcon(
            QtGui.QIcon('assets/icon/transaction.png'))
        self.action_search_transaction.setIcon(
            QtGui.QIcon('assets/icon/searchtransaction.png'))
        self.action_report_ntd.setIcon(QtGui.QIcon('assets/icon/report.png'))
        self.action_report_total.setIcon(QtGui.QIcon('assets/icon/result.png'))
        self.action_report_td.setIcon(QtGui.QIcon('assets/icon/report2.png'))

        self.action_add_staff.triggered.connect(self.open_add_staff)
        self.action_search_staff.triggered.connect(self.open_search_staff)
        self.QS_Body.showFullScreen()

        self.show()

    def show_child(self, child_window, title):
        # Tạo QVBoxLayout để chứa UI con
        layout = QVBoxLayout()
        layout.addWidget(child_window)

        # Tạo QWidget để chứa QVBoxLayout
        container = QWidget()
        container.setLayout(layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Thêm container vào QScrollArea
        self.QS_Body.setWidget(container)
        self.QS_Body.setWindowTitle(title)
        self.QS_Body.showFullScreen()

    def open_add_staff(self):
        child_window = NhanVien.ThemNhanVien()
        title = "Nhân viên"
        self.show_child(child_window, title)

    def open_search_staff(self):
        child_window = NhanVien.TimKiemNhanVien()
        title = "Tìm kiếm nhân viên"
        self.show_child(child_window, title)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

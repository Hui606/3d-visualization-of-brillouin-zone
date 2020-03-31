
from PyQt5 import QtCore
from prance.util import fs
import pyvista as pv
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QCheckBox, QWidgetAction, QMainWindow


class ZoneSwitch(QtWidgets.QMainWindow):

    def __init__(self, main_window):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint);
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowTitleHint)
        # enable custom window hint
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        #
        # # disable (but not hide) close button
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setStyleSheet("QMainWindow {background: 'yellow';}");


        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # self.setStyleSheet("QMainWindow {background:transparent;}")

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        self.window_layout = QtWidgets.QVBoxLayout()
        wid.setLayout(self.window_layout)

        # self.setWindowOpacity(0.1)


        self.title = 'Zone Switch'

        self.main_win = main_window

        self.initUI()



    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedWidth(100)

        for layer_num in sorted(self.main_win.layer_dict.keys()):

            # add_layer_action = QtWidgets.QAction('Layer ' + str(layer_num), self, checkable=True, checked=True)
            # add_layer_action.triggered.connect(self.main_win.layer_box_is_checked)
            # self.main_win.layer_menu.addAction(add_layer_action)


            checkBox = QCheckBox('Zone ' + str(layer_num+1))
            checkBox.stateChanged.connect(self.main_win.layer_box_is_checked)
            checkBox.setChecked(True)
            self.window_layout.addWidget(checkBox)
            # self.main_win.layer_menu.addAction(self.add_layer_action_qwa)

        # self.setLayout(self.window_layout)
        # self.show()
    # def closeEvent(self, QCloseEvent):
    #     self.close()
    #
    #     if self.txt_win is not None:
    #         self.txt_win.close()
    #     else:
    #         pass
    #
    #     if self.layer_switch is not None:
    #         self.layer_switch.close()
    #     else:
    #         pass
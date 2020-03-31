from PyQt5 import QtCore
import pyvista as pv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox


class ZoneSwitch(QtWidgets.QMainWindow):

    def __init__(self, main_window):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        self.window_layout = QtWidgets.QVBoxLayout()
        wid.setLayout(self.window_layout)

        self.title = 'Zone Switch'

        self.main_win = main_window

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedWidth(100)

        for zone_num in sorted(self.main_win.zone_dict.keys()):

            # note the zone number start from 1, not 0
            checkBox = QCheckBox('Zone ' + str(zone_num+1))
            checkBox.stateChanged.connect(self.main_win.zone_box_is_checked)
            checkBox.setChecked(True)
            self.window_layout.addWidget(checkBox)

import sys
import pyvista as pv
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, QPoint, QTimer
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QLabel
import input_data
import file_operation as op
from zone_switch_window import ZoneSwitch


folder_path = input_data.folder_path


class MainWindow(QtWidgets.QMainWindow):

    center = input_data.ball_center  # User input ball center
    center_sphere_actor = None
    poly_actor_list = []
    layer_dict = {}
    txt_win = None  # For user to input the name of image
    gif_name_win = None  # For user to input the name of gif
    zone_switch = None  #

    # options_menu_open = False

    # 1. 实现screenshot
    # 2. context menu

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)
        # super(MainWindow, self).__init__(parent)

        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # create the frame

        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.vtk_widget = pv.QtInteractor(self.frame)
        vlayout.addWidget(self.vtk_widget)

        self.frame.setLayout(vlayout)

        self.setCentralWidget(self.frame)



        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # 开场直接画出polyhedron
        self.add_polyhedron()

        # self.vtk_widget.updateGeometry()
        # menu button for screenshots
        meshMenu = mainMenu.addMenu('Screenshots')
        self.add_screenshots_action = QtWidgets.QAction('Print screen', self)
        self.add_screenshots_action.triggered.connect(self.print_screen)
        meshMenu.addAction(self.add_screenshots_action)

        # menu button for hide/show layers
        layer_menu = mainMenu.addMenu('Brillouin Zone')
        zone_switch_action = QtWidgets.QAction('Zone Switch', self, checkable=True, checked=True)
        layer_menu.addAction(zone_switch_action)
        zone_switch_action.triggered.connect(self.zone_switch_is_clicked)

        gif_menu = mainMenu.addMenu('Orbit GIF')
        gif_action_x = QtWidgets.QAction('Around X-Axis', self)
        gif_action_y = QtWidgets.QAction('Around Y-Axis', self)
        gif_action_z = QtWidgets.QAction('Around Z-Axis', self)
        gif_menu.addAction(gif_action_x)
        gif_menu.addAction(gif_action_y)
        gif_menu.addAction(gif_action_z)
        gif_action_x.triggered.connect(self.gif_is_clicked)
        gif_action_y.triggered.connect(self.gif_is_clicked)
        gif_action_z.triggered.connect(self.gif_is_clicked)

        growing_menu = mainMenu.addMenu('Growing Ball GIF')
        growing_action = QtWidgets.QAction('Start recording', self)
        growing_menu.addAction(growing_action)
        growing_action.triggered.connect(self.growing_action_is_clicked)

        axis_view_menu = mainMenu.addMenu('Axis View')
        axis_view_action_x = QtWidgets.QAction('X-Axis', self)
        axis_view_action_y = QtWidgets.QAction('Y-Axis', self)
        axis_view_action_z = QtWidgets.QAction('Z-Axis', self)
        axis_view_menu.addAction(axis_view_action_x)
        axis_view_menu.addAction(axis_view_action_y)
        axis_view_menu.addAction(axis_view_action_z)
        axis_view_action_x.triggered.connect(self.axis_view_is_clicked)
        axis_view_action_y.triggered.connect(self.axis_view_is_clicked)
        axis_view_action_z.triggered.connect(self.axis_view_is_clicked)

        self.zone_switch = ZoneSwitch(self)

        self.vtk_widget.background_color = "white"

        self.radius_recorder = 0

        if show:
            self.show()
            self.zone_switch.show()

    # def eventFilter(self, obj, event):
    #     if event.type() == QtCore.QEvent.MouseButtonRelease:
    #         self.options_menu_open = True if obj is self.layer_menu else False
    #
    #         # self.__options_menu_pos_cache = event.globalPos()
    #         # self.options_menu.popup(event.globalPos())
    #         return True
    #
    #     return False

    def growing_action_is_clicked(self):
        self.gif_name_win = TextWindow(self, "growing_ball")

    def save_growing_ball_gif(self,image_name):
        # Open a gif
        self.vtk_widget.open_gif(folder_path + image_name + ".gif")

        # Update Z and write a frame for each updated position
        nframe = 100
        max_radius = 10
        for f in range(nframe):
            if self.center_sphere_actor is not None:
                self.vtk_widget.remove_actor(self.center_sphere_actor)

            upd_radius = f * max_radius / nframe + self.radius_recorder

            if upd_radius >= max_radius:
                break

            center_sphere = pv.Sphere(upd_radius, self.center, phi_resolution=100, theta_resolution=100)

            self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                                reset_camera=False)
            self.vtk_widget.write_frame()

        self.vtk_widget.remove_actor(self.center_sphere_actor)  # Recover the deflated ball
        center_sphere = pv.Sphere(self.radius_recorder, self.center, phi_resolution=100, theta_resolution=100)
        self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                            reset_camera=False)


    def axis_view_is_clicked(self):
        action = self.sender()
        action_text = action.text().split('-')[0]
        if action_text == 'X':
            self.vtk_widget.view_yz()
        elif action_text == 'Y':
            self.vtk_widget.view_xz()
        elif action_text == 'Z':
            self.vtk_widget.view_xy()

    def gif_is_clicked(self):
        # 首先生成对话框要求输入名称
        # global view_up
        action = self.sender()

        action_text = action.text().split()[1]

        if action_text == 'X-Axis':
            view_up = [1, 0, 0]
        elif action_text == 'Y-Axis':
            view_up = [0, 1, 0]
        elif action_text == 'Z-Axis':
            view_up = [0, 0, 1]

        self.gif_name_win = TextWindow(self, "gif", view_up)

    def save_gif(self, gif_name, view_up):

        path = self.vtk_widget.generate_orbital_path(n_points=50, viewup=view_up)
        self.vtk_widget.open_gif(folder_path + gif_name + ".gif")
        self.vtk_widget.orbit_on_path(path, write_frames=True, viewup=view_up)

    def zone_switch_is_clicked(self, state):

        # action = self.sender()
        if not state:
            self.zone_switch.setWindowOpacity(0)
        else:
            self.zone_switch.setWindowOpacity(1)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)

    def closeEvent(self, QCloseEvent):
        self.close()

        if self.txt_win is not None:
            self.txt_win.close()
        else:
            pass

        if self.zone_switch is not None:
            self.zone_switch.close()
        else:
            pass

        if self.gif_name_win is not None:
            self.gif_name_win.close()
        else:
            pass

    def print_screen(self):
        # 想用户索取截图名称
        self.init_textbox()

    def save_screenshots(self, image_name):
        self.txt_win.update()
        self.vtk_widget.screenshot(folder_path + image_name)

    def init_textbox(self):
        # print("Here")

        self.txt_win = TextWindow(self, "screenshots")
        # self.txt_win.show()

    def add_polyhedron(self):

        polyhedron_data_list = op.open_folder(folder_path)

        for phd in polyhedron_data_list:
            poly_actor = self.vtk_widget.add_mesh(phd.get_grid(), opacity=1, color=phd.get_color())
            self.poly_actor_list.append(poly_actor)

            layer = phd.get_layer()

            if layer in self.layer_dict.keys():
                self.layer_dict[layer].append((poly_actor, poly_actor.GetProperty().GetOpacity()))  # 找到它所在的层的list，把它加进去
            else:
                self.layer_dict[layer] = []  # 找不到的话就创建这个键值对，然后加进去
                self.layer_dict[layer].append((poly_actor, poly_actor.GetProperty().GetOpacity()))

        # 加入球和它的slider
        self.vtk_widget.add_slider_widget(self.create_center_sphere, [0.1, 15], 0.1, title='Radius', color="b")

    def create_center_sphere(self, radius, sphere_center=center):

        self.radius_recorder = radius

        if self.center_sphere_actor is not None:
            self.vtk_widget.remove_actor(self.center_sphere_actor)

        center_sphere = pv.Sphere(radius, sphere_center, phi_resolution=100, theta_resolution=100)

        self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                            reset_camera=False)

    def layer_box_is_checked(self, state):
        action = self.sender()
        num = int(action.text().split()[1]) - 1

        if state:
            self.layer_visible(num)

        else:
            self.layer_invisible(num)

    def layer_invisible(self, layer_index):

        for pair in self.layer_dict[layer_index]:
            pair[0].GetProperty().SetOpacity(0)
            self.vtk_widget.update()  # 如果没有这个update，就必须点一下屏幕才会更新

    def layer_visible(self, layer_index):
        # print(layer_index)
        for pair in self.layer_dict[layer_index]:
            pair[0].GetProperty().SetOpacity(pair[1])  # 恢复其原来的 opacity
            self.vtk_widget.update()
        # print('success')

    def find_screen_center(self):
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry(-1)
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        return QPoint(x, y)


'''还有一个是命名的时候有一些关键字不能让其含有，例如"/" '''


class TextWindow(QtWidgets.QMainWindow):

    def __init__(self, main_window, target="screenshots", view_up=[]):
        super().__init__()

        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.target = target
        self.view_up = view_up
        self.initUI()
        self.main_win = main_window

    def initUI(self):
        self.title = 'Input name for saved image' if self.target == "screenshots" else 'Input name for saved GIF'
        # self.title = 'Input name for saved image' if

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        # Create button 1 in the window
        self.button_ok = QPushButton('OK', self)
        self.button_ok.move(30, 80)

        # connect button to function on_click
        self.button_ok.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        image_name = self.textbox.text()
        # print(folder_path+image_name)
        # 此处对filename和imagename的检测还要改，中间那个fs尚不清楚是否有效，而最后一个则是为了防止名字里带'/'，macOS命名唯一不允许的符号
        # fs.is_pathname_valid(folder_path+"/"+image_name) and image_name.find("/") is False
        # print(image_name.find("/"))
        # print('/' in image_name)
        if image_name is not "" and bool('/' in image_name) is False:
            if self.target == 'screenshots':
                self.main_win.save_screenshots(image_name)
                self.close()
            elif self.target == 'gif':

                self.main_win.save_gif(image_name, self.view_up)
                self.close()

            elif self.target == 'growing_ball':
                self.main_win.save_growing_ball_gif(image_name)
                self.close()

        else:
            QMessageBox.question(self, 'Warning', "Valid name is required", QMessageBox.Ok,
                                 QMessageBox.Ok)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 800)
    window.move(window.find_screen_center())
    window.zone_switch.move(window.find_screen_center())
    sys.exit(app.exec_())

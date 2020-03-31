import sys
import pyvista as pv
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QPoint
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox
import input_data
import file_operation as op
from zone_switch_window import ZoneSwitch


folder_path = input_data.folder_path


class MainWindow(QtWidgets.QMainWindow):

    center = input_data.ball_center  # user input ball center
    center_sphere_actor = None
    poly_actor_list = []
    zone_dict = {}
    txt_win = None  # for user to input the name of image
    gif_name_win = None  # for user to input the name of gif
    zone_switch = None  # the window used to control visibility of zones

    def __init__(self, parent=None, show=True):

        QtWidgets.QMainWindow.__init__(self, parent)
        self.frame = QtWidgets.QFrame()  # create the frame
        vlayout = QtWidgets.QVBoxLayout()
        # add the pyvista interactor object
        self.vtk_widget = pv.QtInteractor(self.frame)
        vlayout.addWidget(self.vtk_widget)
        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # set hot keys
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # draw all the polyhedrons
        self.add_polyhedron()

        # menu button for screenshots
        scrshots_menu = mainMenu.addMenu('Screenshots')
        self.add_screenshots_action = QtWidgets.QAction('Print screen', self)
        self.add_screenshots_action.triggered.connect(self.print_screen)
        scrshots_menu.addAction(self.add_screenshots_action)

        # menu button for hide/show zones
        layer_menu = mainMenu.addMenu('Brillouin Zone')
        zone_switch_action = QtWidgets.QAction(
            'Zone Switch', self, checkable=True, checked=True)
        layer_menu.addAction(zone_switch_action)
        zone_switch_action.triggered.connect(self.zone_switch_is_clicked)

        # menu button for save orbiting gif
        gif_menu = mainMenu.addMenu('Orbit GIF')
        gif_action_x = QtWidgets.QAction('Around X-Axis', self)
        gif_action_y = QtWidgets.QAction('Around Y-Axis', self)
        gif_action_z = QtWidgets.QAction('Around Z-Axis', self)
        gif_menu.addAction(gif_action_x)
        gif_menu.addAction(gif_action_y)
        gif_menu.addAction(gif_action_z)
        gif_action_x.triggered.connect(self.orbit_gif_is_clicked)
        gif_action_y.triggered.connect(self.orbit_gif_is_clicked)
        gif_action_z.triggered.connect(self.orbit_gif_is_clicked)

        # menu button for save growing ball gif
        growing_ball_menu = mainMenu.addMenu('Growing Ball GIF')
        growing_action = QtWidgets.QAction('Start recording', self)
        growing_ball_menu.addAction(growing_action)
        growing_action.triggered.connect(self.growing_action_is_clicked)

        # menu button for camera to return to a specific position
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

        self.radius_recorder = 0  # to stop ball growing

        if show:
            self.show()
            self.zone_switch.show()

    def growing_action_is_clicked(self):
        # create window of name input
        self.gif_name_win = TextWindow(self, "growing_ball")

    def axis_view_is_clicked(self):

        action = self.sender()
        action_text = action.text().split('-')[0]
        if action_text == 'X':
            self.vtk_widget.view_yz()
        elif action_text == 'Y':
            self.vtk_widget.view_xz()
        elif action_text == 'Z':
            self.vtk_widget.view_xy()

    def orbit_gif_is_clicked(self):

        action = self.sender()
        action_text = action.text().split()[1]
        if action_text == 'X-Axis':
            view_up = [1, 0, 0]
        elif action_text == 'Y-Axis':
            view_up = [0, 1, 0]
        elif action_text == 'Z-Axis':
            view_up = [0, 0, 1]

        self.gif_name_win = TextWindow(self, "orbit_gif", view_up)

    def zone_switch_is_clicked(self, state):

        if not state:
            self.zone_switch.setWindowOpacity(0)
        else:
            self.zone_switch.setWindowOpacity(1)

    def save_growing_ball_gif(self, image_name):
        """ 
        to call Phil's C++ package in this project, developer shall focus on this function.
        "nframe" controls the speed of growing
        """
        # open a gif
        self.vtk_widget.open_gif(folder_path + image_name + ".gif")

        # update radius and write a frame for each updated position
        nframe = 100  # how many frames in the gif
        max_radius = 10  # stop growing at max_radius
        # draw the gif
        for f in range(nframe):
            if self.center_sphere_actor is not None:
                self.vtk_widget.remove_actor(
                    self.center_sphere_actor)  # remove previous state

            upd_radius = f * max_radius / nframe + self.radius_recorder  # update the radius

            if upd_radius >= max_radius:
                break

            center_sphere = pv.Sphere(
                upd_radius, self.center, phi_resolution=100, theta_resolution=100)  # make the ball

            # show the ball
            self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                                reset_camera=False)
            self.vtk_widget.write_frame()

        # recover the initial ball after gif is done
        self.vtk_widget.remove_actor(self.center_sphere_actor)
        center_sphere = pv.Sphere(
            self.radius_recorder, self.center, phi_resolution=100, theta_resolution=100)
        self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                            reset_camera=False)

    def save_orbit_gif(self, gif_name, view_up):

        path = self.vtk_widget.generate_orbital_path(
            n_points=50, viewup=view_up)
        self.vtk_widget.open_gif(folder_path + gif_name + ".gif")
        self.vtk_widget.orbit_on_path(path, write_frames=True, viewup=view_up)

    def add_polyhedron(self):
        """
        parse the data from txt files and show all polyhedrons
        """

        polyhedron_data_list = op.open_folder(folder_path)

        for phd in polyhedron_data_list:
            poly_actor = self.vtk_widget.add_mesh(
                phd.get_grid(), opacity=1, color=phd.get_color())  # show the polyhedron
            self.poly_actor_list.append(poly_actor)

            zone = phd.get_zone()  # get zone number

            if zone in self.zone_dict.keys():
                self.zone_dict[zone].append(
                    (poly_actor, poly_actor.GetProperty().GetOpacity()))
            else:
                self.zone_dict[zone] = []
                self.zone_dict[zone].append(
                    (poly_actor, poly_actor.GetProperty().GetOpacity()))

        # create the center ball and slider which control its radius
        self.vtk_widget.add_slider_widget(self.create_center_sphere, [
                                          0.1, 15], 0.1, title='Radius', color="b")

    def create_center_sphere(self, radius, sphere_center=center):
        """ create the center ball

        Arguments:
            radius {int} -- initial radius (to make the ball invisible initially)

        Keyword Arguments:
            sphere_center {tuple} -- user input coordinate (default: {center})
        """
        self.radius_recorder = radius

        if self.center_sphere_actor is not None:
            self.vtk_widget.remove_actor(self.center_sphere_actor)

        center_sphere = pv.Sphere(
            radius, sphere_center, phi_resolution=100, theta_resolution=100)

        self.center_sphere_actor = self.vtk_widget.add_mesh(center_sphere, opacity=1, color='r',
                                                            reset_camera=False)

    def print_screen(self):
        self.txt_win = TextWindow(self, "screenshots")

    def save_screenshots(self, image_name):

        self.txt_win.update()
        self.vtk_widget.screenshot(folder_path + image_name)

    def zone_box_is_checked(self, state):

        action = self.sender()
        num = int(action.text().split()[1]) - 1
        if state:
            self.zone_visible(num)
        else:
            self.zone_invisible(num)

    def zone_invisible(self, zone_index):

        for pair in self.zone_dict[zone_index]:
            pair[0].GetProperty().SetOpacity(0)
            self.vtk_widget.update()

    def zone_visible(self, zone_index):

        for pair in self.zone_dict[zone_index]:
            pair[0].GetProperty().SetOpacity(pair[1])
            self.vtk_widget.update()

    def find_screen_center(self):
        """
        a function used to place the window at the center of the screen
        """
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry(-1)
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        return QPoint(x, y)

    def closeEvent(self, QCloseEvent):
        # make sure everything will be closed
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


class TextWindow(QtWidgets.QMainWindow):
    """
    create window asking for the name of saved image
    """

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
        if image_name is not "" and bool('/' in image_name) is False:
            if self.target == 'screenshots':
                self.main_win.save_screenshots(image_name)
                self.close()

            elif self.target == 'orbit_gif':
                self.main_win.save_orbit_gif(image_name, self.view_up)
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

import os
# sys.path.append("/Users/bumptious/PycharmProjects/0131FYP/0206-generalize-polyhedron/polyhedron_data.py")

from polyhedron_data import PolyhedronData

# https://lorensen.github.io/VTKExamples/site/Python/GeometricObjects/Cell3DDemonstration/

# PolyhedronData

'''

各种颜色：https://www.rapidtables.com/web/color/RGB_Color.html#color-table

        Black	 	0	 	0	 	0
        White	 	255	 	255	 	255
        Medium Gray	 	128	 	128	 	128
        Aqua	 	0	 	128	 	128
        Navy Blue	 	0	 	0	 	128
        Green	 	0	 	255	 	0
        Orange	 	255	 	165	 	0
        Yellow	 	255	 	255	 	0

'''


###################################################################################
# phd_1 = PolyhedronData("/Users/bumptious/PycharmProjects/0131FYP/0206-generalize-polyhedron/Test_Poly.off")
# phd_2 = PolyhedronData("/Users/bumptious/PycharmProjects/0131FYP/0206-generalize-polyhedron/Test_Cone.txt")
# win = None
# center_sphere_actor = None
# cube_actor = None
# pyramid_actor_lst = []
#
# # 球心
# center = (10, 10, 10)  # question：这个polyhedron的中心怎么获取？如果未来是不规则的就无法计算，必须直接从文件中获取

# def pass_window(passed_win):
#     global win
#     win = passed_win


###################################################################################
# def create_center_sphere(radius, sphere_center=center):
#     global center_sphere_actor
#
#     if center_sphere_actor is not None:
#         win.remove_actor(center_sphere_actor)
#
#     center_sphere = pv.Sphere(radius, sphere_center,phi_resolution=100,theta_resolution=100)
#
#     # plotter.add_mesh(center_sphere, opacity=0.2, color='r')
#
#     # center_sphere_actor = plotter.add_mesh(center_sphere, opacity=0.6, color='Aqua')
#
#     return


###################################################################################
# def create_polyhedron(polyhedron_data):
#     points = pv.vtk_points(np.array(polyhedron_data.get_vertex_list()))  # 生成 polyhedron的所有点, 类型均为 list，3D坐标
#
#     polyhedron_faces = polyhedron_data.get_faces_list()  # 此处注意Top是最后一个点，之前插入点的时候也要注意
#
#     polyhedron_faces_id_list = vtk.vtkIdList()
#     # Number faces that make up the cell.
#     polyhedron_faces_id_list.InsertNextId(len(polyhedron_faces))
#     for face in polyhedron_faces:
#         # Number of points in the face == numberOfFaceVertices
#         polyhedron_faces_id_list.InsertNextId(len(face))
#         # Insert the pointIds for that face.
#         [polyhedron_faces_id_list.InsertNextId(i) for i in face]
#
#     polyhedron_grid = vtk.vtkUnstructuredGrid()
#     polyhedron_grid.InsertNextCell(vtk.VTK_POLYHEDRON, polyhedron_faces_id_list)
#     polyhedron_grid.SetPoints(points)
#
#     return polyhedron_grid


###################################################################################


def open_folder(folder_path):

    polyhedron_data_list = []

    for file_name in os.listdir(folder_path):  # path to folder
        if file_name.endswith('.txt'):
            # print(file_name)
            # phd = PolyhedronData(split_lines(txt_reader(folder_path+"/"+file_name)))
            phd = PolyhedronData(split_lines_Phil(txt_reader(folder_path + "/" + file_name)))
            polyhedron_data_list.append(phd)

    return polyhedron_data_list


def txt_reader(file_name):
    # Open the file with read only permit
    f = open(file_name, "r")

    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines in the file
    lines = f.readlines()
    # print(lines)
    # close the file after reading the lines.
    f.close()
    # print('Here')

    del lines[3]  # 那个空行

    return lines


def split_lines(lines):

    # lines = self.txt_reader()
    # print(lines)
    layer = int(lines[1])

    num_of_points = int(lines[2].split()[0])  # 取得txt中第3行数组的第一个数字，即为点的数量
    # num_of_faces = int(lines[2].split()[1]) # 取得txt中第3行数组的第二个数字，即为face的数量

    pnt_coord_lst = []
    face_list = []

    for pnt_str in lines[3:(3+num_of_points)]:  # 因为line2本身也是一个点坐标,所以要-1
        splited_lst = pnt_str.split()
        pnt_coord = [float(i) for i in splited_lst]  # 把这行转化为一个含有3个float的list
        pnt_coord_lst.append(pnt_coord)  # 放进存所有坐标的大list

    for face_str in lines[(3+num_of_points):]:
        splited_lst = face_str.split()
        face = [int(j) for j in splited_lst[1:]]  # face 所在的行的第一个数字一概不要，其代表着该面由几个点组成
        face_list.append(face)

    return [pnt_coord_lst, face_list, layer]


def split_lines_Phil(lines):

    # lines = self.txt_reader()
    # print(lines)
    layer = int(lines[0])
    num_of_points = int(lines[2].split()[0])  # 取得txt中第3行数组的第一个数字，即为点的数量
    num_of_faces = int(lines[2].split()[1]) # 取得txt中第3行数组的第二个数字，即为face的数量

    pnt_coord_lst = []
    face_list = []

    for pnt_str in lines[3:(3+num_of_points)]:  # 因为line2本身也是一个点坐标,所以要-1
        splited_lst = pnt_str.split()
        pnt_coord = [float(i) for i in splited_lst]  # 把这行转化为一个含有3个float的list
        pnt_coord_lst.append(pnt_coord)  # 放进存所有坐标的大list

    for face_str in lines[(3+num_of_points):(3+num_of_points+num_of_faces)]:
        splited_lst = face_str.split()
        face = [int(j) for j in splited_lst[1:]]  # face 所在的行的第一个数字一概不要，其代表着该面由几个点组成
        face_list.append(face)

    return [pnt_coord_lst, face_list, layer]


# def draw_plot(plotter):

# plotter.add_slider_widget(create_center_sphere, [0.1, 30], 0.1, title='Radius', color="b")

# plotter.add_mesh(create_cube(), opacity=0.5, color='w')
#
# for prd in create_pyramid():
#     plotter.add_mesh(prd, opacity=0.4, color='g')

# for prd in create_pyramid():
#     plotter.add_mesh(prd, opacity=0.8, color='g')
# 一定让create_cube（）在 create_pyramid（）之前被执行，这样全局变量才能获取顶点位置

# 设置点一下h就会清除growing ball
# plotter.add_key_event("h", clear_ball)

# plotter.add_mesh(create_polyhedron(phd_1),opacity=0.5, color='b')

# plotter.add_mesh(create_polyhedron(phd_2),opacity=0.2, color='#2F4F4F')


# for point_coordinate in phd_2.get_vertex_list():
#     # point = pv.Sphere(0.1, point_coordinate)
#
#     poly = pv.PolyData(np.array([point_coordinate]))
#     poly["My Labels"] = ["Point {}".format( point_coordinate, 0.1)]
#     plotter.add_point_labels(poly, "My Labels", point_size=20, font_size=36,point_color="r")

# plotter.show()


###################################################################################

# if __name__ == '__main__':
#     open_folder(folder_path)

    # plotter = pv.Plotter()  # 生成 plotter
    # plotter.background_color = "w"
    #
    # draw_plot(plotter)  # plotter传进去

###################################################################################


# GUI
# https://docs.pyvista.org/plotting/qt_plotting.html?highlight=interaction
###################################################################################

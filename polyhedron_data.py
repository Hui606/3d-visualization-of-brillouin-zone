import pyvista as pv
import vtk
import numpy as np

# color_list = ['red',
#               'green',
#               'aqua',
#               'pink',
#               'gold',
#               'yellow']  # 目前最多六种颜色，即最多6个layer

color_list = [[0.4, 1, 0.1],
              [0.7, 0.9, 1],
              [0.3, 0, 0.9],
              [0.5, 1, 1],
              [0.9, 0.9, 0.1],
              [1, 0, 0.5],
              [0.3, 0, 0.1],
              [1, 1, 0.8]
              ]


def create_polyhedron(polyhedron_data):
    points = pv.vtk_points(np.array(polyhedron_data.vertex_list))  # 生成 polyhedron的所有点, 类型均为 list，3D坐标

    polyhedron_faces = polyhedron_data.polyhedron_faces  # 此处注意Top是最后一个点，之前插入点的时候也要注意

    polyhedron_faces_id_list = vtk.vtkIdList()
    # Number faces that make up the cell.
    polyhedron_faces_id_list.InsertNextId(len(polyhedron_faces))
    for face in polyhedron_faces:
        # Number of points in the face == numberOfFaceVertices
        polyhedron_faces_id_list.InsertNextId(len(face))
        # Insert the pointIds for that face.
        [polyhedron_faces_id_list.InsertNextId(i) for i in face]

    polyhedron_grid = vtk.vtkUnstructuredGrid()
    polyhedron_grid.InsertNextCell(vtk.VTK_POLYHEDRON, polyhedron_faces_id_list)
    polyhedron_grid.SetPoints(points)

    return polyhedron_grid


class PolyhedronData:

    def __init__(self, para_list):
        # self.file_name = file_name  # 后期会有一个reader用于读取传进来的file_name
        # lines_from_txt = txt_reader(file_name)
        self.vertex_list, self.polyhedron_faces, self.layer = para_list[0], para_list[1], para_list[2]
        self.grid = create_polyhedron(self)
        self.color = color_list[self.layer]

    def get_layer(self):
        return self.layer

    def get_grid(self):
        return self.grid

    def get_color(self):
        return self.color

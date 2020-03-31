import pyvista as pv
import vtk
import numpy as np

# every zone has a color from this list
# the number of zones cannot over the length of this list
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
    """
    create the vtk grid containing all points and faces
    """
    points = pv.vtk_points(np.array(polyhedron_data.vertex_list))

    polyhedron_faces = polyhedron_data.polyhedron_faces

    polyhedron_faces_id_list = vtk.vtkIdList()
    # Number faces that make up the cell.
    polyhedron_faces_id_list.InsertNextId(len(polyhedron_faces))
    for face in polyhedron_faces:
        # Number of points in the face == numberOfFaceVertices
        polyhedron_faces_id_list.InsertNextId(len(face))
        # Insert the pointIds for that face.
        [polyhedron_faces_id_list.InsertNextId(i) for i in face]

    polyhedron_grid = vtk.vtkUnstructuredGrid()
    polyhedron_grid.InsertNextCell(
        vtk.VTK_POLYHEDRON, polyhedron_faces_id_list)
    polyhedron_grid.SetPoints(points)

    return polyhedron_grid


class PolyhedronData:

    def __init__(self, para_list):
        self.vertex_list, self.polyhedron_faces, self.zone = para_list[
            0], para_list[1], para_list[2]
        self.grid = create_polyhedron(self)
        self.color = color_list[self.zone]

    def get_zone(self):
        return self.zone

    def get_grid(self):
        return self.grid

    def get_color(self):
        return self.color

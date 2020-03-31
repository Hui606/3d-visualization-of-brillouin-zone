import os
from polyhedron_data import PolyhedronData

# https://lorensen.github.io/VTKExamples/site/Python/GeometricObjects/Cell3DDemonstration/


def open_folder(folder_path):

    polyhedron_data_list = []

    for file_name in os.listdir(folder_path):  # path to folder
        if file_name.endswith('.txt'):
            phd = PolyhedronData(split_lines(
                txt_reader(folder_path + "/" + file_name)))
            polyhedron_data_list.append(phd)

    return polyhedron_data_list


def txt_reader(file_name):

    f = open(file_name, "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines in the file
    lines = f.readlines()
    f.close()  # close the file after reading the lines.
    del lines[3]  # delete the empty line in the txt file

    return lines


def split_lines(lines):

    layer = int(lines[0])
    num_of_points = int(lines[2].split()[0])
    num_of_faces = int(lines[2].split()[1])

    pnt_coord_lst = []  # points coordinates
    face_list = []  # the order of point index

    for pnt_str in lines[3:(3+num_of_points)]:
        splited_lst = pnt_str.split()
        pnt_coord = [float(i) for i in splited_lst]
        pnt_coord_lst.append(pnt_coord)

    for face_str in lines[(3+num_of_points):(3+num_of_points+num_of_faces)]:
        splited_lst = face_str.split()
        face = [int(j) for j in splited_lst[1:]]
        face_list.append(face)

    return [pnt_coord_lst, face_list, layer]

import bpy
import math
import mathutils
import csv
import json

FILE_PATH = (
    "/Users/geo/Documents/MATLAB/whiskitphysics/code/data/whisker_param_average_rat/"
)


def read_csv_string(file_path):
    data = list()
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:  # Each row is a list of values
            data.append(row)
    return data


def read_csv_int(file_path):
    data = read_csv_string(file_path)
    for index in range(len(data)):
        data[index] = [int(item) for item in data[index]]

    return data


def read_csv_float(file_path):
    data = read_csv_string(file_path)
    for index in range(len(data)):
        data[index] = [float(item) for item in data[index]]

    return data


def data_reader():
    whisker_names = read_csv_string(FILE_PATH + "param_name.csv")
    whisker_geom = read_csv_float(FILE_PATH + "param_s_a.csv")
    whisker_angles = read_csv_float(FILE_PATH + "param_angles.csv")
    whisker_pos = read_csv_int(FILE_PATH + "param_side_row_col.csv")
    base_pos = read_csv_float("/Users/geo/Downloads/param_bp_pos.csv")
    base_rot = read_csv_float(FILE_PATH + "param_bp_angles.csv")
    return [
        whisker_names,
        whisker_geom,
        whisker_angles,
        whisker_pos,
        base_pos,
        base_rot,
    ]


"""
unit: mm
"""


def calc_base_radius(row, col, length):
    base_radius = 0.041 + 0.002 * length + 0.011 * row - 0.0039 * col
    return base_radius / 2


"""

"""


def calc_slope(length, base_radius, row, col):
    slope = 0.0012 + 0.00017 * row - 0.000066 * col + 0.00011 * (col**2)
    tip_radius = (base_radius - slope * length) / 2

    if tip_radius <= 0.0015:
        tip_radius = 0.0015

    slope = (base_radius - tip_radius) / length
    return slope


def combine_links(whisker_links):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    for link in whisker_links:
        link.select_set(True)
    bpy.context.view_layer.objects.active = whisker_links[0]
    bpy.ops.object.join()
    return bpy.context.object


def apply_bp(whisker, pos, angles, whisker_name, link_length):
    whisker.location = pos
    # Decide whether we need to rotate based on the base point
    # Per Nadina's code, I think we need to do this
    bpy.context.view_layer.objects.active = whisker
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.transform.translate(value=(0, 0, -link_length / 2))
    bpy.ops.object.mode_set(mode="OBJECT")

    default_euler = mathutils.Euler((0, 0, 0), "XYZ")
    default_euler[1] = math.pi / 2
    additional_rotation = mathutils.Euler((angles[2], angles[1], angles[0]), "XYZ")
    default_euler.rotate(additional_rotation)
    whisker.rotation_euler = default_euler


def create_whisker(
    num_links,
    length,
    whisker_name,
    init_pos,
    init_rot,
    radius_base,
    radius_slope,
    link_angles,
    side,
):
    link_length = length / num_links

    # Rotate the cone 90 degrees around the Y-axis
    default_euler = mathutils.Euler((0, 0, 0), "XYZ")
    default_euler[1] = math.pi / 2
    additional_rotation = mathutils.Euler(
        (init_rot[2], init_rot[1], init_rot[0]), "XYZ"
    )
    default_euler.rotate(additional_rotation)

    location = mathutils.Vector(init_pos)

    rotation = default_euler

    #    links = []

    parent_obj = None

    for i in range(num_links):
        rotation = default_euler
        angle_radians = link_angles[i]
        bpy.ops.mesh.primitive_cone_add(
            radius1=radius_base - (i * (link_length * radius_slope)),
            radius2=radius_base - ((i + 1) * (link_length * radius_slope)),
            vertices=8,
            depth=link_length,
        )

        whisker_segment = bpy.context.object
        whisker_segment.name = f"{whisker_name}_link{i+1}"
        #        links.append(whisker_segment)

        bpy.context.view_layer.objects.active = whisker_segment
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.transform.translate(value=(0, 0, link_length / 2))
        bpy.ops.object.mode_set(mode="OBJECT")

        if parent_obj:
            whisker_segment.parent = parent_obj
            whisker_segment.location = mathutils.Vector((0, 0, link_length))
            whisker_segment.rotation_euler = mathutils.Euler(
                (-angle_radians, 0, 0), "XYZ"
            )
        else:
            whisker_segment.location = location
            whisker_segment.rotation_euler = rotation

        parent_obj = whisker_segment

    bpy.context.view_layer.update()
    # print(whisker_segment.matrix_world)
    return whisker_segment.matrix_world.translation


def create_whisker_shapes(points, whisker_name):
    mesh = bpy.data.meshes.new(whisker_name)
    whisker = bpy.data.objects.new(whisker_name, mesh)
    bpy.context.collection.objects.link(whisker)
    vertices = points
    edges = [(i, i + 1) for i in range(len(vertices) - 1)]
    mesh.from_pydata(vertices, edges, [])
    mesh.update()
    return whisker


def calculate_distance(point1, point2):
    vec1 = mathutils.Vector(point1)
    vec2 = mathutils.Vector(point2)
    return (vec1 - vec2).length


def compare_tips(whisker_tips, mesh_tips):
    for i in range(len(whisker_tips)):
        whisker_tip = whisker_tips[i]
        mesh_tip = mesh_tips[i]
        print(f"whisker{i} tip location:", whisker_tip)
        print(f"mesh{i} tip location:", mesh_tip)
        print("Difference in distance:", calculate_distance(whisker_tip, mesh_tip))


if __name__ == "__main__":
    # Clear existing objects
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    (
        whisker_names,
        whisker_geom,
        whisker_angles,
        whisker_pos,
        whisker_bp_coor,
        whisker_bp_angles,
    ) = data_reader()

    whisker_tips = []
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    control = bpy.context.object
    control.name = "WhiskerControl"
    
    for i in range(len(whisker_names)):
        # print(i)
        print(whisker_names[i])
        link_angles = whisker_angles[i]
        num_links = len(link_angles)
        length = whisker_geom[i][0]
        side = whisker_pos[i][0]
        row = whisker_pos[i][1]
        col = whisker_pos[i][2]
        radius_base = calc_base_radius(row, col, length)
        radius_slope = calc_slope(length, radius_base, row, col)
        if "R" in whisker_names[i][0]:
            if "D" in whisker_names[i][0]:
                init_pos = (
                    whisker_bp_coor[i + 1][0],
                    whisker_bp_coor[i + 1][1],
                    whisker_bp_coor[i + 1][2],
                )
            elif "E" in whisker_names[i][0]:
                init_pos = (
                    whisker_bp_coor[i + 2][0],
                    whisker_bp_coor[i + 2][1],
                    whisker_bp_coor[i + 2][2],
                )
            else:
                init_pos = (
                    whisker_bp_coor[i][0],
                    whisker_bp_coor[i][1],
                    whisker_bp_coor[i][2],
                )
        elif "L" in whisker_names[i][0]:
            if "D" in whisker_names[i][0]:
                init_pos = (
                    whisker_bp_coor[i + 4][0],
                    whisker_bp_coor[i + 4][1],
                    whisker_bp_coor[i + 4][2],
                )
            elif "E" in whisker_names[i][0]:
                init_pos = (
                    whisker_bp_coor[i + 5][0],
                    whisker_bp_coor[i + 5][1],
                    whisker_bp_coor[i + 5][2],
                )
            else:
                init_pos = (
                    whisker_bp_coor[i + 3][0],
                    whisker_bp_coor[i + 3][1],
                    whisker_bp_coor[i + 3][2],
                )
        else:
            init_pos = (
                whisker_bp_coor[i][0],
                whisker_bp_coor[i][1],
                whisker_bp_coor[i][2],
            )
        init_rot = (
            whisker_bp_angles[i][0] - math.pi / 2,
            -whisker_bp_angles[i][1],
            whisker_bp_angles[i][2] + math.pi / 2,
        )
        # Call the function to create the cone
        origin = (0, 0, 0)
        whisker = create_whisker(
            num_links,
            length,
            whisker_names[i][0],
            init_pos,
            init_rot,
            radius_base,
            radius_slope,
            link_angles,
            side,
        )
        whisker_tips.append(whisker)

    # whisker_points = {"right": [[] for _ in range(30)], "left": [[] for _ in range(30)]}
    # with open("Python/utils/ratWhiskingArray.json") as file:
    #     whisker_data = json.load(file)
    #     right_rest = whisker_data["ratWhiskingArray"][10][0]
    #     left_rest = whisker_data["ratWhiskingArray"][10][1]
    #     for i in range(len(right_rest)):
    #         rx = right_rest[i][0]
    #         ry = right_rest[i][1]
    #         rz = right_rest[i][2]
    #         lx = left_rest[i][0]
    #         ly = left_rest[i][1]
    #         lz = left_rest[i][2]
    #         for j in range(len(rx)):
    #             r_point = [rx[j], ry[j], rz[j]]
    #             whisker_points["right"][j].append(r_point)
    #             l_point = [lx[j], ly[j], lz[j]]
    #             whisker_points["left"][j].append(l_point)

    # mesh_tips = []
    # for i in range(len(whisker_points["right"])):
    #     points = whisker_points["right"][i]
    #     whisker_mesh = create_whisker_shapes(points, f"right_whisker_{i}")
    #     mesh_tips.append(points[-1])
    # for i in range(len(whisker_points["left"])):
    #     points = whisker_points["left"][i]
    #     whisker_mesh = create_whisker_shapes(points, f"left_whisker_{i}")
    #     mesh_tips.append(points[-1])

    # compare_tips(whisker_tips, mesh_tips)

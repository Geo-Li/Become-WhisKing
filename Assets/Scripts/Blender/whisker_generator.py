import bpy
import math
import mathutils
import csv
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
FILE_PATH = config['Data']['path']

def read_csv_string(file_path):
    data = list()
    
    with open(file_path, 'r') as file:
        csvreader = csv.reader(file)
        
        # To skip the header (if you have one)
        # next(csvreader)
        
        # Process each row
        for row in csvreader: # Each row is a list of values
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
    whisker_names = read_csv_string(FILE_PATH+"param_name.csv")
    whisker_geom = read_csv_float(FILE_PATH+"param_s_a.csv")
    whisker_angles = read_csv_float(FILE_PATH+"param_angles.csv")
    whisker_pos = read_csv_int(FILE_PATH+"param_side_row_col.csv")
    whisker_bp_coor = read_csv_float(FILE_PATH+"param_bp_pos.csv")
    whisker_bp_angles = read_csv_float(FILE_PATH+"param_bp_angles.csv")
    # print(whisker_angles)
    return [whisker_names, whisker_geom, whisker_angles, whisker_pos, whisker_bp_coor, whisker_bp_angles]


"""
unit: mm
"""
def calc_base_radius(row, col, length):
    base_radius = 0.041 + 0.002*length + 0.011*row - 0.0039*col
    return base_radius / 2


"""

"""
def calc_slope(length, base_radius, row, col):
    slope = 0.0012 + 0.00017*row - 0.000066*col + 0.00011*(col**2)
    tip_radius = (base_radius - slope*length)/2

    if tip_radius <= 0.0015:
        tip_radius = 0.0015

    slope = (base_radius-tip_radius) / length
    return slope


def rotX(angle):
    rot = mathutils.Quaternion((1,0,0), angle)
    return rot.to_matrix().to_4x4()


def rotY(angle):
    rot = mathutils.Quaternion((0,1,0), angle)
    return rot.to_matrix().to_4x4()


def rotZ(angle):
    rot = mathutils.Quaternion((0,0,1), angle)
    return rot.to_matrix().to_4x4()


def create_frame(origin, rotation=(0,0,0)):
    origin_vec = mathutils.Vector(origin)
    rotation_euler = mathutils.Euler((rotation[2], rotation[1], rotation[0]), "ZYX")
    mat_loc = mathutils.Matrix.Translation(origin_vec)
    mat_rot = rotation_euler.to_matrix().to_4x4()
    return mat_loc @ mat_rot


def create_whisker_segment(whisker_name,
                           side,
                           row,
                           col,
                           length,
                           radius_base,
                           radius_slope,
                           radius_tip,
                           link_angles,
                           base_pos,
                           base_rot,
                           NUM_LINKS):
    
    bpy.ops.object.select_all(action='DESELECT')
    
    # prev_end_location = mathutils.Vector(location)
    
    link_prev = None
    
    # parent_obj = None
    link_length = whisker_length / NUM_LINKS
    for i in range(NUM_LINKS):
        # Calculate segment size and position
        # radius = radius_base - (i * (link_length * radius_slope))
        angle = link_angles[i]
        total_transform = mathutils.Matrix.Identity(4)
        
        if i == 0:
            rot_transform = rotZ(base_rot[0]) @ rotY(base_rot[1]) @ rotX(base_rot[2])
            trans_transform = create_frame((link_length/2, 0, 0))
            total_transform = link_prev @ rot_transform @ trans_transform
        else:
            rotation = (0, 0, link_angles[i])
            link_transform1 = create_frame((link_length/2, 0, 0))
            link_transform2 = create_frame((0,0,0), (0, 0, angle))
            link_transform3 = create_frame((link_length/2, 0, 0))
            total_transform = link_prev @ link_transform1 @ link_transform2 @ link_transform3
                    
        # if i > 0:
        #     offset = mathutils.Vector((0,0,link_length))
        #     offset.rotate(mathutils.Euler(rotation))
        #     prev_end_location += offset
            

        # Create cylinder
        bpy.ops.mesh.primitive_cone_add(radius1=radius_base - (i * (link_length * radius_slope)),
                                        radius2=radius_base - ((i+1) * (link_length * radius_slope)),
                                        vertices=8,
                                        depth=link_length,)
                                        # location=prev_end_location,
                                        # rotation=rotation)
        segment = bpy.context.object
        segment.name = f"Whisker_{whisker_name}_Segment_{i}"
        
        segment.matrix_world = total_transform
        
        # Parenting
        # if parent_obj:
        #     segment.parent = parent_obj
        #     segment.location = (0, 0, link_length)
        
        # parent_obj = segment
        link_prev = segment.matrix_world().copy()


if __name__ == "__main__":
    whisker_names, whisker_geom, whisker_angles,\
    whisker_pos, whisker_bp_coor, whisker_bp_angles = data_reader()
    for i in range(len(whisker_names)):
        ##############################
        # configurations for whiskers
        ##############################
        whisker_name = whisker_names[i]
        side = whisker_pos[i][0]
        row = whisker_pos[i][1]
        col = whisker_pos[i][2]
        whisker_length = whisker_geom[i][0]
        radius_base = calc_base_radius(row, col, whisker_length)
        radius_slope = calc_slope(whisker_length, radius_base, row, col)
        radius_tip = radius_base - whisker_length*radius_slope        
        link_angles = whisker_angles[i]
        NUM_LINKS = len(link_angles)
        base_pos=(whisker_bp_coor[i][0], whisker_bp_coor[i][1], whisker_bp_coor[i][2]) #(i*2,0,0)
        base_rot=(whisker_bp_angles[i][0]-math.pi/2, -whisker_bp_angles[i][0], whisker_bp_angles[i][0]+math.pi/2)
        ##############################
        create_whisker_segment(whisker_name=whisker_name,
                               side=side,
                               row=row,
                               col=col,
                               length=whisker_length,
                               radius_base=radius_base,
                               radius_slope=radius_slope,
                               radius_tip=radius_tip,
                               link_angles=link_angles,
                               base_pos=base_pos,
                               base_rot=base_rot,
                               NUM_LINKS=NUM_LINKS)

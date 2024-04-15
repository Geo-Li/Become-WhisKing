import bpy
import math
import mathutils
import csv

FILE_PATH = "/Users/geo/Desktop/Education/Northwestern University/Research/whiskitphysics/code/data/whisker_param_average_rat/"
ALL = False

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
    
    # Initial transformation
    location = mathutils.Vector(base_pos)
#    rot_transform = rotZ(base_rot[0]) @ rotY(base_rot[1]) @ rotX(base_rot[2])
    rotation = mathutils.Euler((base_rot[0], base_rot[1], base_rot[2]), 'XYZ')
#    rotation = rot_transform.to_euler('XYZ')
    
    # parent_obj = None
    link_length = whisker_length / NUM_LINKS
    for i in range(NUM_LINKS):
        # Calculate segment size and position
        # radius = radius_base - (i * (link_length * radius_slope))
        angle_radians = link_angles[i]

        # Create cylinder
        bpy.ops.mesh.primitive_cone_add(radius1=radius_base - (i * (link_length * radius_slope)),
                                        radius2=radius_base - ((i+1) * (link_length * radius_slope)),
                                        vertices=8,
                                        depth=link_length,)
                                        # location=prev_end_location,
                                        # rotation=rotation)
                                        
        whisker_segment = bpy.context.object
        whisker_segment.name = f"Whisker_{whisker_name}_Segment_{i+1}"
        
        # Move origin to the base of the cone
        bpy.context.view_layer.objects.active = whisker_segment
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, -link_length / 2))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Set cone transformation
        whisker_segment.location = location
        whisker_segment.rotation_euler = rotation
        
        # Calculate the new base position for the next cone
        # Move up along the local Z-axis of the cone (accounting for rotation)
        offset = mathutils.Vector((0, 0, link_length))
        rotation.z += angle_radians
        offset.rotate(rotation)
        location += offset
        
        # Parenting
        # if parent_obj:
        #     segment.parent = parent_obj
        #     segment.location = (0, 0, link_length)
        
        # parent_obj = segment


if __name__ == "__main__":
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    num_whiskers = 30 if not ALL else 60
    
    whisker_names, whisker_geom, whisker_angles,\
    whisker_pos, whisker_bp_coor, whisker_bp_angles = data_reader()
    for i in range(num_whiskers):
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
        base_rot=(whisker_bp_angles[i][0], whisker_bp_angles[i][1], whisker_bp_angles[i][2])
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
                               base_rot=(15,0,0),
                               NUM_LINKS=NUM_LINKS)

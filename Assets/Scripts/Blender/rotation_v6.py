import bpy
import math
import mathutils
import csv

FILE_PATH = "/Users/geo/Documents/MATLAB/whiskitphysics/code/data/whisker_param_average_rat/"


def read_csv_string(file_path):
    data = list()
    with open(file_path, 'r') as file:
        csvreader = csv.reader(file)
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
    base_pos = read_csv_float(FILE_PATH+"param_bp_pos.csv")
    base_rot = read_csv_float(FILE_PATH+"param_bp_angles.csv")
    whisker_points = []
    with open(FILE_PATH+"whisker_data.csv") as whisker_data:
        reader = csv.reader(whisker_data, delimiter=',')
        for data_points in reader:
            whisker_points.append(list(map(float, data_points)))  # Convert to floats
    return [whisker_names, whisker_geom, 
            whisker_angles, whisker_pos, 
            base_pos, base_rot, whisker_points]


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



def combine_links(whisker_links):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
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
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, -link_length/2))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    default_euler = mathutils.Euler((0, 0, 0), 'XYZ')
    default_euler[1] = math.pi / 2
    additional_rotation = mathutils.Euler((angles[2],angles[1],angles[0]), 'XYZ')
    default_euler.rotate(additional_rotation)
    whisker.rotation_euler = default_euler


def create_whisker(num_links, length, whisker_name,
                   init_pos, init_rot,
                   radius_base, radius_slope,
                   link_angles, side):
    link_length = length / num_links

    # Rotate the cone 90 degrees around the Y-axis
    default_euler = mathutils.Euler((0, 0, 0), 'XYZ')
    default_euler[1] = math.pi / 2
    additional_rotation = mathutils.Euler((init_rot[2],init_rot[1],init_rot[0]), 'XYZ')
    default_euler.rotate(additional_rotation)
    
    location = mathutils.Vector(init_pos)
    
    rotation = default_euler
    
#    links = []
    
    for i in range(num_links):
        rotation = default_euler
        angle_radians = link_angles[i]
        bpy.ops.mesh.primitive_cone_add(radius1=radius_base - (i * (link_length * radius_slope)),
                                        radius2=radius_base - ((i+1) * (link_length * radius_slope)),
                                        vertices=8,
                                        depth=link_length)
                                        
        
        whisker_segment = bpy.context.object
        whisker_segment.name = f"{whisker_name}_link{i+1}"
#        links.append(whisker_segment)
        
        bpy.context.view_layer.objects.active = whisker_segment
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, -link_length/2))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Set cone transformation
        whisker_segment.location = location
        whisker_segment.rotation_euler = rotation
#        
        offset = mathutils.Vector((0, 0, link_length))
        rotation.x -= angle_radians
#        if side:
#            rotation.x += angle_radians
#        else:
#            rotation.x -= angle_radians
        offset.rotate(rotation)
        location += offset
        
#    return links
        


def create_whisker_shapes(points, whisker_name):
    mesh = bpy.data.meshes.new(whisker_name)
    whisker = bpy.data.objects.new(whisker_name, mesh)
    bpy.context.collection.objects.link(whisker)
    vertices = points
    edges = [(i, i + 1) for i in range(len(vertices) - 1)]
    mesh.from_pydata(vertices, edges, [])
    mesh.update()
    return whisker




if __name__ == "__main__":
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    whisker_names, whisker_geom,\
    whisker_angles, whisker_pos,\
    whisker_bp_coor, whisker_bp_angles,\
    whisker_points = data_reader()
    
    for i in range(len(whisker_names)):
        link_angles = whisker_angles[i]
        num_links = len(link_angles)
        length = whisker_geom[i][0]
        side = whisker_pos[i][0]
        row = whisker_pos[i][1]
        col = whisker_pos[i][2]
        radius_base = calc_base_radius(row, col, length)
        radius_slope = calc_slope(length, radius_base, row, col)
        init_pos = (whisker_bp_coor[i][0], whisker_bp_coor[i][1], whisker_bp_coor[i][2])
        init_rot = (whisker_bp_angles[i][0]-math.pi/2, -whisker_bp_angles[i][1], whisker_bp_angles[i][2]+math.pi/2)
        # Call the function to create the cone
        origin = (0,0,0)
#        whisker = create_whisker(angles, length, origin, NUM_LINKS, link_angles, radius_base, radius_slope)
        create_whisker(num_links, length, whisker_names[i][0],
                   init_pos, init_rot,
                   radius_base, radius_slope,
                   link_angles, side)
#        whisker = combine_links(whisker)
#        apply_bp(whisker, pos, angles, whisker_names[i], length/NUM_LINKS)
    
    for i in range(0, len(whisker_points), 100):
        points = whisker_points[i:i + 100]
        whisker_mesh = create_whisker_shapes(points, whisker_names[i//100][0])

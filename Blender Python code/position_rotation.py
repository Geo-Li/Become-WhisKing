import bpy
import math
import mathutils
import csv
FILE_PATH = "/Users/geo/Desktop/Education/Northwestern University/Research/whiskitphysics/code/data/whisker_param_average_rat/"


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
    whisker_bp_angles = read_csv_float(FILE_PATH+"param_bp_angles.csv")
    return whisker_bp_angles


def combine_links(whisker_links):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for link in whisker_links:
        link.select_set(True)
    bpy.context.view_layer.objects.active = whisker_links[0]
    bpy.ops.object.join()
    return bpy.context.object



def apply_bp(whisker, pos, rot, whisker_name, link_length):
    whisker.location = pos
    # Ensure the rotation mode is set to Euler XYZ, to correctly apply the Euler rotations
#    whisker.rotation_mode = 'XYZ'
    bpy.context.view_layer.objects.active = whisker
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, -link_length/2))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    default_euler = mathutils.Euler((0, 0, 0), 'XYZ')
    additional_rotation = mathutils.Euler((angles[2],angles[1],angles[0]), 'XYZ')
    default_euler.rotate(additional_rotation)
    whisker.rotation_euler = default_euler
    rot = whisker.rotation_euler
#    additional_rotation = mathutils.Euler((angles[2],angles[1],angles[0]), 'XYZ')
    print(f"{whisker_name} rotations x: {rot.x}, y: {rot.y}, z: {rot.z}")
    bpy.context.view_layer.update()



def create_cone(angles, length, pos, NUM_LINKS, link_angles):
    link_length = length / NUM_LINKS
    # Create a cone
#    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.2, radius2=0.2, depth=link_length, end_fill_type='NGON')

    # Get the newly created cone
#    cone = bpy.context.object

    # Rotate the cone 90 degrees around the Y-axis
    default_euler = mathutils.Euler((0, 0, 0), 'XYZ')
    default_euler[1] = math.pi / 2
#    cone.rotation_euler[1] = math.pi / 2
    
#    additional_rotation = mathutils.Euler((angles[2],angles[1],angles[0]), 'XYZ')
#    default_euler.rotate(additional_rotation)
     
    location = mathutils.Vector(pos)
#    cone.location = location
    
    rotation = default_euler
    
    links = list()
    
    parent_obj = None
    
    for i in range(NUM_LINKS):
        angle_radians = link_angles[i]
        bpy.ops.mesh.primitive_cone_add(radius1=0.2,
                                        radius2=0.2,
                                        vertices=8,
                                        depth=link_length)
        whisker_segment = bpy.context.object
        
        if i==0:
            parent_obj = whisker_segment
        else:
            whisker_segment.parent = parent_obj
        
        
        bpy.context.view_layer.objects.active = whisker_segment
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, -link_length/2))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Set cone transformation
        whisker_segment.location = location
        whisker_segment.rotation_euler = rotation
        
        links.append(whisker_segment)
        
        offset = mathutils.Vector((0, 0, link_length))
        additional_rotation = mathutils.Euler((0,0,angle_radians), 'XYZ')
        rotation.rotate(additional_rotation)
#        rotation.x += angle_radians
        offset.rotate(rotation)
#        offset.rotate(additional_rotation)
        location += offset
    
    return links
        
        

if __name__ == "__main__":
    # Clear existing objects
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    whisker_names = read_csv_string(FILE_PATH+"param_name.csv")
    whisker_angles = read_csv_float(FILE_PATH+"param_angles.csv")
    whisker_geom = read_csv_float(FILE_PATH+"param_s_a.csv")
    whisker_bp_coor = read_csv_float(FILE_PATH+"param_bp_pos.csv")
    whisker_bp_angles = read_csv_float(FILE_PATH+"param_bp_angles.csv")
    for i in range(1):
        link_angles = whisker_angles[i]
        NUM_LINKS = len(link_angles)
        length = whisker_geom[i][0]
        pos=(whisker_bp_coor[i][0], whisker_bp_coor[i][1], whisker_bp_coor[i][2])
        angles = (whisker_bp_angles[i][0]-math.pi/2, -whisker_bp_angles[i][1], whisker_bp_angles[i][2]+math.pi/2)
        print(f"modified angles: x: {angles[0]}, y: {angles[1]}, z: {angles[2]}")
    #    if i >= 30:
    #        link_angles = [-angle for angle in link_angles]
        # Call the function to create the cone
        whisker_links = create_cone(angles, length, (0,0,0), NUM_LINKS, link_angles)
        combined_whisker_links = combine_links(whisker_links)
        apply_bp(combined_whisker_links, pos, angles, whisker_names[i], link_length=(length/NUM_LINKS))

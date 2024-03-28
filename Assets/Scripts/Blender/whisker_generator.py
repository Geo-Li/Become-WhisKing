import bpy
import math
import csv


FILE_PATH = "/home/guru/Desktop/whiskitphysics/code/data/whisker_param_average_rat/"


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
    # print(whisker_angles)
    return [whisker_names, whisker_geom, whisker_angles, whisker_pos]


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


def create_whisker_segment(whisker_name,
                           side,
                           row,
                           col,
                           length,
                           radius_base,
                           radius_slope,
                           radius_tip,
                           link_angles,
                           NUM_LINKS,
                           location=(0, 0, 0)):
    
    bpy.ops.object.select_all(action='DESELECT')

    parent_obj = None
    link_length = whisker_length / NUM_LINKS
    for i in range(NUM_LINKS):
        # Calculate segment size and position
        # radius = radius_base - (i * (link_length * radius_slope))
        location = (location[0], location[1], location[2] + (link_length if i > 0 else 0))
        
        # Create cylinder
        bpy.ops.mesh.primitive_cone_add(
                                            radius1=radius_base - (i * (link_length * radius_slope)),
                                            radius2=radius_base - ((i+1) * (link_length * radius_slope)),
                                            # vertices=32,
                                            depth=link_length,
                                            location=location)
        segment = bpy.context.object
        segment.name = f"Whisker_{whisker_name}_Segment_{i}"
        
        # Parenting
        if parent_obj:
            segment.parent = parent_obj
            segment.location = (0, 0, link_length / 2)
        
        parent_obj = segment


if __name__ == "__main__":
    whisker_names, whisker_geom, whisker_angles, whisker_pos = data_reader()
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
        location=(i*2,0,0)
        ##############################
        # same applies to the location
        # I am not worrying about the angles between links for now
        create_whisker_segment(whisker_name=whisker_name,
                               side=side,
                               row=row,
                               col=col,
                               length=whisker_length,
                               radius_base=radius_base,
                               radius_slope=radius_slope,
                               radius_tip=radius_tip,
                               link_angles=link_angles,
                               NUM_LINKS=NUM_LINKS,
                               location=location)

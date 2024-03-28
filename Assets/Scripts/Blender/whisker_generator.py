import bpy
import math
import csv


FILE_PATH = "/Users/geo/Desktop/Education/Northwestern University/Research/whiskitphysics/code/data/param_sinusoidal/whisker_param_model_rat/"


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
    print(whisker_angles)
    return [whisker_names, whisker_geom, whisker_angles]


def create_whisker_segment(radius_base, length, NUM_LINKS, location=(0, 0, 0)):
    bpy.ops.object.select_all(action='DESELECT')
    
    parent_obj = None
    for i in range(NUM_LINKS):
        # Calculate segment size and position
        radius = radius_base - (i * (radius_base / NUM_LINKS))
        segment_length = length / NUM_LINKS
        location = (location[0], location[1], location[2] + (segment_length if i > 0 else 0))
        
        # Create cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=segment_length, location=location)
        segment = bpy.context.object
        segment.name = f"Whisker_Segment_{i+1}"
        
        # Parenting
        if parent_obj:
            segment.parent = parent_obj
            segment.location = (0, 0, segment_length / 2)
        
        parent_obj = segment

if __name__ == "__main__":
    data_reader()
    # Example usage
    NUM_LINKS = 10
    create_whisker_segment(radius_base=0.1, length=2.0, NUM_LINKS=NUM_LINKS)

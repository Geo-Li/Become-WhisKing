import csv
import bpy
from math import cos, sin

FILE_PATH = "/Users/geo/Documents/MATLAB/whiskitphysics/code/data/whisker_param_average_rat/whisker_data.csv"

def data_reader():
    data = []
    with open(FILE_PATH) as whisker_data:
        reader = csv.reader(whisker_data, delimiter=',')
        for data_point in reader:
            data.append(list(map(float, data_point)))  # Convert to floats
    return data

def create_whisker(points, whisker_name):
    mesh = bpy.data.meshes.new(whisker_name)
    obj = bpy.data.objects.new(whisker_name, mesh)
    bpy.context.collection.objects.link(obj)
    verts = points
    edges = [(i, i + 1) for i in range(len(verts) - 1)]
    mesh.from_pydata(verts, edges, [])
    mesh.update()
    return obj

if __name__ == "__main__":
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()  # Clear existing objects

    whisker_points = data_reader()
    for i in range(0, len(whisker_points), 100):
        whisker_name = f'Whisker_{i // 100}'
        points = whisker_points[i:i + 100]
        whisker_obj = create_whisker(points, whisker_name)

    material = bpy.data.materials.new(name="Whisker_Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Red
#        bsdf.inputs['Emission'].default_value = (1.0, 0.0, 0.0, 1.0)  # Make it glow red for visibility
        bsdf.inputs['Emission Strength'].default_value = 10.0

    for obj in bpy.data.objects:
        if "Whisker" in obj.name and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')

    # Make sure the viewport updates to show new materials
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
    
    bpy.data.worlds['World'].node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0

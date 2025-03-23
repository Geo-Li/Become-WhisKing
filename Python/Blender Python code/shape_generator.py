import bpy
import math
from mathutils import Vector, Euler

# Delete everything first for a clean scene
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Create a cone pointing to +Z
def create_cone_z(name="Cone_Z", location=(0, 0, 0), radius1=1, depth=2):
    bpy.ops.mesh.primitive_cone_add(
        radius1=radius1,
        depth=depth,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    # By default, cones point down -Z, so rotate 180° to point +Z
    obj.rotation_euler = Euler((math.radians(180), 0, 0), 'XYZ')
    return obj

# Create a cone pointing to +X
def create_cone_x(name="Cone_X", location=(0, 0, 0), radius1=1, depth=2):
    bpy.ops.mesh.primitive_cone_add(
        radius1=radius1,
        depth=depth,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    # Rotate cone to point +X
    obj.rotation_euler = Euler((0, math.radians(90), math.radians(-90)), 'XYZ')
    return obj

# Create a cone pointing to +Y
def create_cone_y(name="Cone_Y", location=(0, 0, 0), radius1=1, depth=2):
    bpy.ops.mesh.primitive_cone_add(
        radius1=radius1,
        depth=depth,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    # Rotate cone to point +Y
    obj.rotation_euler = Euler((math.radians(-90), 0, 0), 'XYZ')
    return obj

# Main function
def main():
    clear_scene()

    # Place the cones at different positions so you can see them clearly
    cone_z = create_cone_z(location=(0, 0, 0))
    cone_x = create_cone_x(location=(3, 0, 0))
    cone_y = create_cone_y(location=(0, 3, 0))

# Run the main function
main()

import bpy
import mathutils

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

start_radius = 1
length = 3
location = mathutils.Vector((0, 0, 0))

parent_obj = None

# Draw a series of cones
for i in range(9):
    bpy.ops.mesh.primitive_cone_add(radius1=start_radius - i*(0.1),
                                    radius2=start_radius - (i + 1)*(0.1),
                                    vertices=8,
                                    depth=length)
    cone = bpy.context.object
    bpy.context.view_layer.objects.active = cone
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, length/2))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if parent_obj:
        cone.parent = parent_obj
        cone.location = mathutils.Vector((0, 0, length))
    else:
        cone.location = location

    parent_obj = cone
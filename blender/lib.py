print('hello world')
# import IPython; IPython.embed()
# bpy.ops.import_mesh.stl(
#     filepath='/Users/matt-admin/code/penrose/stl/compounds/cross-compound-3.py.scad.stl',
#     #os.path.dirname(__file__),
#     # filter_glob="*.stl",
#     # files=[{"name":"mymodel.stl", "name":"mymodel.stl"}],
#     # directory="C://Users//Dom//Documents//DomCorp."
#     )
import bpy

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

# Test
obj_camera = bpy.data.objects["Camera"]
obj_other = bpy.data.objects["Cube"]

obj_camera.location = (5.0, 2.0, 3.0)
look_at(obj_camera, obj_other.matrix_world.to_translation())


# geo_engine.carpet(*stl, offset=2, cols=cols, rows=rows)
# geo_engine.grid()
# obj.createNode("geo", "geo1", run_init_scripts=False)
# > <hou.ObjNode of type geo at /obj/geo3>
# > >>> obj.node("geo1").children()
# > (<hou.SopNode of type file at /obj/geo1/file1>,)
# node = hx.create_node(obj, 'node', type= 'geo', run_init_scripts=False)
# geo = node.geometry()
# p0 = geo.createPoint()
# p1 = geo.createPoint()
# geo = hx.create_node(obj, 'geo', type='geo')
# p2 = geo.createPoint()
# p3 = geo.createPoint()
# p4 = default.geo.createPoint()
# p0.setPosition((0, 0, 0))
# p1.setPosition((.5, .5, .5))
# p2.setPosition((.5, -.5, -.5))
# p3.setPosition((-.5, .5, -.5))
# p4.setPosition((-.5, -.5, .5))



# middle = geo_engine.copy_node(stl, into='middle', count=num_cols)
# [  obj.setParmTransform(hou.hmath.buildTranslate(
#         base['x'] + (-1**i)*(offset*i),
#         base['y'],
#         base['z']))
#     for i, obj in enumerate(middle)  ]

# stl.setName('-'.join(['original', stl.name()]))


# stl_file.loadFromFile(os.path.join(
#     STL_ROOT,
#     '/compounds/cross-compound-3.py.scad.stl'))
#     # get_viewport().setCamera(cam)
#     describe_nodes()
#     # addTriangle(default,  p,  q,  r)
#     addTriangle(default, p0, p1, p2)
#     addTriangle(default, p0, p1, p3)
#     addTriangle(default, p0, p1, p4)
#     addTriangle(default, p0, p2, p3)
#     addTriangle(default, p0, p2, p4)
#     addTriangle(default, p0, p3, p4)
#     describe_nodes()
# main()
# root.move(hou.Vector2(0, 0))

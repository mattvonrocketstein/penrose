
# @main.command(name='stl-render', help='show')
# @click.option('--verbose', help='set logger to DEBUG', default=False, is_flag=True)
# @click.option('--size', help='img size', default='1024', required=False)
# # @click.option('-o', '--output-dir', help='output dir', required=False, default=None)
# @click.argument('filename')
# @click.pass_context
# def stl_render(ctx, verbose, size, filename):
#     LOGGER.debug("rendering filename: {}".format(filename))
#     # cmd = '{} -b -P mesh2img.py -- --paths {} --dimensions {} --camera-coords 0.0,0.0,10.0'.format(BLENDER_EXEC, filename, size)
#     # {filepath}_{width}.{ext}
#     util.invoke(cmd)
#     # from stl import mesh
#     # from mpl_toolkits import mplot3d
#     # from matplotlib import pyplot
#     # # Create a new plot
#     # figure = pyplot.figure()
#     # axes = mplot3d.Axes3D(figure)
#     # # Load the STL files and add the vectors to the plot
#     # your_mesh = mesh.Mesh.from_file(filename)
#     # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#     # # Auto scale to the mesh size
#     # scale = your_mesh.points.flatten(-1)
#     # axes.auto_scale_xyz(scale, scale, scale)
#     # # Show the plot to the screen
#     # pyplot.show()
#
#
#
# @main.command(name='stl-rotate', help='rotate')
# @click.option('--verbose', help='set logger to DEBUG', default=False, is_flag=True)
# @click.option('--step', help='step angle', required=False, default='10')
# @click.option('-o', '--output-dir', help='output dir', required=False, default=None)
# @click.argument('filename')
# @click.pass_context
# def stl_rotate(ctx, verbose, step, output_dir, filename):
#     from stl import mesh
#     stl_mesh = mesh.Mesh.from_file(filename)
#     step = int(step)
#     output_dir = output_dir or os.path.join(os.getcwd(),'output')
#     if not os.path.isdir(output_dir):
#         LOGGER.debug("saving to: ".format(output_dir))
#         os.makedirs(output_dir)
#
#     rotation_axises = [0.0, 1.0, 0.0]
#     iterations = int(360.0/step)
#     for i in range(1, iterations):
#         angle = step*i
#         file = os.path.join(output_dir,'angle-{}.stl'.format(angle))
#         LOGGER.debug(" angle {}: saving to {}".format(angle,file) )
#         stl_mesh.rotate(rotation_axises, math.radians(angle))
#         stl_mesh.save(file)

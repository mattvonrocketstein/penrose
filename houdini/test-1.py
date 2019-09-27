import hou

"""
This module lets you create and evaluate a compositing network simply
by writing an expression describing the compositing operations to perform.
With some simple extensions to this example, you can create a Pythonic
equivalent of Houdini's icomposite program.

For example, you can write:

    import comp
    comp.readFile("default.pic").bright(1.2).over(comp.constant(0.3, 0.3, 0.3)
        ).writeFile("out.pic")

and Houdini will build a composite network that loads the default.pic image,
brightens it, composites it over a constant, and writes out the result to
out.pic.

Note that this module supports compositing over a sequence of images: simply
use a time-dependent expression (like $F) in the input and output image names.

If you use this module from a graphical Houdini session, you can inspect
the compositing networks it creates.
"""

def test():
    """This function creates a simple test case that evaluates the following:
       comp.readFile("default.pic").bright(1.2).over(
           comp.constant(0.3, 0.3, 0.3)).writeFile("out.pic")
    """
    readFile("default.pic").bright(1.2).over(constant(0.3, 0.3, 0.3)
        ).writeFile("out.pic")

class _Image:
    """This image class wraps a COP node and exposes image operations via
       methods that simply create COP nodes and return a new image wrapping
       that node.
    """
    def __init__(self, node):
        # The node parameter is a COP node.  The user of this module will
        # create images with the readFile and constant methods, and construct
        # _Image objects directly.
        self.node = node

    def __createNode(self, type):
        # Create and return a COP node of the specified type in the current
        # network.
        return self.node.parent().createNode(type)

    def bright(self, amount):
        """Brighten the image, returning a new image."""
        n = self.__createNode("bright")
        n.setFirstInput(self.node)
        n.parm("bright").set(amount)
        return _Image(n)

    def over(self, image):
        """Composite this image over the specified one, returning a new
           image."""
        n = self.__createNode("over")
        n.setFirstInput(self.node)
        n.setInput(1, image.node)
        return _Image(n)

    def writeFile(self, file_name):
        """Write this image to a file or file sequence."""
        n = self.__createNode("rop_comp")
        n.setFirstInput(self.node)
        n.parm("copoutput").set(file_name)
        self.node.parent().layoutChildren()

        # If we're called from a standard Python shell or hython, actually
        # write out the file.
        if hou.applicationName() == 'hbatch':
            n.render()

def __network():
    # This internal function just returns the COP network.  For this example,
    # it simply hard-codes a particular network.
    return hou.node("/img/comp1") or hou.node("/img").createNode("img", "comp1")

def __nodeResolution(node):
    """Use the hscript res() expression to return the a composite node's
       image resolution."""
    return (hou.hscriptExpression('res("%s", D_XRES)' % node.path()),
        hou.hscriptExpression('res("%s", D_YRES)' % node.path()))

_lastResolution = None

def readFile(file_name):
    """Return an image object corresponding to a file or file sequence."""
    n = __network().createNode("file")
    n.parm("filename1").set(file_name)

    # Remember the image resolution.  If we later create a constant color,
    # we'll use this resolution.
    global _lastResolution
    _lastResolution = __nodeResolution(n)

    return _Image(n)

def constant(r, g, b, a=1.0):
    """Return an image that's a constant color.  The size of the image will
       be the same as the size of the last file read in."""
    n = __network().createNode("color")
    n.parmTuple("color").set((r, g, b, a))

    if _lastResolution is not None:
        n.parm("overridesize").set(True)
        n.parmTuple("size").set(_lastResolution)
    return _Image(n)

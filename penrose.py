import os
import math
import random
import cmath
import cairocffi as cairo

from solid import (
    union, translate, cube, polygon, color,
    difference, cylinder, OpenSCADObject)
from solid.utils import scad_render_to_file
SCAD_SEGMENTS = 48
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2


class Canvas(object):

    out_png = 'penrose.png'
    out_scad = 'penrose.scad'

    def __init__(self, IMAGE_SIZE):
        """ """
        self.IMAGE_SIZE = [IMAGE_SIZE] * 2
        # Prepare cairo surface
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.IMAGE_SIZE[0], self.IMAGE_SIZE[1])
        self.cr = cairo.Context(self.surface)

    def draw_lines(self, triangles):
        # Determine line width from size of first triangle
        kolor, A, B, C = triangles[0]
        self.cr.set_line_width(abs(B - A) / 10.0)
        self.cr.set_line_join(cairo.LINE_JOIN_ROUND)

        # Draw outlines
        for kolor, A, B, C in triangles:
            self.cr.move_to(C.real, C.imag)
            self.cr.line_to(A.real, A.imag)
            self.cr.line_to(B.real, B.imag)
        self.cr.set_source_rgb(0.2, 0.2, 0.2)
        self.cr.stroke()

    def finish(self, kolor):
        """
        """
        if kolor == 0:
            self.cr.set_source_rgb(0, 0, 0)
        else:
            self.cr.set_source_rgb(1, 1, 1)
        self.cr.fill()
        # import IPython; IPython.embed()
        # raise Exception("bonk")

    def render(self, triangles):
        self.render_cairo(triangles)
        self.render_scad(triangles)

    def render_scad(self, triangles):
        """
        """
        triangle_points = [
            [
                [C.real, C.imag],
                [A.real, A.imag],
                [B.real, B.imag],
            ] for kolor, A, B, C in triangles]
        print triangles[0]
        print triangle_points[0]
        objects = [

            OpenSCADObject('polygon', {'points': x}) for x in triangle_points
        ]
        for i, obj in enumerate(objects):
            if i % 2 == 0:
                # obj = color('black')(obj)
                pass
            else:
                obj = color('black')(obj)
                objects[i] = obj
            # objects[i] = obj

        obj = union()(cube(1), *objects)
        self.save_scad(obj)

    def render_cairo(self, triangles=[]):
        """ """
        self.cr.translate(
            self.IMAGE_SIZE[0] / 2.0,
            self.IMAGE_SIZE[1] / 2.0)
        wheelRadius = 1.2 * \
            math.sqrt((self.IMAGE_SIZE[0] / 2.0) **
                      2 + (self.IMAGE_SIZE[1] / 2.0) ** 2)
        self.cr.scale(wheelRadius, wheelRadius)

        # Draw triangles
        for kolor, A, B, C in triangles:
            self.cr.move_to(A.real, A.imag)
            self.cr.line_to(B.real, B.imag)
            self.cr.line_to(C.real, C.imag)
            self.cr.close_path()
            self.finish(kolor)
        self.draw_lines(triangles)
        self.save_png()

    def save_png(self):
        # Save to PNG
        self._save(
            lambda fname: self.surface.write_to_png(fname),
            self.out_png
        )

    def save_scad(self, objects):
        """ """
        self._save(
            lambda fname: scad_render_to_file(
                objects,
                fname,
                include_orig_code=False,
                file_header='$fn = %s;' % SCAD_SEGMENTS),
            self.out_scad)

    def _save(self, fxn, fname):
        if os.path.exists(fname):
            msg = 'overwriting file: '
            os.system('rm "{0}"'.format(fname))
        else:
            msg = 'writing to file: '
        print msg + "{0}".format(fname)
        fxn(fname)


def subdivide(triangles):
    """
    """
    result = []
    for kolor, A, B, C in triangles:
        if kolor == 0:
            # Subdivide red triangle
            P = A + (B - A) / GOLDEN_RATIO
            result += [(0, C, P, B), (1, P, C, A)]
        else:
            # Subdivide blue triangle
            Q = B + (A - B) / GOLDEN_RATIO
            R = B + (C - B) / GOLDEN_RATIO
            result += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
    return result


def tiling():
    # Create wheel of red triangles around the origin
    triangles = []
    for i in xrange(10):
        B = cmath.rect(1, (2 * i - 1) * math.pi / 10)
        C = cmath.rect(1, (2 * i + 1) * math.pi / 10)
        if i % 2 == 0:
            B, C = C, B  # Make sure to mirror every second triangle
        triangles.append((0, 0j, B, C))
    return triangles


def elaborate(triangles, num_subdivisions):
    # Perform subdivisions
    for i in xrange(num_subdivisions):
        triangles = subdivide(triangles)
    return triangles


if __name__ == '__main__':
    num_subdivisions = 6
    canvas = Canvas(1000)
    triangles = tiling()
    triangles = elaborate(triangles, num_subdivisions)
    canvas.render(triangles)

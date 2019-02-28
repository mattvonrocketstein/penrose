##
#
##
import logging

from solid.utils import (
    mirror, forward, back, up, down, left, right,
    Black, Blue, Red, Yellow, rotate, scale,
    scad_render, scad_render_to_file)

from solid import (
    cube, sphere,
    union, translate, intersection, linear_extrude, minkowski,
    polygon, color,
    difference, cylinder, OpenSCADObject)


def get_logger(name):
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel('DEBUG')
    return logger

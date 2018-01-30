"""Drawing utilities. A list of functions to draw common elements"""
import bgl
from mathutils import Vector


def draw_line(start, end):
    """Draws a line using two Vector-based points"""
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(start.x, start.y)
    bgl.glVertex2f(end.x, end.y)
    bgl.glEnd()


def draw_arrow_head(center, size, points_right=True):
    """
    Draws a triangular arrow using two Vectors:
    - the triangle's center
    - the triangle's size
    """
    direction = 1 if points_right else -1

    point_upper = Vector([ center.x - size.x/2 * direction, center.y + size.y/2 ])
    point_tip = Vector([ center.x + size.x/2 * direction, center.y ])
    point_lower = Vector([ center.x - size.x/2 * direction, center.y - size.y/2 ])

    draw_line(point_upper, point_tip)
    draw_line(point_tip, point_lower)
# Singledispath doesn't work currently - you get an error if you try register more than 1 type?
# Maybe due to Blender's py3 version?
# from functools import singledispatch
# @singledispatch
# def draw_line(**args):
#     """Fallback for draw_line"""
#     print('Unsupported type, please use one of: {} '.format(draw_line.registry.keys()))


# @draw_line.register(Vector)
# def draw_line(start, end):
#     """Draws an openGL line using two Vector objects"""
#     bgl.glBegin(bgl.GL_LINES)
#     bgl.glVertex2f(start.x, start.y)
#     bgl.glVertex2f(end.x, end.y)
#     bgl.glEnd()


# @draw_line.register(float)
# def draw_line(start_x, start_y, end_x, end_y):
#     """Draws an openGL line with four floats for coordinates"""
#     bgl.glBegin(bgl.GL_LINES)
#     bgl.glVertex2f(start_x, start_y)
#     bgl.glVertex2f(end_x, end_y)
#     bgl.glEnd()

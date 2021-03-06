import pymunk
from pymunk import Vec2d as Vec
from typing import Union, Tuple


def pinjoint(b_a: pymunk.Body, b_b: pymunk.Body, a: Union[Tuple[float, float], Vec] = None,
             b: Union[Tuple[float, float], Vec] = None) -> pymunk.PinJoint:
    """
    :param b_a: First Body you want to attach
    :type b_a: pymunk.Body
    :param b_b Second Body you want to attach
    :type b_b: pymunk.Body
    :param a Place to anchor the First body
    :type a: pymunk.Vec2d
    :param b Place to anchor the Second body
    :type b: pymunk.Vec2d
    :return PinJoint between body_a and body_b through anchor_a and anchor_b
    """
    if a is None:
        anchor_a = pymunk.Vec2d(0, 0)
    else:
        anchor_a = a
    if b is None:
        anchor_b = pymunk.Vec2d(0, 0)
    else:
        anchor_b = b
    body_a = b_a
    body_b = b_b
    joint = pymunk.PinJoint(body_a, body_b, anchor_a, anchor_b)
    return joint


def pivotjoint(b_a: pymunk.Body, b_b: pymunk.Body, a: Union[Tuple[float, float], Vec] = None,
               b: Union[Tuple[float, float], Vec] = None) -> pymunk.PivotJoint:
    """
    :param b_a: First Body you want to attach
    :type b_a: pymunk.Body
    :param b_b Second Body you want to attach
    :type b_b: pymunk.Body
    :param a Place to anchor the First body
    :type a: pymunk.Vec2d
    :param b Place to anchor the Second body
    :type b: pymunk.Vec2d
    :return PinJoint between body_a and body_b through anchor_a and anchor_b
    """
    if a is None:
        anchor_a = pymunk.Vec2d(0, 0)
    else:
        anchor_a = a
    if b is None:
        anchor_b = pymunk.Vec2d(0, 0)
    else:
        anchor_b = b
    body_a = b_a
    body_b = b_b
    joint = pymunk.PivotJoint(body_a, body_b, anchor_a, anchor_b)
    return joint

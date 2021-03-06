import pygame as pg
from math import pi, exp
from pymunk import Vec2d as Vec
from typing import Union, Tuple
# import rsvgwrapper
# import cairo
# from PIL import Image
# import numpy


def blitrotate(image: Union[pg.Surface, pg.SurfaceType], pos: Union[Tuple[float, float], Vec],
               originpos: Union[Tuple[float, float], Vec],
               angle: float) -> Tuple[Union[pg.Surface, pg.SurfaceType], Union[Tuple[float, float], Vec]]:
    """
    :param image: the Surface which has to be rotated and blit
    :param pos: the position of the pivot on the target Surface surf (relative to the top left of surf)
    :param originpos: position of the pivot on the Surface (relative to the top left of sky_image)
    :param angle: the angle of rotation in degrees
    :return:
    """
    # calcaulate the axis aligned bounding box of the rotated sky_image
    w, h = image.get_size()
    box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pg.math.Vector2(originpos[0], -originpos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated sky_image
    origin = Vec(pos.x - originpos.x + min_box[0] - pivot_move[0], pos.y - originpos.y - max_box[1] + pivot_move[1])

    # get parab_a rotated sky_image
    rotated_image = pg.transform.rotate(image, angle)

    return rotated_image, origin


def scale(img: Union[pg.Surface, pg.SurfaceType], original_dimensions: Tuple[int, int] = None,
          zoom: float = 1) -> Union[pg.Surface, pg.SurfaceType]:
    dim = original_dimensions if original_dimensions is not None else img.get_rect().size
    return pg.transform.scale(img, (round(dim[0]*zoom), round(dim[1]*zoom)))


def formated(original: str, value: Union[str, float]) -> str:
    if value is None:
        return original
    else:
        # print(original)
        try:
            return original.format(value)
        except ValueError as error:
            print(error)
            return original


def rad_to_degrees(angle: float) -> float:
    return angle*180/pi


def normalize(x: float) -> float:
    return 1 / (1 + exp(-x + 5))


'''def load_svg(file, size=None):
    """Returns Pygame Image object from rasterized SVG
    :param file: Path to the file
    :param size: the image will be clipped to specified size.
    """
    data = memoryview(numpy.empty(size[0] * size[1] * 4, dtype=numpy.int8))
    cairo_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, size[0], size[1], size[1] * 4)
    svg_graphics = rsvgwrapper.rsvgHandle(file)
    svg_graphics.render_cairo(cairo_surface)
    data_string = bgra_surf_to_rgba_string(cairo_surface)
    return pg.image.frombuffer(data_string, size, 'RGBA')


def bgra_surf_to_rgba_string(cairo_surface):
    # We use PIL to do this
    img = Image.frombuffer(
        'RGBA', (cairo_surface.get_width(),
                 cairo_surface.get_height()),
        cairo_surface.get_data(), 'raw', 'BGRA', 0, 1)

    return img.tostring('raw', 'RGBA', 0, 1)'''

import pygame as pg


def blitrotate(image, pos, originpos, angle):
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
    origin = (pos.x - originpos.x + min_box[0] - pivot_move[0], pos.y - originpos.y - max_box[1] + pivot_move[1])

    # get parab_a rotated sky_image
    rotated_image = pg.transform.rotate(image, angle)

    return rotated_image, origin


def scale(img, zoom):
    return pg.transform.scale(img, (round(img.get_rect().width*zoom), round(img.get_rect().height*zoom)))

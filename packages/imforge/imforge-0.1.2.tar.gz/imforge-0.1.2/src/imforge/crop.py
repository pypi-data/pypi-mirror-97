import math
import operator

# noinspection PyPackageRequirements
import cv2
import numpy as np
import pyclipper
from PIL import Image

from imforge.cut import cut_out as _cut_out
from imforge.utils import is_clockwise


def crop(image, polygon, fillcolor=None, cut_out=False, clip=False):  # noqa: C901
    """
    Crop image according to given (convex) polygon.

    :param PIL.Image.Image image: the (pillow) image to crop
    :param list[tuple[int, int]] polygon: the list of points coordinates of the polygon to crop
    :param fillcolor: the color to use for filling area outside of polygon
    :param bool cut_out: if ``False`` (the default), the fillcolor is only used for filling areas outside of original
      image when doing crop. Il ``True``, then all areas outside of polygon are filled with fillcolor.
    :param bool clip: if ``False`` (the default), the cropped image will include the whole polygon, even if some of its
      coordinates are outside of the original image, which can lead to a large image with areas filled with fillcolor on
      edges of cropped image. If ``True``, the polygon is first clipped to the original image box, thus leading to the
      minimal cropped image containing all the *visible* parts of polygon in original image.
    :return: the cropped image
    :rtype: PIL.Image.Image
    """
    im_width, im_height = image.size
    if cut_out:
        image = image.copy()
        _cut_out(image, polygon, fillcolor=fillcolor)
    if clip:
        rect = ((0, 0), (im_width, 0), (im_width, im_height), (0, im_height))
        pc = pyclipper.Pyclipper()
        pc.AddPath(rect, pyclipper.PT_CLIP, True)
        pc.AddPath(polygon, pyclipper.PT_SUBJECT, True)
        clipped_paths = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
        points = np.array([point for path in clipped_paths for point in path], dtype=np.int32)
    else:
        points = np.array(polygon, dtype=np.int32)
    (center_x, center_y), (width, height), angle = cv2.minAreaRect(points)
    mbr = np.float32(cv2.boxPoints(((center_x, center_y), (width, height), angle))).tolist()

    # search for the mbr point closest to the first polygon point for keeping *orientation* of cropped images as the
    # first polygon point should be the top-left point of the cropped image
    # As we are just comparing distances, we can do comparison on square value of distances. This avoid a costly call to
    # math.sqrt
    def sq_dist(x1, y1, x2, y2):
        return (x2 - x1) ** 2 + (y2 - y1) ** 2

    x, y = polygon[0]
    top_left_dists = [(idx, sq_dist(x, y, mx, my)) for idx, (mx, my) in enumerate(mbr)]
    min_dist_idx = min(top_left_dists, key=operator.itemgetter(1))[0]
    flip = not is_clockwise(polygon, check_convexity=False)
    if min_dist_idx == 0:
        angle -= 90
        width, height = height, width
    # elif min_dist_idx == 1:
    #    the mbr is correctly oriented. No change
    elif min_dist_idx == 2:
        angle += 90
        width, height = height, width
    elif min_dist_idx == 3:
        angle += 180

    # using expand=True in image.rotate assumes that center is the center of image, so it does not give correct result
    # when center is near an image side. This is the reason for the following.
    if angle != 0:  # No need for rotation boilerplate if angle is 0
        matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
        rotated_mbr = cv2.transform(np.array([mbr], dtype=np.float32), matrix).tolist()[0]
        min_x = min_y = 0
        max_x = im_width
        max_y = im_height
        for x, y in rotated_mbr:
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y
        min_x = math.floor(min_x)
        min_y = math.floor(min_y)
        max_x = math.ceil(max_x)
        max_y = math.ceil(max_y)
        if min_x < 0 or min_y < 0 or max_x > im_width or max_y > im_height:
            image = image.transform(
                size=(max_x - min_x, max_y - min_y), method=Image.AFFINE,
                data=(1, 0, min_x, 0, 1, min_y), fillcolor=fillcolor
            )
            center_x -= min_x
            center_y -= min_y
        image = image.rotate(
            angle, resample=Image.BICUBIC, expand=False, center=(center_x, center_y), fillcolor=fillcolor
        )
    left = center_x - width / 2
    top = center_y - height / 2
    right = left + width
    bottom = top + height
    image = image.crop((left, top, right, bottom))
    if flip:
        image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    return image

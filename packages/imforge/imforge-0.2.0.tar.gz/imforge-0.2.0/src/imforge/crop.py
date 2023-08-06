import operator

# noinspection PyPackageRequirements
import cv2
import numpy as np
from PIL import Image

from imforge.cut import cut_out_pil, cut_out_cv2
from imforge.utils import is_clockwise, clip_polygon


def _get_transforms_params(polygon, im_width, im_height, clip=False):  # noqa
    """
    Compute the parameters for the different transformations to apply for cropping polygon in an image of given width
    and height. The following transformations are to be applied on the image from crop:

    * resize the image so that polygon fit in the resulting image after applying rotation
    * apply rotation of image so that polygon MBR is straight and can be cropped
    * crop the rotated MBR

    For each transformation, the following parameters are returned:

    * resize: (left_add, top_add, new_width, new_height) where:

      + left_add is the number of pixels to add on the left of image
      + top_add is the number of pixels to add on the top of image
      + new_width is the width of resized image
      + new_height is the height of resized image

    * rotation: ((center_x, center_y), angle) where:

      + (center_x, center_y) are the coordinates of the rotation center in the resized image referential
      + angle is the rotation angle to apply

    * crop: (left, top, right, bottom) where:

      + (left, top) are the coordinates of the top-left point of crop box in rotated image
      + (bottom, right) are the coordinates of the bottom-right point of the crop box in rotated image

    :param list[tuple[int,int]] polygon: the list of points coordinates of the polygon to crop
    :param int im_width: image width
    :param int im_height: image height
    :param bool clip: if ``False`` (the default), the cropped image will include the whole polygon, even if some of its
      coordinates are outside of the original image, which can lead to a large image with areas filled with fillcolor on
      edges of cropped image. If ``True``, the polygon is first clipped to the original image box, thus leading to the
      minimal cropped image containing all the *visible* parts of polygon in original image.
    :return: parameters of the transformations to apply for crop in the form
      ((left_add, top_add, new_width, new_height), ((center_x, center_y), angle), (left, top, width, height))
    :rtype: tuple[tuple[int,int,int,int],tuple[tuple[float,float],float],tuple[int,int,int,int]]
    """
    points = np.array(clip_polygon(polygon, im_width, im_height) if clip else polygon, dtype=np.int0)
    (center_x, center_y), (width, height), angle = cv2.minAreaRect(points)
    # The rectangle seems to be computed so that right and bottom edges are not included. So increase width / height
    # This can be seen with a polygon being a straight rectangle ((0, 0), (im.width - 1, im.height - 1))
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
    if min_dist_idx == 0:
        angle -= 90
    # elif min_dist_idx == 1:
    #    the mbr is correctly oriented. No change
    elif min_dist_idx == 2:
        angle += 90
    elif min_dist_idx == 3:
        angle += 180

    if angle != 0:  # No need for rotation boilerplate if angle is 0
        matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
        rotated_mbr = cv2.transform(np.array([mbr], dtype=np.float32), matrix).tolist()[0]
    else:
        rotated_mbr = mbr
    left = top = float("inf")
    right = bottom = float("-inf")
    for x, y in rotated_mbr:
        if x < left:
            left = x
        elif x > right:
            right = x
        if y < top:
            top = y
        elif y > bottom:
            bottom = y
    left = round(left)
    right = round(right)
    top = round(top)
    bottom = round(bottom)
    left_add = top_add = 0
    new_width = im_width
    new_height = im_height
    if left < 0:
        left_add = -left
        left = 0
        center_x += left_add
        right += left_add
        new_width += left_add
    if right >= new_width:
        new_width = right + 1  # Add 1 so that right edge is included in image
    if top < 0:
        top_add = -top
        top = 0
        center_y += top_add
        bottom += top_add
        new_height += top_add
    if bottom >= new_height:
        new_height = bottom + 1  # Add 1 so that bottom edge is included in image

    return (
        (left_add, top_add, new_width, new_height),
        ((center_x, center_y), angle),
        (left, top, right, bottom)
    )


def crop_pil(image, polygon, fillcolor=None, cut_out=False, clip=False):
    """
    Crop image according to given (convex) polygon.

    .. note::

       All edges of the polygon are included in the cropped image. This is not the same behaviour as
       :py:meth:`PIL.Image.Image.crop` when using a straight rectangular crop box because the ``right`` and ``bottom``
       coordinates are not included in the cropped image.

    :param PIL.Image.Image image: the (pillow) image to crop
    :param list[tuple[int,int]] polygon: the list of points coordinates of the polygon to crop
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
        cut_out_pil(image, polygon, fillcolor=fillcolor)

    flip = not is_clockwise(polygon, check_convexity=False)
    # using expand=True in PIL.Image.Image.rotate assumes that center is the center of image, so it does not give
    # correct result when center is near an image side. This is the reason why we manually apply a first transform to
    # resize image before rotation and crop.
    resize_params, rotate_params, crop_params = _get_transforms_params(polygon, im_width, im_height, clip=clip)
    _, angle = rotate_params
    left_add, top_add, new_width, new_height = resize_params
    if left_add > 0 or top_add > 0 or new_width > im_width or new_height > im_height:
        image = image.transform(
            size=(new_width, new_height), method=Image.AFFINE, data=(1, 0, -left_add, 0, 1, -top_add),
            fillcolor=fillcolor
        )
    left, top, right, bottom = crop_params
    if angle != 0:
        # recompute center because the center computed by minAreaRect seems not to be the exact center (as if right and
        # bottom edges of the rectangle are not included in the crop box). PIL.Image.rotate requires the exact center
        center = (left + (right + 1 - left) / 2, top + (bottom + 1 - top) / 2)
        image = image.rotate(angle, resample=Image.BICUBIC, expand=False, center=center, fillcolor=fillcolor)
    # Add 1 to include right and bottom edges in the cropped image
    image = image.crop((left, top, right + 1, bottom + 1))
    if flip:
        image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    return image


def crop_cv2(image, polygon, fillcolor=None, cut_out=False, clip=False):
    """
    Crop image according to given (convex) polygon.

    .. note::

       All edges of the polygon are included in the cropped image. This is not the same behaviour as
       :py:meth:`PIL.Image.Image.crop` when using a straight rectangular crop box because the ``right`` and ``bottom``
       coordinates are not included in the cropped image.

    :param numpy.ndarray image: the (opencv) image to crop
    :param list[tuple[int,int]] polygon: the list of points coordinates of the polygon to crop
    :param fillcolor: the color to use for filling area outside of polygon
    :param bool cut_out: if ``False`` (the default), the fillcolor is only used for filling areas outside of original
      image when doing crop. Il ``True``, then all areas outside of polygon are filled with fillcolor.
    :param bool clip: if ``False`` (the default), the cropped image will include the whole polygon, even if some of its
      coordinates are outside of the original image, which can lead to a large image with areas filled with fillcolor on
      edges of cropped image. If ``True``, the polygon is first clipped to the original image box, thus leading to the
      minimal cropped image containing all the *visible* parts of polygon in original image.
    :return: the cropped image
    :rtype: numpy.ndarray
    """
    im_height, im_width = image.shape[:2]
    if cut_out:
        image = image.copy()
        cut_out_cv2(image, polygon, fillcolor=fillcolor)

    flip = not is_clockwise(polygon, check_convexity=False)
    resize_params, rotate_params, crop_params = _get_transforms_params(polygon, im_width, im_height, clip=clip)
    center, angle = rotate_params
    if fillcolor is None:
        fillcolor = 0
    left_add, top_add, new_width, new_height = resize_params
    if left_add > 0 or top_add > 0 or new_width > im_width or new_height > im_height:
        new_image = np.empty((new_height, new_width, *image.shape[2:]), dtype=image.dtype)
        new_image[:, :] = fillcolor
        new_image[top_add:top_add+im_height, left_add:left_add+im_width] = image
        image = new_image

    if angle != 0:
        matrix = cv2.getRotationMatrix2D(center, angle, 1)
        image = cv2.warpAffine(
            image, matrix, (new_width, new_height), flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT, borderValue=fillcolor
        )
    left, top, right, bottom = crop_params
    # Add 1 to include right and bottom edges in the cropped image
    image = image[top:bottom + 1, left:right + 1]
    if flip:
        image = cv2.flip(cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
    return image


def crop(image, polygon, fillcolor=None, cut_out=False, clip=False):
    """
    Crop image according to given (convex) polygon.

    .. note::

       All edges of the polygon are included in the cropped image. This is not the same behaviour as
       :py:meth:`PIL.Image.Image.crop` when using a straight rectangular crop box because the ``right`` and ``bottom``
       coordinates are not included in the cropped image.

    :param image: the (pillow) image to crop
    :type image: Union[PIL.Image.Image,numpy.ndarray]
    :param list[tuple[int,int]] polygon: the list of points coordinates of the polygon to crop
    :param fillcolor: the color to use for filling area outside of polygon
    :param bool cut_out: if ``False`` (the default), the fillcolor is only used for filling areas outside of original
      image when doing crop. Il ``True``, then all areas outside of polygon are filled with fillcolor.
    :param bool clip: if ``False`` (the default), the cropped image will include the whole polygon, even if some of its
      coordinates are outside of the original image, which can lead to a large image with areas filled with fillcolor on
      edges of cropped image. If ``True``, the polygon is first clipped to the original image box, thus leading to the
      minimal cropped image containing all the *visible* parts of polygon in original image.
    :return: the cropped image, in same format as input image
    :rtype: Union[PIL.Image.Image,numpy.ndarray]
    """
    if isinstance(image, Image.Image):
        return crop_pil(image, polygon, fillcolor=fillcolor, cut_out=cut_out, clip=clip)
    else:
        return crop_cv2(image, polygon, fillcolor=fillcolor, cut_out=cut_out, clip=clip)

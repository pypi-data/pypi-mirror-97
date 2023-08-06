# noinspection PyPackageRequirements
import cv2
import numpy as np
from PIL import Image, ImageDraw


def cut_out(image, *polygons, fillcolor=None):
    """
    Cut out the areas delimited by given list of polygons: i.e. fill image pixels outside of given polygons with the
    given fill color.

    :param image: the image to cut out
    :type image: Union[PIL.Image.Image,numpy.ndarray]
    :param list[tuple[int,int]] polygons: the polygons to cut out
    :param fillcolor: the color to use for filling area outside of polygons
    """
    if isinstance(image, Image.Image):
        cut_out_pil(image, *polygons, fillcolor=fillcolor)
    else:
        cut_out_cv2(image, *polygons, fillcolor=fillcolor)


def cut_out_pil(image, *polygons, fillcolor=None):
    """
    Cut out the areas delimited by given list of polygons: i.e. fill image pixels outside of given polygons with the
    given fill color.

    :param PIL.Image.Image image: the image to cut out
    :param list[tuple[int,int]] polygons: the polygons to cut out
    :param fillcolor: the color to use for filling area outside of polygons
    """
    if polygons:
        mask = Image.new(mode="1", size=image.size, color=255)
        draw = ImageDraw.ImageDraw(mask)
        for polygon in polygons:
            draw.polygon(polygon, fill=0, outline=0)
        if fillcolor is None:
            fillcolor = 0
        image.paste(fillcolor, mask=mask)


def cut_out_cv2(image, *polygons, fillcolor=None):
    """
    Cut out the areas delimited by given list of polygons: i.e. fill image pixels outside of given polygons with the
    given fill color.

    :param numpy.ndarray image: the numpy array representing the image
    :param list[tuple[int,int]] polygons: the polygons to cut out
    :param fillcolor: the color to use for filling area outside of polygons
    """
    if polygons:
        if fillcolor is None:
            fillcolor = 0
        background = np.empty_like(image)
        background[:, :] = fillcolor
        mask = np.full(image.shape[:2], 0, dtype=np.uint8)
        polygons = [np.array(poly) for poly in polygons]
        cv2.fillPoly(mask, polygons, color=255, lineType=cv2.LINE_AA)
        image[:] = cv2.add(
            cv2.bitwise_and(image, image, mask=mask),
            cv2.bitwise_and(background, background, mask=cv2.bitwise_not(mask))
        )

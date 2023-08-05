from PIL import Image, ImageDraw


def cut_out(image, *polygons, fillcolor=None):
    """
    Cut out the areas delimited by given list of polygons: i.e. fill image pixels outside of given polygons with the
    given fill color.

    :param PIL.Image.Image image: the image to cut out
    :param list[tuple[int, int]] polygons: the polygons to cut out
    :param fillcolor: he color to use for filling area outside of polygons
    """
    if polygons:
        mask = Image.new(mode="1", size=image.size, color=255)
        draw = ImageDraw.ImageDraw(mask)
        for polygon in polygons:
            draw.polygon(polygon, fill=0, outline=0)
        if fillcolor is None:
            fillcolor = 0
        image.paste(fillcolor, mask=mask)

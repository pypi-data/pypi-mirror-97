Cut
===

The :py:mod:`imforge.cut` module contains functions for cutting areas of images.

* :py:func:`imforge.cut.cut_out`:

  Cut out the areas delimited by a given list of polygons: i.e. fill image pixels outside of given polygons with the
  given fill color.

  The input image is modified in place.

  Sample usage:

  .. code-block:: python

     from PIL import Image
     from imforge.crop import crop

     with Image.open("/path/to/image.jpg") as image:
         # with a single polygon and default color (black)
         polygon = [(15, 8), (368, 78), (325, 161), (14, 71)]
         cut_out(image, polygon)
         # with multiple polygons and purple color
         polygons = (
            [(15, 8), (368, 78), (325, 161), (14, 71)],
            [(100, 0), (150, 0), (125, 20)],
            [(0, 150), (200, 150), (200, 178), (0, 178)],
        )
        cut_out(image, *polygons, fillcolor=(255, 0, 255))

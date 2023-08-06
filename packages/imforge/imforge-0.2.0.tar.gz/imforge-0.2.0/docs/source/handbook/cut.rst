Cut
===

The :py:mod:`imforge.cut` module contains functions for cutting areas of images.

* :py:func:`imforge.cut.cut_out`:

  Cut out the areas delimited by a given list of polygons: i.e. fill image pixels outside of given polygons with the
  given fill color.

  The input image is modified in place.

  .. note::

     The fill color is not necessarily an RGB color. It depends on the color space of the processed image.
     In particular, OpenCv images are usually opened in BGR mode, so the fill color must be a BGR value in such case.

  Sample (pillow) usage:

  .. code-block:: python

     from PIL import Image
     from imforge.cut import cut_out

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

  .. note::

     Calling :py:func:`imforge.cut.cut_out` with a :py:class:`PIL image<PIL.Image.Image>` is the same as calling
     :py:func:`imforge.cut.cut_out_pil`.

  Sample (opencv) usage:

  .. code-block:: python

     import cv2
     from imforge.cut import cut_out

     image = cv2.imread("/path/to/image.jpg", cv2.IMREAD_UNCHANGED)
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

  .. note::

     Calling :py:func:`imforge.cut.cut_out` with an OpenCv image (i.e. a :py:class:`NumPy array<numpy.ndarray>`) is the
     same as calling :py:func:`imforge.cut.cut_out_cv2`.

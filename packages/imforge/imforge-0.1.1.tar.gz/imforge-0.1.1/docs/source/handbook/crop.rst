Crop
====

The :py:mod:`imforge.crop` module contains functions for image cropping.

* :py:func:`imforge.crop.crop`:

  Crop an image according to a given (convex) polygon. The polygon is first approximated to the minimum area rectangle
  containing the polygon. Then image is cropped so that the crop result correspond to this rectangle.

  The crop rectangle may have some parts outside original image, in which case corresponding parts are filled in with
  the `fillcolor` value passed to the function (if not given, the fill color is black).

  It's also possible to fill area outside of given polygon (but inside crop rectangle) with the `fillcolor` value by
  setting `cut_out` parameter to `True`.

  Finally, if the crop rectangle has complete edges out of the original image, it may be clipped to the extent of
  original image (so that resulting cropped image has a the minimum possible area filled with the `fillcolor`) by
  setting `clip` parameter to `True`.

  The first point of the polygon is considered as being the closer to the top-left corner of the cropped image. If
  polygon is oriented clockwise, the cropped image have same orientation as original image. If polygon is oriented
  counter-clockwise, the cropped image is flipped (as if it was seen from the back of the original image).

  Sample usage:

  .. code-block:: python

     from PIL import Image
     from imforge.crop import crop

     with Image.open("/path/to/image.jpg") as image:
         crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
         # out of image area is filled with default fillcolor (black)
         # original image pixels out of crop_box but inside result cropped image are left as is
         cropped_image = crop(image, crop_box)
         #
         crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
         # Out of image area is filled with purple color
         # original image pixels out of crop_box are also replaced with purple color
         # the crop box is clipped to original image size to minify the filled area in cropped image
         cropped_image = crop(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)

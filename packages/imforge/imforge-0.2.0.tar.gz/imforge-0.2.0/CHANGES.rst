Changelog (ImForge)
===================

0.2.0 (2021-03-07)
------------------

* Add support for OpenCv images (i.e. numpy arrays) to :py:func:`imforge.crop.crop` and :py:func:`imforge.cut.cut_out`
  functions.

0.1.2 (2021-03-03)
------------------

Initial version of the library with following functionalities:

* :py:func:`imforge.crop.crop`: crop a part (not necessarily a straight rectangle) of an image.
* :py:func:`imforge.cut.cut_out`: cut out image areas delimited by some polygons, by filling image pixels outside of
  those polygons with a fill color.

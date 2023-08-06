Geometry and colors
===================

Geometry
--------

Transformations
~~~~~~~~~~~~~~~

.. currentmodule:: djvu.decode
.. class:: AffineTransform((x0, y0, w0, h0), (x1, y1, w1, h1))

   The object represents an affine coordinate transformation that maps points
   from rectangle (`x0`, `y0`, `w0`, `h0`) to rectangle (`x1`, `y1`, `w1`, `h1`).

   .. method:: rotate(n)

      Rotate the output rectangle counter-clockwise by `n` degrees.

   .. method:: apply((x, y))
               apply((x, y, w, h))

      Apply the coordinate transform to a point or a rectangle.

   .. method:: inverse((x, y))
               inverse((x, y, w, h))

      Apply the inverse coordinate transform to a point or a rectangle.

   .. method:: mirror_x()

      Reverse the X coordinates of the output rectangle.

   .. method:: mirror_y()

      Reverse the Y coordinates of the output rectangle.

Pixel formats
-------------

.. currentmodule:: djvu.decode
.. class:: PixelFormat

   Abstract base for all pixel formats.

   Inheritance diagram:

      .. inheritance-diagram::
         PixelFormatRgb
         PixelFormatRgbMask
         PixelFormatGrey
         PixelFormatPalette
         PixelFormatPackedBits
         :parts: 1

   .. attribute:: rows_top_to_bottom

      Flag indicating whether the rows in the pixel buffer are stored
      starting from the top or the bottom of the image.

      Default ordering starts from the bottom of the image. This is the
      opposite of the X11 convention.

   .. attribute:: y_top_to_bottom

      Flag indicating whether the *y* coordinates in the drawing area are
      oriented from bottom to top, or from top to bottom.

      The default is bottom to top, similar to PostScript. This is the
      opposite of the X11 convention.

   .. attribute:: bpp

      Return the depth of the image, in bits per pixel.

   .. attribute:: dither_bpp

      The final depth of the image on the screen. This is used to decide
      which dithering algorithm should be used.

      The default is usually appropriate.

   .. attribute:: gamma

      Gamma of the display for which the pixels are intended. This will be
      combined with the gamma stored in DjVu documents in order to compute
      a suitable color correction.

      The default value is 2.2.

.. currentmodule:: djvu.decode
.. class:: PixelFormatRgb([byteorder='RGB'])

   24-bit pixel format, with:

   - RGB (`byteorder` = ``'RGB'``) or
   - BGR (`byteorder` = ``'BGR'``)

   byte order.

.. currentmodule:: djvu.decode
.. class::
   PixelFormatRgbMask(red_mask, green_mask, blue_mask[, xor_value], bpp=16)
   PixelFormatRgbMask(red_mask, green_mask, blue_mask[, xor_value], bpp=32)

   `red_mask`, `green_mask` and `blue_mask` are bit masks for color components
   for each pixel. The resulting color is then xored with the `xor_value`.

   For example, ``PixelFormatRgbMask(0xF800, 0x07E0, 0x001F, bpp=16)`` is a
   highcolor format with:

   - 5 (most significant) bits for red,
   - 6 bits for green,
   - 5 (least significant) bits for blue.

.. currentmodule:: djvu.decode
.. class:: PixelFormatGrey()

   8-bit, grey pixel format.

.. currentmodule:: djvu.decode
.. class:: PixelFormatPalette(palette)

   Palette pixel format.

   `palette` must be a dictionary which contains 216 (6 × 6 × 6)
   entries of a web color cube, such that:

   - for each key ``(r, g, b)``: ``r in range(0, 6)``, ``g in range(0, 6)`` etc.;
   - for each value ``v``: ``v in range(0, 0x100)``.

.. currentmodule:: djvu.decode
.. class:: PixelFormatPackedBits(endianness)

   Bitonal, 1 bit per pixel format with:

   - most significant bits on the left (*endianness* = ``'>'``) or
   - least significant bits on the left (*endianness* = ``'<'``).

Render modes
------------

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_COLOR

   Render color page or stencil.

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_BLACK

   Render stencil or color page.

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_COLOR_ONLY

   Render color page or fail.

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_MASK_ONLY

   Render stencil or fail.

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_BACKGROUND

   Render color background layer.

.. currentmodule:: djvu.decode
.. data:: djvu.decode.RENDER_FOREGROUND

   Render color foreground layer.

.. vim:ts=3 sts=3 sw=3 et

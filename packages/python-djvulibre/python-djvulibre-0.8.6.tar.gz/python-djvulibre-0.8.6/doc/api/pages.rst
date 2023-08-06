Document pages
==============

.. currentmodule:: djvu.decode
.. class:: DocumentPages

   Pages of a document.

   Use :attr:`Document.pages` to obtain instances of this class.

   Page indexing is zero-based, i.e. :attr:`~Document.pages`\ ``[0]`` stands for the first page.

   ``len(pages)`` might return 1 when called before receiving a :class:`DocInfoMessage`.


.. currentmodule:: djvu.decode
.. class:: Page

   Page of a document.

   Use :attr:`Document.pages`\ ``[N]`` to obtain instances of this class.

   .. attribute:: document

      :rtype: :class:`Document`

   .. attribute:: file

      :return: a file associated with the page.
      :rtype: :class:`File`.

   .. attribute:: n

      :return: the page number.

      Page indexing is zero-based, i.e. 0 stands for the very first page.

   .. attribute:: thumbnail

      :return: a thumbnail for the page.
      :rtype: :class:`Thumbnail`.

   .. method:: get_info([wait=1])

      Attempt to obtain information about the page without decoding the page.

      If `wait` is true, wait until the information is available.

      If the information is not available, raise :exc:`NotAvailable` exception.
      Then, start fetching the page data, which causes emission of
      :class:`PageInfoMessage` messages with empty
      :attr:`~Message.page_job`.

      :raise NotAvailable: see above.
      :raise JobFailed: on failure.

   .. attribute:: width

      :return: the page width, in pixels.
      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: height

      :return: the page height, in pixels.

      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: size

      :return: ``(page.width, page.height)``

      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: dpi

      :return: the page resolution, in pixels per inch.

      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: rotation

      :return: the initial page rotation, in degrees.
      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: version

      :return: the page version.

      :raise NotAvailable: see :meth:`get_info`.
      :raise JobFailed: on failure.

   .. attribute:: dump

      :return:
        a text describing the contents of the page using the same format as the
        ``djvudump`` command.

      If the information is not available, raise :exc:`NotAvailable` exception.
      Then :class:`PageInfoMessage` messages with empty
      :attr:`~Message.page_job` may be emitted.

      :raise NotAvailable: see above.

   .. method:: decode([wait=1])

      Initiate data transfer and decoding threads for the page.

      If `wait` is true, wait until the job is done.

      :rtype: :class:`PageJob`.
      :raise NotAvailable: if called before receiving the :class:`DocInfoMessage`.
      :raise JobFailed: if document decoding failed.

   .. attribute:: annotations

      :rtype: :class:`PageAnnotations`

   .. attribute:: text

      :rtype: :class:`PageText`

.. class:: PageJob

   Inheritance diagram:

      .. inheritance-diagram::
         PageJob
         :parts: 1

   A page decoding job.

   Use :meth:`Page.decode` to obtain instances of this class.

   .. attribute:: width

      :return: the page width in pixels.
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: height

      :return: the page height in pixels.
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: size

      :return: ``(page_job.width, page_job.height)``
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: dpi

      :return: the page resolution in pixels per inch.
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: gamma

      :return: the gamma of the display for which this page was designed.
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: version

      :return: the version of the DjVu file format.
      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: type

      :return: the type of the page data.

      Possible values are:

      .. data:: PAGE_TYPE_UNKNOWN
      .. data:: PAGE_TYPE_BITONAL
      .. data:: PAGE_TYPE_PHOTO
      .. data:: PAGE_TYPE_COMPOUND

      :raise NotAvailable: before receiving a :class:`PageInfoMessage`.

   .. attribute:: initial_rotation

      :return:
         the counter-clockwise page rotation angle (in degrees) specified by
         the orientation flags in the DjVu file.

      .. warning::
         This is useful because ``maparea`` coordinates in the annotation
         chunks are expressed relative to the rotated coordinates whereas text
         coordinates in the hidden text data are expressed relative to the
         unrotated coordinates.

   .. attribute:: rotation

      :return: the counter-clockwise rotation angle (in degrees) for the page.

      The rotation is automatically taken into account by :meth:`render` method
      and :attr:`width` and :attr:`height` properties.

   .. method:: render(self, mode, page_rect, render_rect, pixel_format[, row_alignment=1][, buffer=None])

      Render a segment of a page with arbitrary scale. `mode` indicates
      which image layers should be rendered:

      * :data:`~djvu.decode.RENDER_COLOR`, or
      * :data:`~djvu.decode.RENDER_BLACK`, or
      * :data:`~djvu.decode.RENDER_COLOR_ONLY`, or
      * :data:`~djvu.decode.RENDER_MASK_ONLY`, or
      * :data:`~djvu.decode.RENDER_BACKGROUND`, or
      * :data:`~djvu.decode.RENDER_FOREGROUND`.

      Conceptually this method renders the full page into a rectangle
      `page_rect` and copies the pixels specified by rectangle
      `render_rect` into a buffer. The actual code is much more efficient
      than that.

      `pixel_format` (a :class:`~djvu.decode.PixelFormat` instance) specifies
      the expected pixel format. Each row will start at `row_alignment` bytes
      boundary.

      Data will be saved to the provided buffer or to a newly created string.

      This method makes a best effort to compute an image that reflects the
      most recently decoded data.

      :raise NotAvailable:
         to indicate that no image could be computed at this point.

.. currentmodule:: djvu.decode
.. class:: Thumbnail

   Thumbnail for a page.

   Use :attr:`Page.thumbnail` to obtain instances of this class.

   .. attribute:: page

      :return: the page.

   .. attribute:: status

      Determine whether the thumbnail is available.

      :return: a :exc:`JobException` subclass indicating the current job
         status.

   .. method:: calculate()

      Determine whether the thumbnail is available. If it's not, initiate the
      thumbnail calculating job. Regardless of its success, the completion of
      the job is signalled by a subsequent :class:`ThumbnailMessage`.

      Return a :exc:`JobException` subclass indicating the current job status.

   .. method:: render((w0, h0)[, pixel_format][, row_alignment=1][, dry_run=False][, buffer=None])

      Render the thumbnail:

      * not larger than `w0` × `h0` pixels;
      * using the `pixel_format` (a :class:`~djvu.decode.PixelFormat` instance)
        pixel format;
      * with each row starting at `row_alignment` bytes boundary;
      * into the provided buffer or to a newly created string.

      :return: a ((`w1`, `h1`, `row_size`), `data`) tuple.

      * `w1` and `h1` are actual thumbnail dimensions in pixels
        (`w1` ≤ `w0` and `h1` ≤ `h0`);
      * `row_size` is length of each image row, in bytes;
      * `data` is ``None`` if `dry_run` is true; otherwise is contains the
        actual image data.

      :raise NotAvailable: when no thumbnail is available.

.. vim:ts=3 sts=3 sw=3 et

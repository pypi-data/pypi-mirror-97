DjVu documents
==============

.. currentmodule:: djvu.decode
.. class:: Document

   DjVu document.

   Use :meth:`Context.new_document` to obtain instances of this class.

   .. attribute:: decoding_status

        :return: a :exc:`JobException` subclass indicating the decoding job
                 status.

   .. attribute:: decoding_error

      Indicate whether the decoding job failed.

   .. attribute:: decoding_done

      Indicate whether the decoding job is done.

   .. attribute:: decoding_job

      :rtype: :exc:`DocumentDecodingJob`

   .. attribute:: type

      :return: the type of the document.

      The following values are possible:

         :data:`~djvu.decode.DOCUMENT_TYPE_UNKNOWN`

         :data:`~djvu.decode.DOCUMENT_TYPE_SINGLE_PAGE`

            single-page document

         :data:`~djvu.decode.DOCUMENT_TYPE_BUNDLED`

            bundled multi-page document

         :data:`~djvu.decode.DOCUMENT_TYPE_INDIRECT`

            indirect multi-page document

         :data:`~djvu.decode.DOCUMENT_TYPE_OLD_BUNDLED`

            (obsolete)

         :data:`~djvu.decode.DOCUMENT_TYPE_OLD_INDEXED`

            (obsolete)

      Before receiving the :class:`DocInfoMessage`, :data:`~djvu.decode.DOCUMENT_TYPE_UNKNOWN` may be returned.

   .. attribute:: pages

        :rtype: :class:`DocumentPages`.

   .. attribute:: files

        :rtype: :class:`DocumentFiles`.

   .. attribute:: outline

        :rtype: :class:`DocumentOutline`.

   .. attribute:: annotations

        :rtype: :class:`DocumentAnnotations`.

   .. method::
      save(file[, pages][, wait=True])
      save(indirect[, pages][, wait=True])

      Save the document as:

      * a bundled DjVu `file` or;
      * an indirect DjVu document with index file name `indirect`.

      `pages` argument specifies a subset of saved pages.

      If `wait` is true, wait until the job is done.

      :rtype: :class:`SaveJob`.

   .. method:: export_ps(file[, …][, wait=True])

      Convert the document into PostScript.

      `pages` argument specifies a subset of saved pages.

      If `wait` is true, wait until the job is done.

      Additional options:

      `eps`
         Produce an *Encapsulated* PostScript file. Encapsulated PostScript
         files are suitable for embedding images into other documents.
         Encapsulated PostScript file can only contain a single page.
         Setting this option overrides the options `copies`, `orientation`,
         `zoom`, `crop_marks`, and `booklet`.
      `level`
         Selects the language level of the generated PostScript. Valid
         language levels are 1, 2, and 3. Level 3 produces the most compact
         and fast printing PostScript files. Some of these files however
         require a very modern printer. Level 2 is the default value. The
         generated PostScript files are almost as compact and work with all
         but the oldest PostScript printers. Level 1 can be used as a last
         resort option.
      `orientation`
         Specifies the pages orientation:

         :data:`~djvu.decode.PRINT_ORIENTATION_AUTO`

            automatic

         :data:`~djvu.decode.PRINT_ORIENTATION_LANDSCAPE`

            portrait

         :data:`~djvu.decode.PRINT_ORIENTATION_PORTRAIT`

            landscape

      `mode`
         Specifies how pages should be decoded:

         :data:`~djvu.decode.RENDER_COLOR`
             render all the layers of the DjVu documents
         :data:`~djvu.decode.RENDER_BLACK`
             render only the foreground layer mask
         :data:`~djvu.decode.RENDER_FOREGROUND`
             render only the foreground layer
         :data:`~djvu.decode.RENDER_BACKGROUND`
             render only the background layer

      `zoom`
         Specifies a zoom factor. The default zoom factor scales the image to
         fit the page.
      `color`
         Specifies whether to generate a color or a gray scale PostScript
         file. A gray scale PostScript files are smaller and marginally more
         portable.
      `srgb`
         The default value, True, generates a PostScript file using device
         independent colors in compliance with the sRGB specification.
         Modern printers then produce colors that match the original as well
         as possible. Specifying a false value generates a PostScript file
         using device dependent colors. This is sometimes useful with older
         printers. You can then use the `gamma` option to tune the output
         colors.
      `gamma`
         Specifies a gamma correction factor for the device dependent
         PostScript colors. Argument must be in range 0.3 to 5.0. Gamma
         correction normally pertains to cathodic screens only. It gets
         meaningful for printers because several models interpret device
         dependent RGB colors by emulating the color response of a cathodic
         tube.
      `copies`
         Specifies the number of copies to print.
      `frame`,
         If true, generate a thin gray border representing the boundaries of
         the document pages.
      `crop_marks`
         If true, generate crop marks indicating where pages should be cut.
      `text`
         Generate hidden text. This option is deprecated. See also the
         warning below.
      `booklet`
         :data:`~djvu.decode.PRINT_BOOKLET_NO`

            Disable booklet mode. This is the default.

         :data:`~djvu.decode.PRINT_BOOKLET_YES`

            Enable recto/verse booklet mode.

         :data:`~djvu.decode.PRINT_BOOKLET_RECTO`

            Enable recto booklet mode.

         :data:`~djvu.decode.PRINT_BOOKLET_VERSO`

            Enable verso booklet mode.

      `booklet_max`
         Specifies the maximal number of pages per booklet. A single printout
         might then be composed of several booklets. The argument is rounded
         up to the next multiple of 4. Specifying 0 sets no maximal number
         of pages and ensures that the printout will produce
         a single booklet. This is the default.
      `booklet_align`
         Specifies a positive or negative offset applied to the verso of
         each sheet. The argument is expressed in points [1]_. This is useful
         with certain printers to ensure that both recto and verso are
         properly aligned. The default value is 0.
      `booklet_fold` (= `(base, increment)`)
         Specifies the extra margin left between both pages on a single
         sheet. The base value is expressed in points [1]_. This margin is
         incremented for each outer sheet by value expressed in millipoints.
         The default value is (18, 200).

      .. [1] 1 pt = :math:`\frac1{72}` in = 0.3528 mm

.. currentmodule:: djvu.decode
.. class:: SaveJob

   Inheritance diagram:

      .. inheritance-diagram::
         SaveJob
         :parts: 1

   Document saving job.

   Use :meth:`Document.save` to obtain instances of this class.

.. currentmodule:: djvu.decode
.. class:: DocumentDecodingJob

   Inheritance diagram:

      .. inheritance-diagram::
         DocumentDecodingJob
         :parts: 1

   Document decoding job.

   Use :attr:`Document.decoding_job` to obtain instances of this class.

.. vim:ts=3 sts=3 sw=3 et

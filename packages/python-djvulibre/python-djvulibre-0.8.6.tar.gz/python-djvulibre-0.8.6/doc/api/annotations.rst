Annotations
===========

.. testsetup::

   from djvu.decode import *
   from djvu.const import *

.. seealso::

   - |djvu3ref|_: 8.3.4 *Annotation Chunk*;
   - |djvused|_: *Annotation syntax*.

.. currentmodule:: djvu.decode
.. class:: Annotations

   Abstract base for document and page annotations.

   Inheritance diagram:

      .. inheritance-diagram::
         DocumentAnnotations
         PageAnnotations
         :parts: 1

   .. method:: wait()

      Wait until the associated S-expression is available.

   .. attribute:: sexpr

      :return: the associated S-expression.
      :rtype: :class:`djvu.sexpr.Expression`.


      :raise NotAvailable:
         if the S-expression is not available;
         then, :class:`PageInfoMessage` messages with empty
         :attr:`~Message.page_job` may be emitted.
      :raise JobFailed: on failure.

.. currentmodule:: djvu.decode
.. class:: DocumentAnnotations(document[, shared=True])


   If `shared` is true and no document-wide annotations are available, shared
   annotations are considered document-wide.

   .. seealso::
      |djvuext|_: *Document annotations and metadata*.

   .. attribute:: document

      :return: the concerned document.
      :rtype: :class:`Document`.

.. currentmodule:: djvu.decode
.. class:: PageAnnotations(page)

   .. attribute:: page

      :return: the concerned page.
      :rtype: :class:`Page`.


Mapareas (overprinted annotations)
----------------------------------
.. seealso::
   |djvu3ref|_: 8.3.4.2 *Maparea (overprinted annotations)*.

.. class:: Hyperlinks(annotations)

   A sequence of ``(maparea …)`` S-expressions.

.. currentmodule:: djvu.decode

The following symbols are pre-defined:

   .. data:: ANNOTATION_MAPAREA

      >>> ANNOTATION_MAPAREA
      Symbol('maparea')

   .. data:: MAPAREA_SHAPE_RECTANGLE

      >>> MAPAREA_SHAPE_RECTANGLE
      Symbol('rect')

   .. data:: MAPAREA_SHAPE_OVAL

      >>> MAPAREA_SHAPE_OVAL
      Symbol('oval')

   .. data:: MAPAREA_SHAPE_POLYGON

      >>> MAPAREA_SHAPE_POLYGON
      Symbol('poly')

   .. data:: MAPAREA_SHAPE_LINE

      >>> MAPAREA_SHAPE_LINE
      Symbol('line')

   .. data:: MAPAREA_SHAPE_TEXT

      >>> MAPAREA_SHAPE_TEXT
      Symbol('text')

   .. data:: MAPAREA_URI

      >>> MAPAREA_URI
      Symbol('url')

   .. data:: MAPAREA_URL

      Equivalent to :data:`MAPAREA_URI`.

Border style
~~~~~~~~~~~~
.. seealso::
   |djvu3ref|_: 8.3.4.2.3.1.1 *Border type*, 8.3.4.2.3.1.2 *Border always
   visible*.

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: MAPAREA_BORDER_NONE

      >>> MAPAREA_BORDER_NONE
      Symbol('none')

   .. data:: MAPAREA_BORDER_XOR

      >>> MAPAREA_BORDER_XOR
      Symbol('xor')

   .. data:: MAPAREA_BORDER_SOLID_COLOR

      >>> MAPAREA_BORDER_SOLID_COLOR
      Symbol('border')

   .. data:: MAPAREA_BORDER_SHADOW_IN

      >>> MAPAREA_BORDER_SHADOW_IN
      Symbol('shadow_in')

   .. data:: MAPAREA_BORDER_SHADOW_OUT

      >>> MAPAREA_BORDER_SHADOW_OUT
      Symbol('shadow_out')

   .. data:: MAPAREA_BORDER_ETCHED_IN

      >>> MAPAREA_BORDER_ETCHED_IN
      Symbol('shadow_ein')

   .. data:: MAPAREA_BORDER_ETCHED_OUT

      >>> MAPAREA_BORDER_ETCHED_OUT
      Symbol('shadow_eout')

   .. data:: MAPAREA_SHADOW_BORDERS

      A sequence of all shadow border types.

      >>> MAPAREA_SHADOW_BORDERS
      (Symbol('shadow_in'), Symbol('shadow_out'), Symbol('shadow_ein'), Symbol('shadow_eout'))

   .. data:: MAPAREA_BORDER_ALWAYS_VISIBLE

      >>> MAPAREA_BORDER_ALWAYS_VISIBLE
      Symbol('border_avis')

The following numeric constant are pre-defined:

   .. data:: MAPAREA_SHADOW_BORDER_MIN_WIDTH

      >>> MAPAREA_SHADOW_BORDER_MIN_WIDTH
      1

   .. data:: MAPAREA_SHADOW_BORDER_MAX_WIDTH

      >>> MAPAREA_SHADOW_BORDER_MAX_WIDTH
      32


Highlight color and opacity
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. seealso::
   |djvu3ref|_: 8.3.4.2.3.1.3 *Highlight color and opacity*.

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: MAPAREA_HIGHLIGHT_COLOR

      >>> MAPAREA_HIGHLIGHT_COLOR
      Symbol('hilite')

   .. data:: MAPAREA_OPACITY

      >>> MAPAREA_OPACITY
      Symbol('opacity')

.. currentmodule:: djvu.const

The following numeric constant are pre-defined:

   .. data:: MAPAREA_OPACITY_MIN

      >>> MAPAREA_OPACITY_MIN
      0

   .. data:: MAPAREA_OPACITY_DEFAULT

      >>> MAPAREA_OPACITY_DEFAULT
      50

   .. data:: MAPAREA_OPACITY_MAX

      >>> MAPAREA_OPACITY_MAX
      100

Line and text parameters
~~~~~~~~~~~~~~~~~~~~~~~~
.. seealso::
   |djvu3ref|_: 8.3.4.2.3.1.4 *Line and Text parameters*.

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: MAPAREA_ARROW

      >>> MAPAREA_ARROW
      Symbol('arrow')

   .. data:: MAPAREA_LINE_WIDTH

      >>> MAPAREA_LINE_WIDTH
      Symbol('width')

   .. data:: MAPAREA_LINE_COLOR

      >>> MAPAREA_LINE_COLOR
      Symbol('lineclr')

   .. data:: MAPAREA_BACKGROUND_COLOR

      >>> MAPAREA_BACKGROUND_COLOR
      Symbol('backclr')

   .. data:: MAPAREA_TEXT_COLOR

      >>> MAPAREA_TEXT_COLOR
      Symbol('textclr')

   .. data:: MAPAREA_PUSHPIN

      >>> MAPAREA_PUSHPIN
      Symbol('pushpin')

.. currentmodule:: djvu.const

The following numeric constants are pre-defined:

   .. data:: MAPAREA_LINE_MIN_WIDTH

      >>> MAPAREA_LINE_MIN_WIDTH
      1

The following default colors are pre-defined:

   .. data:: MAPAREA_LINE_COLOR_DEFAULT

      >>> MAPAREA_LINE_COLOR_DEFAULT
      '#000000'

   .. data:: MAPAREA_TEXT_COLOR_DEFAULT

      >>> MAPAREA_TEXT_COLOR_DEFAULT
      '#000000'

Initial document view
---------------------
.. seealso::
   |djvu3ref|_: 8.3.4.1 *Initial Document View*.

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: ANNOTATION_BACKGROUND

      >>> ANNOTATION_BACKGROUND
      Symbol('background')

   .. data:: ANNOTATION_ZOOM

      >>> ANNOTATION_ZOOM
      Symbol('zoom')

   .. data:: ANNOTATION_MODE

      >>> ANNOTATION_MODE
      Symbol('mode')

   .. data:: ANNOTATION_ALIGN

      >>> ANNOTATION_ALIGN
      Symbol('align')


Metadata
--------
.. seealso:: |djvuext|_ (*Metadata Annotations*, *Document Annotations and Metadata*).
.. _BibTeX: https://www.ctan.org/pkg/bibtex

.. currentmodule:: djvu.decode
.. class:: Metadata

   A metadata mapping.

.. currentmodule:: djvu.const

The following sets contain noteworthy metadata keys:

   .. data:: METADATA_BIBTEX_KEYS

      Keys borrowed from the BibTeX_ bibliography system.

      >>> for key in sorted(METADATA_BIBTEX_KEYS):
      ...     print(repr(key))
      ...
      Symbol('address')
      Symbol('annote')
      Symbol('author')
      Symbol('booktitle')
      Symbol('chapter')
      Symbol('crossref')
      Symbol('edition')
      Symbol('editor')
      Symbol('howpublished')
      Symbol('institution')
      Symbol('journal')
      Symbol('key')
      Symbol('month')
      Symbol('note')
      Symbol('number')
      Symbol('organization')
      Symbol('pages')
      Symbol('publisher')
      Symbol('school')
      Symbol('series')
      Symbol('title')
      Symbol('type')
      Symbol('volume')
      Symbol('year')

   .. data:: METADATA_PDFINFO_KEYS

      Keys borrowed from the PDF DocInfo.

      >>> for key in sorted(METADATA_PDFINFO_KEYS):
      ...     print(repr(key))
      ...
      Symbol('Author')
      Symbol('CreationDate')
      Symbol('Creator')
      Symbol('Keywords')
      Symbol('ModDate')
      Symbol('Producer')
      Symbol('Subject')
      Symbol('Title')
      Symbol('Trapped')

   .. data:: METADATA_KEYS

      Sum of :data:`METADATA_BIBTEX_KEYS` and :data:`METADATA_PDFINFO_KEYS`.

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: ANNOTATION_METADATA

      >>> ANNOTATION_METADATA
      Symbol('metadata')

Printed headers and footers
---------------------------
.. seealso:: |djvu3ref|_ (8.3.4.3 *Printed headers and footers*)

.. currentmodule:: djvu.const

The following symbols are pre-defined:

   .. data:: ANNOTATION_PRINTED_HEADER

      >>> ANNOTATION_PRINTED_HEADER
      Symbol('phead')

   .. data:: ANNOTATION_PRINTED_FOOTER

      >>> ANNOTATION_PRINTED_FOOTER
      Symbol('pfoot')

   .. data:: PRINTER_HEADER_ALIGN_LEFT

      >>> PRINTER_HEADER_ALIGN_LEFT
      Symbol('left')

   .. data:: PRINTER_HEADER_ALIGN_CENTER

      >>> PRINTER_HEADER_ALIGN_CENTER
      Symbol('center')

   .. data:: PRINTER_HEADER_ALIGN_RIGHT

      >>> PRINTER_HEADER_ALIGN_RIGHT
      Symbol('right')

.. vim:ts=3 sts=3 sw=3 et

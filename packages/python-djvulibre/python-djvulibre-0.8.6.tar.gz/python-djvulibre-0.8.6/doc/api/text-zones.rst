Text zones
==========

.. testsetup::

   from djvu.const import *
   from djvu.decode import *
   from djvu.sexpr import *
   from pprint import pprint

.. seealso::
   |djvu3ref|_ (8.3.5 *Text Chunk*).

   Representing text zones as S-expressions is DjVuLibre-specific; see |djvused|_
   for reference.

.. currentmodule:: djvu.decode
.. class:: PageText(page[, details=TEXT_DETAILS_ALL])


   A wrapper around page text.

   `details` controls the level of details in the returned S-expression:

   * :data:`~TEXT_DETAILS_PAGE`, or
   * :data:`~TEXT_DETAILS_COLUMN`, or
   * :data:`~TEXT_DETAILS_REGION`, or
   * :data:`~TEXT_DETAILS_PARAGRAPH`, or
   * :data:`~TEXT_DETAILS_LINE`, or
   * :data:`~TEXT_DETAILS_WORD`, or
   * :data:`~TEXT_DETAILS_CHARACTER`, or
   * :data:`~TEXT_DETAILS_ALL`.

   .. method:: wait()

         Wait until the associated S-expression is available.

   .. attribute:: page

         :rtype: :class:`Page`

   .. attribute:: sexpr

      :rtype: :class:`djvu.sexpr.Expression`
      :raise NotAvailable:
         if the S-expression is not available; then, :class:`PageInfoMessage`
         messages with empty :attr:`~Message.page_job` may be emitted.
      :raise JobFailed:
         on failure.

.. currentmodule:: djvu.const
.. class:: TextZoneType

    A type of a text zone.

    To create objects of this class, use the :func:`get_text_zone_type()` function.

.. currentmodule:: djvu.const
.. function:: get_text_zone_type(symbol)

   Return one of the following text zone types:

      .. data:: TEXT_ZONE_PAGE

         >>> get_text_zone_type(Symbol('page')) is TEXT_ZONE_PAGE
         True

      .. data:: TEXT_ZONE_COLUMN

         >>> get_text_zone_type(Symbol('column')) is TEXT_ZONE_COLUMN
         True

      .. data:: TEXT_ZONE_REGION

         >>> get_text_zone_type(Symbol('region')) is TEXT_ZONE_REGION
         True

      .. data:: TEXT_ZONE_PARAGRAPH

         >>> get_text_zone_type(Symbol('para')) is TEXT_ZONE_PARAGRAPH
         True

      .. data:: TEXT_ZONE_LINE

         >>> get_text_zone_type(Symbol('line')) is TEXT_ZONE_LINE
         True

      .. data:: TEXT_ZONE_WORD

         >>> get_text_zone_type(Symbol('word')) is TEXT_ZONE_WORD
         True

      .. data:: TEXT_ZONE_CHARACTER

         >>> get_text_zone_type(Symbol('char')) is TEXT_ZONE_CHARACTER
         True

   You can compare text zone types using the ``>`` operator:

   >>> TEXT_ZONE_PAGE > TEXT_ZONE_COLUMN > TEXT_ZONE_REGION > TEXT_ZONE_PARAGRAPH
   True
   >>> TEXT_ZONE_PARAGRAPH > TEXT_ZONE_LINE > TEXT_ZONE_WORD > TEXT_ZONE_CHARACTER
   True

.. currentmodule:: djvu.decode
.. function:: cmp_text_zone(zonetype1, zonetype2)

   :return: a negative integer if `zonetype1` is more concrete than `zonetype2`.
   :return: a negative integer if `zonetype1` is the same as `zonetype2`.
   :return: a positive integer if `zonetype1` is the general than `zonetype2`.

.. currentmodule:: djvu.const
.. data:: TEXT_ZONE_SEPARATORS

   Dictionary that maps text types to their separators.

   >>> pprint(TEXT_ZONE_SEPARATORS)
   {<djvu.const.TextZoneType: char>: '',
    <djvu.const.TextZoneType: word>: ' ',
    <djvu.const.TextZoneType: line>: '\n',
    <djvu.const.TextZoneType: para>: '\x1f',
    <djvu.const.TextZoneType: region>: '\x1d',
    <djvu.const.TextZoneType: column>: '\x0b',
    <djvu.const.TextZoneType: page>: '\x0c'}

.. vim:ts=3 sts=3 sw=3 et

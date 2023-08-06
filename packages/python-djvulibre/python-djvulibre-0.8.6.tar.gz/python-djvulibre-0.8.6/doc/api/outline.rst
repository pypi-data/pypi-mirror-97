Document outline
================

.. testsetup::

   from djvu.const import *
   from djvu.decode import *

.. seealso::
   |djvu3ref|_ (8.3.3 *Document Outline Chunk*).

   Representing outlines as S-expressions is DjVuLibre-specific; see
   *Outline/Bookmark syntax* in |djvused|_ for reference.

.. currentmodule:: djvu.decode

.. class:: DocumentOutline

   .. method:: wait()

      Wait until the associated S-expression is available.

   .. attribute:: sexpr

      :return: the associated S-expression.

      If the S-expression is not available, raise :exc:`NotAvailable`
      exception. Then, :class:`PageInfoMessage` messages with empty
      :attr:`~Message.page_job` may be emitted.

      :raise NotAvailable: see above.
      :raise JobFailed: on failure.

.. data:: djvu.const.EMPTY_OUTLINE

   Empty outline S-expression.

   >>> EMPTY_OUTLINE
   Expression([Symbol('bookmarks')])

.. vim:ts=3 sts=3 sw=3 et

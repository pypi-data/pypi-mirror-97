Document files
==============

.. currentmodule:: djvu.decode
.. class:: DocumentFiles

   Component files of a document.

   Use :attr:`Document.files` to obtain instances of this class.

   File indexing is zero-based, i.e. :attr:`~Document.files`\ ``[0]`` stands for the first file.

   ``len(files)`` might raise :exc:`NotAvailable` when called before receiving
   a :class:`DocInfoMessage`.

.. currentmodule:: djvu.decode
.. class:: File

   Component file of a document.

   Use :attr:`Document.files`\ ``[N]`` to obtain instances of this class.

   .. attribute:: document

      :rtype: :class:`Document`

   .. attribute:: n

      :return: the component file number.

      File indexing is zero-based, i.e. 0 stands for the very first file.

   .. method:: get_info([wait=1])

      Attempt to obtain information about the component file.

      If `wait` is true, wait until the information is available.

      :raise NotAvailable: if the information is not available.
      :raise JobFailed: on failure.

   .. attribute:: type

      :return: the type of the compound file.

      The following types are possible:

         .. data:: FILE_TYPE_PAGE
         .. data:: FILE_TYPE_THUMBNAILS
         .. data:: FILE_TYPE_INCLUDE

      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: n_page

      :return: the page number, or ``None`` when not applicable.

      Page indexing is zero-based, i.e. 0 stands for the very first page.

      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: page

      :return: the page, or ``None`` when not applicable.
      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: size

      :return: the compound file size, or ``None`` when unknown.
      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: id

      :return: the compound file identifier, or ``None``.
      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: name

      :return: the compound file name, or ``None``.
      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: title

      :return: the compound file title, or ``None``.
      :raise NotAvailable: see :meth:`~File.get_info`.
      :raise JobFailed: on failure.

   .. attribute:: dump

      :return:
         a text describing the contents of the file using the same format as
         the ``djvudump`` command.

      If the information is not available, raise :exc:`NotAvailable` exception.
      Then, :exc:`PageInfoMessage` messages with empty
      :attr:`~Message.page_job` may be emitted.

      :raise NotAvailable: see above.

.. vim:ts=3 sts=3 sw=3 et

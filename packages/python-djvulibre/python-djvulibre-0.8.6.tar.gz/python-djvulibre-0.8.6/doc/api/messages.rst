Messages
========

.. currentmodule:: djvu.decode

.. class:: Message

   An abstract base for all messages.

   .. attribute:: context

      :return: the concerned context.
      :rtype: :class:`Context`.

   .. attribute:: document

      :return: the concerned document or ``None``.
      :type: :class:`Document`

   .. attribute:: page_job

      :return: the concerned page job or ``None``.
      :rtype: :class:`PageJob`

   .. attribute:: job

      :return: the concerned job or ``None``.
      :rtype: :class:`Job`

   Inheritance diagram:

      .. inheritance-diagram::
         ErrorMessage
         InfoMessage
         NewStreamMessage
         DocInfoMessage
         PageInfoMessage
         ChunkMessage
         RelayoutMessage
         RedisplayMessage
         ThumbnailMessage
         ProgressMessage
         :parts: 1

.. class:: ErrorMessage

   An :class:`ErrorMessage` is generated whenever the decoder or the DDJVU API
   encounters an error condition. All errors are reported as error messages
   because they can occur asynchronously.

   .. attribute:: message

      :return: the actual error message, as text.

   .. attribute:: location

      :return:
         a (`function`, `filename`, `line_no`) tuple indicating where the error
         was detected.

.. class:: InfoMessage

   A :class:`InfoMessage` provides informational text indicating the progress
   of the decoding process. This might be displayed in the browser status bar.

   .. attribute:: message

      :return: the actual error message, as text.

.. class:: NewStreamMessage

   A :class:`NewStreamMessage` is generated whenever the decoder needs to
   access raw DjVu data. The caller must then provide the requested data using
   the :attr:`stream` file-like object.

   In the case of indirect documents, a single decoder might simultaneously
   request several streams of data.

   .. attribute:: name

      The first :class:`NewStreamMessage` message always has :attr:`name` set
      to ``None``. It indicates that the decoder needs to access the data in
      the main DjVu file.

      Further :class:`NewStreamMessage` messages are generated to access the
      auxiliary files of indirect or indexed DjVu documents. :attr:`name` then
      provides the base name of the auxiliary file.


   .. attribute:: uri

      :return: the requested URI.

      URI is set according to the `uri` argument provided to function
      :meth:`Context.new_document`. The first :class:`NewStreamMessage` message
      always contain the URI passed to :meth:`Context.new_document`.
      Subsequent :class:`NewStreamMessage` messages contain the URI of the
      auxiliary files for indirect or indexed DjVu documents.

   .. attribute:: stream

      :return: a data stream.

      .. class:: djvu.decode.Stream

         .. method:: close()

            Indicate that no more data will be provided on the particular stream.

         .. method:: abort()

             Indicate that no more data will be provided on the particular stream,
             because the user has interrupted the data transfer (for instance by
             pressing the stop button of a browser) and that the decoding threads
             should be stopped as soon as feasible.

         .. method:: flush()

            Do nothing.

            (This method is provided solely to implement Python's file-like
            interface.)

         .. method:: read([size])

            :raise exceptions.IOError: always.

            (This method is provided solely to implement Python's file-like
            interface.)

         .. method:: write(data)

            Provide raw data to the DjVu decoder.

            This method should be called as soon as the data is available, for
            instance when receiving DjVu data from a network connection.


.. class:: DocInfoMessage

   A :class:`DocInfoMessage` indicates that basic information about the
   document has been obtained and decoded. Not much can be done before this
   happens.

   Check the document's :attr:`~Document.decoding_status` to determine whether
   the operation was successful.

.. class:: PageInfoMessage

   The page decoding process generates a :class:`PageInfoMessage`:

   - when basic page information is available and before any
     :class:`RelayoutMessage` or :class:`RedisplayMessage`,
   - when the page decoding thread terminates.

   You can distinguish both cases using the page job's :attr:`~Job.status`.

   A :class:`PageInfoMessage` may be also generated as a consequence of reading
   :attr:`Page.get_info()` or :attr:`Page.dump`.

.. class:: ChunkMessage

   A :class:`ChunkMessage` indicates that an additional chunk of DjVu data has
   been decoded.

.. class:: RelayoutMessage

   A :class:`RelayoutMessage` is generated when a DjVu viewer should recompute
   the layout of the page viewer because the page size and resolution
   information has been updated.

.. class:: RedisplayMessage

   A :class:`RedisplayMessage` is generated when a DjVu viewer should call
   :meth:`PageJob.render` and redisplay the page. This happens, for instance,
   when newly decoded DjVu data provides a better image.

.. class:: ThumbnailMessage

   A :class:`ThumbnailMessage` is sent when additional thumbnails are
   available.

   .. attribute:: thumbnail

      :rtype: :class:`Thumbnail`

      :raise NotAvailable: if the :class:`Document` has been garbage-collected.

.. class:: ProgressMessage

   A :class:`ProgressMessage` is generated to indicate progress towards the
   completion of a print or save job.

   .. attribute:: percent

      :return: the percent of the job done.

   .. attribute:: status

      :return: a :class:`JobException` subclass indicating the current job status.

.. vim:ts=3 sts=3 sw=3 et

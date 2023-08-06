Event model
===========

The DDJVU API provides for efficiently decoding and displaying DjVu documents.
It provides for displaying images without waiting for the complete DjVu data.
Images can be displayed as soon as sufficient data is available. A higher
quality image might later be displayed when further data is available. The DjVu
library achieves this using a complicated scheme involving multiple threads.
The DDJVU API hides this complexity with a familiar event model.

.. currentmodule:: djvu.decode
.. data:: DDJVU_VERSION

   Version of the DDJVU API.

.. currentmodule:: djvu.decode
.. class:: Context(argv0)

   .. method:: handle_message(message)

      This method is called, in a separate thread, for every received
      message, *before* any blocking method finishes.

      By default do something roughly equivalent to::

         if message.job is not None:
            message.job.message_queue.put(message)
         elif message.document is not None:
            message.document.message_queue.put(message)
         else:
            message.context.message_queue.put(message)

      You may want to override this method to change this behaviour.

      All exceptions raised by this method will be ignored.

   .. attribute:: message_queue

      Return the internal message queue.

   .. method:: get_message([wait=True])

      Get message from the internal context queue.

      :return: a :class:`Message` instance
      :return: ``None`` if `wait` is false and no message is available.


   .. method:: new_document(uri[ ,cache=True])

      Creates a decoder for a DjVu document and starts decoding. This
      method returns immediately. The decoding job then generates messages to
      request the raw data and to indicate the state of the decoding process.

      `uri` specifies an optional URI for the document. The URI follows the
      usual syntax (``protocol://machine/path``). It should not end with
      a slash. It only serves two purposes:

      - The URI is used as a key for the cache of decoded pages.
      - The URI is used to document :class:`NewStreamMessage` messages.

      Setting argument `cache` to a true value indicates that decoded pages
      should be cached when possible.

      It is important to understand that the URI is not used to access the
      data. The document generates :class:`NewStreamMessage` messages to indicate
      which data is needed. The caller must then provide the raw data using
      a :attr:`NewStreamMessage.stream` object.

      .. class:: djvu.decode.FileUri(filename)

         To open a local file, provide a :class:`FileUri` instance as an `uri`.

      Localized characters in `uri` should be in URI-encoded.

      :rtype: :class:`Document`
      :raise JobFailed: on failure.

   .. attribute:: cache_size

   .. method:: clear_cache()

.. currentmodule:: djvu.decode
.. class:: Job

   A job.

   .. method:: get_message([wait=True])

      Get message from the internal job queue.

      :return: a :class:`Message` instance.
      :return: ``None`` if `wait` is false and no message is available.

   .. attribute:: is_done

      Indicate whether the decoding job is done.

   .. attribute:: is_error

      Indicate whether the decoding job is done.

   .. attribute:: message_queue

      :return: the internal message queue.

   .. attribute:: status

      :return: a :exc:`JobException` subclass indicating the job status.

   .. method:: stop()

      Attempt to cancel the job.

      This is a best effort method. There no guarantee that the job will
      actually stop.

   .. method:: wait()

      Wait until the job is done.

.. vim:ts=3 sts=3 sw=3 et

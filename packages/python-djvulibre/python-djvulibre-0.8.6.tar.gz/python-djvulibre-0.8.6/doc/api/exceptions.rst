Exceptions
==========

Common exceptions
-----------------

.. currentmodule:: djvu.decode
.. exception:: NotAvailable

   A resource not (yet) available.

.. currentmodule:: djvu.sexpr
.. exception:: ExpressionSyntaxError

   Syntax error while parsing an S-expression.

.. currentmodule:: djvu.sexpr
.. exception:: InvalidExpression

   Invalid S-expression.

Job status
----------

.. currentmodule:: djvu.decode
.. exception:: JobException

   Status of a job. Possibly, but not necessarily, exceptional.

   Inheritance diagram:

      .. inheritance-diagram::
         JobNotDone
         JobNotStarted
         JobStarted
         JobDone
         JobOK
         JobFailed
         JobStopped
         :parts: 1

.. currentmodule:: djvu.decode
.. exception:: JobNotDone

   Operation is not yet done.

.. currentmodule:: djvu.decode
.. exception:: JobNotStarted

   Operation was not even started.

.. currentmodule:: djvu.decode
.. exception:: JobStarted

   Operation is in progress.

.. currentmodule:: djvu.decode
.. exception:: JobDone

   Operation finished.

.. currentmodule:: djvu.decode
.. exception:: JobOK

   Operation finished successfully.

.. currentmodule:: djvu.decode
.. exception:: JobFailed

   Operation failed because of an error.

.. currentmodule:: djvu.decode
.. exception:: JobStopped

   Operation was interrupted by user.

.. vim:ts=3 sts=3 sw=3 et

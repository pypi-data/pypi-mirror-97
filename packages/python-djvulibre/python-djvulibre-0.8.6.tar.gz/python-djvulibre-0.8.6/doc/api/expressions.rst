LISP S-expressions
==================

.. testsetup::

   from djvu.sexpr import *
   from djvu.const import *

Textual representation
----------------------
Special characters are:

* the parenthesis ``(`` and ``)``,
* the double quote ``"``,
* the vertical bar ``|``.

Symbols are represented by their name. Vertical bars ``|`` can be used to
delimit names that contain blanks, special characters, non printable
characters, non-ASCII characters, or can be confused as a number.

Numbers follow the syntax specified by the C function ``strtol()`` with
``base=0``.

Strings are delimited by double quotes. All C string escapes are
recognized. Non-printable ASCII characters must be escaped.

List are represented by an open parenthesis ``(`` followed by the space
separated list elements, followed by a closing parenthesis ``)``.

When the ``cdr`` of the last pair is non zero, the closed parenthesis is
preceded by a space, a dot ``.``, a space, and the textual representation
of the ``cdr``. (This is only partially supported by Python bindings.)

Symbols
-------
.. currentmodule:: djvu.sexpr
.. class:: Symbol(str)

   >>> Symbol('ham')
   Symbol('ham')

S-expressions
-------------
.. currentmodule:: djvu.sexpr
.. class:: Expression

   Inheritance diagram:

      .. inheritance-diagram::
         IntExpression
         ListExpression
         StringExpression
         SymbolExpression
         :parts: 1

   .. method:: as_string(width=None, escape_unicode=True)

      Return a string representation of the expression.

   .. method:: print_into(file, width=None, escape_unicode=True)

      Print the expression into the file.

   .. attribute:: value

      The “pythonic” value of the expression.
      Lisp lists as mapped to Python tuples.

   .. attribute:: lvalue

      The “pythonic” value of the expression.
      Lisp lists as mapped to Python lists.

      .. versionadded:: 0.4

.. currentmodule:: djvu.sexpr
.. class:: IntExpression

   :class:`IntExpression` can represent any integer in range :math:`\left[-2^{29}, 2^{29}\right)`.

   To create objects of this class, use the :class:`Expression` constructor:

   >>> x = Expression(42)
   >>> x
   Expression(42)
   >>> type(x)
   <class 'djvu.sexpr.IntExpression'...>
   >>> x.as_string()
   '42'
   >>> x.value
   42

.. currentmodule:: djvu.sexpr
.. class:: ListExpression

   To create objects of this class, use the :class:`Expression` constructor:

   >>> x = Expression([4, 2])
   >>> x
   Expression([4, 2])
   >>> type(x)
   <class 'djvu.sexpr.ListExpression'...>
   >>> x.as_string()
   '(4 2)'
   >>> x.value
   (4, 2)
   >>> x.lvalue
   [4, 2]

.. currentmodule:: djvu.sexpr
.. class:: StringExpression

   To create objects of this class, use the :class:`Expression` constructor:

   >>> x = Expression('eggs')
   >>> x
   Expression('eggs')
   >>> type(x)
   <class 'djvu.sexpr.StringExpression'...>
   >>> x.as_string()
   '"eggs"'
   >>> x.value
   'eggs'

.. currentmodule:: djvu.sexpr
.. class:: SymbolExpression

   To create objects of this class, use the :class:`Expression` constructor:

   >>> x = Expression(Symbol('ham'))
   >>> x
   Expression(Symbol('ham'))
   >>> type(x)
   <class 'djvu.sexpr.SymbolExpression'...>
   >>> x.as_string()
   'ham'
   >>> x.value
   Symbol('ham')

Varieties
---------
.. data:: EMPTY_LIST

   Empty list S-expression.

   >>> EMPTY_LIST
   Expression([])

.. vim:ts=3 sts=3 sw=3 et

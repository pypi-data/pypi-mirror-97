
`commie <https://github.com/rtmigo/commie.python/>`_
========================================================


.. image:: https://github.com/rtmigo/commie.python/workflows/CI/badge.svg?branch=master
   :target: https://github.com/rtmigo/commie.python/actions
   :alt: Actions Status


.. image:: https://img.shields.io/pypi/status/commie.svg
   :target: https://pypi.python.org/pypi/commie/
   :alt: PyPI status


.. image:: https://img.shields.io/pypi/v/commie.svg
   :target: https://pypi.python.org/pypi/commie/
   :alt: PyPI version shields.io


.. image:: https://img.shields.io/pypi/pyversions/commie.svg
   :target: https://pypi.python.org/pypi/commie/
   :alt: PyPI pyversions


.. image:: https://img.shields.io/pypi/l/commie.svg
   :target: https://pypi.python.org/pypi/commie/
   :alt: PyPI license


Native Python package for **extracting comments** from source code.

Multiple programming and markup languages are supported: `see list <https://github.com/rtmigo/commie.python#find-comments-in-a-string>`_.

Install
=======

.. code-block:: sh

   $ pip3 install commie

Find comments in a file
=======================

.. code-block:: python

   from pathlib import Path
   import commie

   for comment in commie.iter_comments(Path("/path/to/source.cpp")):

     # something like "/* sample */"
     print("Comment code:", comment.code)
     print("Comment code location:", comment.code_span.start, comment.code_span.end)

     # something like " sample " 
     print("Comment inner text:", comment.text)
     print("Comment text location:", comment.text_span.start, comment.text_span.end)

Find comments in a string
=========================

.. list-table::
   :header-rows: 1

   * - **Method**
     - **Works for**
   * - ``commie.iter_comments_c``
     - C, C++, C#, Java, Objective-C, JavaScript, Dart, TypeScript
   * - ``commie.iter_comments_go``
     - Go
   * - ``commie.iter_comments_ruby``
     - Ruby
   * - ``commie.iter_comments_python``
     - Python
   * - ``commie.iter_comments_shell``
     - Bash, Sh
   * - ``commie.iter_comments_html``
     - HTML, XML, SGML
   * - ``commie.iter_comments_css``
     - CSS
   * - ``commie.iter_comments_sass``
     - SASS


.. code-block:: python

   import commie

   source_code_in_golang:str = ...

   for comment in commie.iter_comments_go(source_code_in_golang):
     # ... process comment ...
     pass

Find comments in a string with a known filename
===============================================

Method ``commie.iter_comments`` will try to guess the file format from the provided filename.

.. code-block:: python

   from pathlib import Path
   import commie

   filename:str = "/path/to/mycode.go"
   source_code:str = Path(filename).read_text()

   for comment in commie.iter_comments(source_code, filename=filename):
     # ... process comment ...
     pass

----

This project was forked from `comment_parser <https://github.com/jeanralphaviles/comment_parser>`_ in 2021. Motivation:

.. list-table::
   :header-rows: 1

   * - **comment_parser**
     - **commie**
   * - Returns only a line number
     - Returns positions where the comment starts and ends. Just like regular string search
   * - Returns only the text of a comment
     - Respects markup as well, making it possible to remove or replace the entire comment
   * - Depends on `python-magic <https://pypi.org/project/python-magic>`_ that requires an optional installation of binaries
     - Pure Python. Easy to install with ``pip``


As for now it's too different from ``comment_parser``\ , so the changes will not be pulled there.

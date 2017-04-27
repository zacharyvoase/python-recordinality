Recordinality.py
================

A Python implementation of the
`Recordinality <http://www-apr.lip6.fr/%7Elumbroso/Publications/HeLuMaVi12.pdf>`__
sketch for cardinality estimation and stream sampling. Inspired by C.
Scott Andreas's
`implementation <https://github.com/cscotta/recordinality>`__, but
powered by SipHash-2-4 rather than MurmurHash3. In particular, this
project uses two other libraries of mine:
`csiphash <https://github.com/zacharyvoase/python-csiphash>`__ and
`cskipdict <https://github.com/zacharyvoase/python-cskipdict>`__.

Installation
------------

::

    pip install recordinality

Usage
-----

You can use the command-line application, which will read lines of text
incrementally from stdin, printing the stream's cardinality (or a random
sample) once the pipe is closed:

::

    $ recordinality -k <sketch-size> [-h|--hash-key <hash-key>] [-s|--sample] < input-lines.txt
    3574
    $ cat input-lines.txt | sort -u | wc -l
    3556

SipHash allows the specification of a 'secret key' (used here as more of
a hash seed); if provided it should be either a 16-char ASCII string or
32-char hexadecimal string.

You can also import the ``Recordinality`` class in Python:

.. code:: python

    >>> from recordinality import Recordinality
    >>> sketch = Recordinality(size=512)
    >>> for observation in input_observations:
    ...     sketch.add(observation)
    >>> print(sketch.cardinality())
    3574
    >>> print(sketch.k_sample)
    ['strife', 'bragging', 'knight?', ...]

Unlicense
---------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to
the public domain. We make this dedication for the benefit of the public
at large and to the detriment of our heirs and successors. We intend
this dedication to be an overt act of relinquishment in perpetuity of
all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org/

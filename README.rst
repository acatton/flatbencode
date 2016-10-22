flatbencode
============

.. image:: https://travis-ci.org/acatton/flatbencode.svg?branch=master
    :target: https://travis-ci.org/acatton/flatbencode

Fast, safe and thoroughly tested implementation of ``bencode`` in pure Python
3, without any C extension.

This is called ``flatbencode`` because the algorithm for decoding a ``bencode``
structure is non-recursive, thus preventing ``RuntimeException``.


Usage
-----


.. code:: python

    >>> from flatbencode import encode, decode
    >>> encode({b'foo': [b'bar', 1]})
    b'd3:fool3:bari1eee'
    >>> decode(b'ldei0e0:e')
    [OrderedDict(), 0, b'']


Run tests
---------

.. code::

    $ pip install pytest hypothesis
    $ py.test -v


Changelog
---------

v0.2.0 (2016-10-22)
^^^^^^^^^^^^^^^^^^^

* Raise an exception when there's still data left. [Tim Ruffing, #2]
* Use bytes as python dictionary keys (instead of strings) [Tim Ruffing, #2]
* Sort dictionary keys when serializing (follows the BEP-0003) [Antoine Catton]


v0.1.0 (2016-06-12)
^^^^^^^^^^^^^^^^^^^

* Initial release.
* Can decode bencoding into a python datastructure.
* Can encode a python datastructure into bencoding serialization format.

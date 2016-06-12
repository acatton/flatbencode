flatbencode
============

Fast and safe implementation of bencode in pure python 3, without any C extension.

This is called ``flatbencode`` because the algorithm for decoding a bencode
structure is non-recursive, thus preventing ``RuntimeException``s

import contextlib
import sys

from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st
import pytest

from flatbencode import decode
from flatbencode import DecodingError
from flatbencode import encode


skip_py37 = pytest.mark.skipif(
    sys.version_info > (3, 6),
    reason="Python 3.7 is not supported by hypothesis"
)


def list_nesting(elem, n):
    """Nest on element in n list::

        >>> list_nesting('hello', 3)
        [[['hello']]]
    """
    for _ in range(n):
        elem = [elem]
    return elem


@contextlib.contextmanager
def maximum_recursion(n):
    default = sys.getrecursionlimit()
    sys.setrecursionlimit(n)
    try:
        yield
    finally:
        sys.setrecursionlimit(default)


@pytest.mark.parametrize('data,expected', [
    # All these examples are from the specification
    # <http://www.bittorrent.org/beps/bep_0003.html>
    (b'i3e', 3),
    (b'i-3e', -3),
    (b'i0e', 0),
    (b'4:spam', b'spam'),
    (b'l4:spam4:eggse', [b'spam', b'eggs']),
    (b'd3:cow3:moo4:spam4:eggse', {b'cow': b'moo', b'spam': b'eggs'}),
    (b'd4:spaml1:a1:bee', {b'spam': [b'a', b'b']}),
    # These are extra test cases for complex nested data structures
    (b'd1:dl1:el1:f1:gee1:al1:b1:cee', {b'a': [b'b', b'c'], b'd': [b'e', [b'f', b'g']]}),
    (b'l1:al1:bl1:cel1:del1:e1:feee', [b'a', [b'b', [b'c'], [b'd'], [b'e', b'f']]]),
])
def test_decode_simple(data, expected):
    assert decode(data) == expected


MIN_RECURSION = 200


# This test makes sure that no data can crash decode function. Thus parsing
# untrusted data with this library is safe.
@pytest.mark.parametrize('depth', [10, 100, 500, 1000, 1500])
def test_decode_recursion(depth):
    data = b'l' * depth + b'i0e' + b'e' * depth
    expected = list_nesting(0, depth)

    # Test that we don't have any nesting limit (many implementation uses
    # recursivity which blows up the stack.)
    with maximum_recursion(MIN_RECURSION):
        result = decode(data)

    with maximum_recursion(max(depth ** 2, MIN_RECURSION)):
        assert result == expected


def test_order_is_preserved():
    assert list(decode(b'd3:cow3:moo4:spam4:eggse').keys()) == [b'cow', b'spam']


@pytest.mark.parametrize('data', [
    b'i03e',
    b'i-0e',
    b'dlelee',
    b'i5etrailing',
])
def test_invalid_values(data):
    with pytest.raises(DecodingError):
        decode(data)


@pytest.mark.parametrize('dictionary,expected', [
    ({b'a': b'b'}, b'd1:a1:be'),
    ({b'a': 0, b'b': 1, b'c': b'c'}, b'd1:ai0e1:bi1e1:c1:ce'),
    ({b'z': 0, b'a': 0}, b'd1:ai0e1:zi0ee'),
])
def test_dict_keys_are_alphabetically_sorted(dictionary, expected):
    assert encode(dictionary) == expected


values = st.recursive(
    st.integers() | st.binary(),
    lambda children: (
        st.lists(children) | st.dictionaries(st.binary(), children)
    )
)


@skip_py37
@given(obj=values)
@example(obj=0)
@example(obj=1)
@example(obj=500)
@example(obj=b'hello')
@example(obj=[b'hello', b'world'])
@example(obj={b'hello': b'world', b',': [b'mister', b'miss']})
def test_prop_decode_encode_is_a_noop(obj):
    assert decode(encode(obj)) == obj


@skip_py37
@given(obj=values)
def test_prop_encode_is_stable(obj):
    assert encode(obj) == encode(obj)


@settings(max_examples=10)
@given(obj=values)
@given(extra=st.binary(min_size=1))
def test_prop_trailing_data_is_invalid(obj, extra):
    with pytest.raises(DecodingError):
        assert decode(encode(obj) + extra)

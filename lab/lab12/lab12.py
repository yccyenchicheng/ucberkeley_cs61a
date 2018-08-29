from stream import *

def countdown(n):
    """
    A generator that counts down from N to 0.
    >>> for number in countdown(5):
    ...     print(number)
    ...
    5
    4
    3
    2
    1
    0
    >>> for number in countdown(2):
    ...     print(number)
    ...
    2
    1
    0
    """
    while n >= 0:
        yield n
        n -= 1

def trap(s, k):
    """Return a generator that yields the first K values in iterable S,
    but raises a ValueError exception if any more values are requested.

    >>> t = trap([3, 2, 1], 2)
    >>> next(t)
    3
    >>> next(t)
    2
    >>> next(t)
    ValueError
    >>> list(trap(range(5), 5))
    ValueError
    """
    assert len(s) >= k
    
    index = 0
    while len(s) >= 0:
        k = k - 1
        if k < 0:
            raise ValueError

        yield s[index]
        index += 1


def repeated(t, k):
    """Return the first value in iterable T that appears K times in a row.

    >>> s = [3, 2, 1, 2, 1, 4, 4, 5, 5, 5]
    >>> repeated(trap(s, 7), 2)
    4
    >>> repeated(trap(s, 10), 3)
    5
    >>> print(repeated([4, None, None, None], 3))
    None
    """
    assert k > 1
    
    first = True
    for elem in t:
        if first:
            first = False
            curr_elem = elem
            count_consecutive = 1

        else:
            if curr_elem == elem:
                count_consecutive += 1
            else:
                count_consecutive = 1
                curr_elem = elem

            if count_consecutive == k:
                return curr_elem
    return None


#ones = None

def ones_test():
    """
    >>> ones.first, ones.rest.first, ones.rest.rest.first, ones.rest.rest.rest.first
    (1, 1, 1, 1)
    """
    return Stream(1, ones_test)

ones = ones_test()

def scan(f, initial_value, stream):
    """
    >>> ones = Stream(1, lambda: ones)
    >>> naturals = scan(lambda x, y: x + y, 1, ones)
    >>> _ = naturals.rest.rest.rest
    >>> naturals
    Stream(1, Stream(2, Stream(3, Stream(4, <Stream>))))
    >>> factorials = scan(lambda x, y: x * y, 1, naturals)
    >>> _ = factorials.rest.rest.rest.rest
    >>> factorials
    Stream(1, Stream(1, Stream(2, Stream(6, Stream(24, <Stream>)))))
    """
    #def make_scan_stream():
    #    return scan(f, f(initial_value, stream.first), stream.rest)
    #return Stream(initial_value, make_scan_stream)

    return Stream(initial_value, lambda: scan(f, f(initial_value, stream.first), stream.rest))




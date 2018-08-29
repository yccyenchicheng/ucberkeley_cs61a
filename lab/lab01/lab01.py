"""Lab 1: Expressions and Control Structures"""

# Coding Practice

def repeated(f, n, x):
    """Returns the result of composing f n times on x.

    >>> def square(x):
    ...     return x * x
    ...
    >>> repeated(square, 2, 3)  # square(square(3)), or 3 ** 4
    81
    >>> repeated(square, 1, 4)  # square(4)
    16
    >>> repeated(square, 6, 2)  # big number
    18446744073709551616
    >>> def opposite(b):
    ...     return not b
    ...
    >>> repeated(opposite, 4, True)
    True
    >>> repeated(opposite, 5, True)
    False
    >>> repeated(opposite, 631, 1)
    False
    >>> repeated(opposite, 3, 0)
    True
    """

    # base case 1
    if n == 0: 
        return

    # base case 2
    elif n == 1:
        return f(x)

    # recursivly call itself
    else:
        return repeated(f, n - 1, f(x))

def sum_digits(n):
    """Sum all the digits of n.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    """

    # mysum is to record the cur sum of digits
    mysum = 0;

    if n < 10:
        return n
    else:
        # if n is greater than 10
        while n // 10 != 0:
            mysum += (n % 10)
            n = n // 10
        mysum += n
        
        return mysum


def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    
    dig_string = str(n)

    for i in range(len(dig_string)):
        if i + 1 == len(dig_string):
            return False
        else:
            if dig_string[i] == '8' and dig_string[i + 1] == '8':
                return True
            else:
                return False




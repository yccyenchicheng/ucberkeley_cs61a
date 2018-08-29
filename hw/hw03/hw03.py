HW_SOURCE_FILE = 'hw03.py'

#############
# Questions #
#############

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    if n <= 3:
        return n
    else:
        return g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    if n <= 3:
        return n
    else:
        g_of_n_minus_3 = 1
        g_of_n_minus_2 = 2
        g_of_n_minus_1 = 3
        k = 4
        while k <= n:
            total = g_of_n_minus_1 + 2 * g_of_n_minus_2 + 3 * g_of_n_minus_3
            g_of_n_minus_3 = g_of_n_minus_2
            g_of_n_minus_2 = g_of_n_minus_1
            g_of_n_minus_1 = total
            k = k + 1
        return total

    

def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    if k % 7 == 0:
        return True

    all_last_digit, last_digit = k // 10, k % 10
    if all_last_digit < 10:
        if all_last_digit == 7:
            return True
        elif last_digit == 7:
            return True
        else:
            return False
    else:
        return has_seven(all_last_digit)

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    if n <= 7:
        return n

    def count_7(n):
        if n == 7:
            return 1
        else:
            if has_seven(n):
                return 1 + count_7(n - 1)
            else:
                return count_7(n - 1)

    def going_up(n):
        if n == 14:
            return 0
        elif has_seven(n):
            return going_down(n - 1) - 1
        else:
            return going_up(n - 1) + 1

    def going_down(n):
        if n == 7:
            return 7
        elif has_seven(n):
            return going_up(n - 1) + 1
        else:
            return going_down(n - 1) - 1

    if count_7(n) % 2 == 0:
        return going_up(n)
    else:
        return going_down(n)

def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    def is_pow_of_two(k):
        if k == 1:
            return True
        elif k == 2:
            return True
        
        if k % 2 != 0:
            return False
        else:
            return is_pow_of_two(k // 2)

    def find_biggest_cent(k):
        if is_pow_of_two(k):
            return k
        else:
            return find_biggest_cent(k - 1)

    def count_change_with_biggest_cent(amount, biggest_cent):
        if amount == 1 or amount == 0:
            return 1
        elif biggest_cent == 1:
            return 1
        elif amount < 0:
            return 0
        else:
            if amount < biggest_cent:
                biggest_cent = biggest_cent // 2
            
            all_last_change = amount - biggest_cent
            next_cent = biggest_cent // 2
            with_biggest_cent = count_change_with_biggest_cent(all_last_change, biggest_cent)
            wo_biggest_cent = count_change_with_biggest_cent(amount, next_cent)

            return with_biggest_cent + wo_biggest_cent

    biggest_cent = find_biggest_cent(amount)
    return count_change_with_biggest_cent(amount, biggest_cent)


    

def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    
    medium = min({1, 2, 3} - {start, end})
    if n == 1:
        print_move(start, end)
    elif n == 2:
        print_move(start, medium)
        print_move(start, end)
        print_move(medium, end)
    else:
        move_stack(n - 1, start, medium)
        move_stack(1, start, end)
        move_stack(n - 1, medium, end)


def flatten(lst):
    """Returns a flattened version of lst.

    >>> flatten([1, 2, 3])     # normal list
    [1, 2, 3]
    >>> x = [1, [2, 3], 4]      # deep list
    >>> flatten(x)
    [1, 2, 3, 4]
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> flatten(x)
    [1, 1, 1, 1, 1, 1]
    """
    flatten_list = []
    for element in lst:
        if type(element) == list:
            flatten_list = flatten_list + flatten(element)
        else:
            flatten_list = flatten_list + [element]

    return flatten_list

def merge(lst1, lst2):
    """Merges two sorted lists.

    >>> merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([], [2, 4, 6])
    [2, 4, 6]
    >>> merge([1, 2, 3], [])
    [1, 2, 3]
    >>> merge([5, 7], [2, 4, 6])
    [2, 4, 5, 6, 7]
    """

    if lst1 == []:
        return lst2
    elif lst2 == []:
        return lst1
    else:
        lst1_length = len(lst1)
        lst2_length = len(lst2)
        result_list = []

        i, j = 0, 0
        while i < lst1_length and j < lst2_length:

            if lst1[i] < lst2[j]:
                result_list += [lst1[i]]

                if i == lst1_length - 1:
                    if j == lst2_length - 1:
                        result_list += [lst2[j]]
                        i += 1
                    else:
                        j += 1
                else:
                    i += 1

            elif lst1[i] == lst2[j]:
                result_list += [lst1[i]]
                if i == lst1_length - 1:
                    j += 1
                else:
                    i += 1

            else:
                result_list += [lst2[j]]

                if j == lst2_length - 1:
                    if i == lst1_length - 1:
                        result_list += [lst1[i]]
                        j += 1
                    else:
                        i += 1
                else:
                    j += 1

    return result_list





def mergesort(seq):
    """Mergesort algorithm.

    >>> mergesort([4, 2, 5, 2, 1])
    [1, 2, 2, 4, 5]
    >>> mergesort([])     # sorting an empty list
    []
    >>> mergesort([1])   # sorting a one-element list
    [1]
    """
    total_length = len(seq)
    if total_length <= 1:
        return seq
    else:
        mid_point = total_length // 2
        left_half = seq[:mid_point]
        right_half = seq[mid_point:]

        left_sorted_list = mergesort(left_half)
        right_sorted_list = mergesort(right_half)

        result_list = merge(left_sorted_list, right_sorted_list)

    return result_list






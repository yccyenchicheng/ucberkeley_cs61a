HW_SOURCE_FILE = 'hw04.py'

################
# Linked Lists #
################

# Linked List definition
empty = 'empty'


def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (type(s) == list and len(s) == 2 and is_link(s[1]))


def link(first, rest=empty):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]


def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), 'first only applies to linked lists.'
    assert s != empty, 'empty linked list has no first element.'
    return s[0]


def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), 'rest only applies to linked lists.'
    assert s != empty, 'empty linked list has no rest.'
    return s[1]

def isempty(s):
    """Returns True iff s is the empty list."""
    return s is empty


def print_link(s):
    """Print elements of a linked list s.

    >>> s = link(1, link(2, link(3, empty)))
    >>> print_link(s)
    1 2 3
    """
    line = ''
    while s != empty:
        if line:
            line += ' '
        line += str(first(s))
        s = rest(s)
    print(line)

def change(lst, s, t):
    """Returns a link matching lst but with all instances of s (if any)
    replaced by t.

    >>> lst = link(1, link(2, link(3)))
    >>> new = change(lst, 3, 1)
    >>> print_link(new)
    1 2 1
    >>> newer = change(new, 1, 2)
    >>> print_link(newer)
    2 2 2
    >>> newest = change(newer, 5, 1)
    >>> print_link(newest)
    2 2 2
    """

    if rest(lst) == empty:
        if first(lst) == s:
            return link(t)
        else:
            return link(first(lst))
    else:
        if first(lst) == s:
            return link(t, change(rest(lst), s, t))
        else:
            return link(first(lst), change(rest(lst), s, t))

def reverse_iterative(s):
    """Return a reversed version of a linked list s.

    >>> primes = link(2, link(3, link(5, link(7, empty))))
    >>> reversed_primes = reverse_iterative(primes)
    >>> print_link(reversed_primes)
    7 5 3 2
    """
    temp = []
    reverse = 'empty'

    while s != empty:
        temp += [first(s)]
        s = rest(s)

    for item in temp:
        reverse = link(item, reverse)

    return reverse

def reverse_recursive(s):
    """Return a reversed version of a linked list s.

    >>> primes = link(2, link(3, link(5, link(7, empty))))
    >>> reversed_primes = reverse_recursive(primes)
    >>> print_link(reversed_primes)
    7 5 3 2
    """

    def link_reverse_list(curr_s, last_s):
        if rest(curr_s) == 'empty':
            return link(first(curr_s), last_s)
        else:
            last_s = link(first(curr_s), last_s)
            return link_reverse_list(rest(curr_s), last_s)

    result = 'empty'

    return link_reverse_list(s, result)


def insert(lst, item, index):
    """Returns a link matching lst but with the given item inserted at the
    specified index. If the index is greater than the current length, the item
    is appended to the end of the list.

    >>> lst = link(1, link(2, link(3)))
    >>> new = insert(lst, 9001, 1)
    >>> print_link(new)
    1 9001 2 3
    >>> newer = insert(new, 9002, 15)
    >>> print_link(newer)
    1 9001 2 3 9002
    """
    
    if rest(lst) == 'empty':
        if index > 0:
            return link(first(lst), link(item))
        else:
            return link(first(lst))
    else:
        if index == 1:
            return link(first(lst), link(item, insert(rest(lst), item, index - 1)))
        else:
            return link(first(lst), insert(rest(lst), item, index - 1))

    



#########
# Trees #
#########

def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def root(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(root(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(root(t), [copy_tree(b) for b in branches(t)])

def acorn_finder(t):
    """Returns True if t contains a node with the value 'acorn' and
    False otherwise.

    >>> scrat = tree('acorn')
    >>> acorn_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('acorn')]), tree('branch2')])
    >>> acorn_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> acorn_finder(numbers)
    False
    """
    if root(t) == 'acorn':
        return True
    else:
        return False or True in [acorn_finder(b) for b in branches(t)]

def same_shape(t1, t2):
    """Return True if t1 is indentical in shape to t2.

    >>> test_tree1 = tree(1, [tree(2), tree(3)])
    >>> test_tree2 = tree(4, [tree(5), tree(6)])
    >>> test_tree3 = tree(1,
    ...                   [tree(2,
    ...                         [tree(3)])])
    >>> test_tree4 = tree(4,
    ...                   [tree(5,
    ...                         [tree(6)])])
    >>> same_shape(test_tree1, test_tree2)
    True
    >>> same_shape(test_tree3, test_tree4)
    True
    >>> same_shape(test_tree2, test_tree4)
    False
    """
    if is_leaf(t1) and is_leaf(t2):
        return True
    elif not is_leaf(t1) and is_leaf(t2):
        return False
    elif is_leaf(t1) and not is_leaf(t2):
        return False
    else:
        return not False in [same_shape(b1, b2) for b1, b2 in zip(branches(t1), branches(t2))]

def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    if is_leaf(t1) and is_leaf(t2):
        return tree(root(t1) + root(t2))

    elif is_leaf(t1) and not is_leaf(t2):
        zero_t1 = tree(root(t1), [tree(0)] * len(branches(t2)))
        return tree(root(t1) + root(t2), [add_trees(b1, b2) for b1, b2 in zip(branches(zero_t1), branches(t2))])

    elif not is_leaf(t1) and is_leaf(t2):
        zero_t2 = tree(root(t2), [tree(0)] * len(branches(t1)))
        return tree(root(t1) + root(t2), [add_trees(b1, b2) for b1, b2 in zip(branches(t1), branches(zero_t2))])
    
    else:
        if len(branches(t1)) < len(branches(t2)):
            zero_t1 = tree(root(t1), branches(t1)) + [tree(0)] * (len(branches(t2)) - len(branches(t1)))
            return tree(root(t1) + root(t2), [add_trees(b1, b2) for b1, b2 in zip(branches(zero_t1), branches(t2))])

        elif len(branches(t1)) > len(branches(t2)):
            zero_t2 = tree(root(t2), branches(t2)) + [tree(0)] * (len(branches(t1)) - len(branches(t2)))
            return tree(root(t1) + root(t2), [add_trees(b1, b2) for b1, b2 in zip(branches(t1), branches(zero_t2))])

        else:
            return tree(root(t1) + root(t2), [add_trees(b1, b2) for b1, b2 in zip(branches(t1), branches(t2))])

###########
# Mobiles #
###########

def mobile(left, right):
    """Construct a mobile from a left side and a right side."""
    return tree(None, [left, right])

def sides(m):
    """Select the sides of a mobile."""
    return branches(m)

def side(length, mobile_or_weight):
    """Construct a side: a length of rod with a mobile or weight at the end."""
    return tree(length, [mobile_or_weight])

def length(s):
    """Select the length of a side."""
    return root(s)

def end(s):
    """Select the mobile or weight hanging at the end of a side."""
    return branches(s)[0]

def weight(size):
    """Construct a weight of some size."""
    assert size > 0
    return tree(size)

def size(w):
    """Select the size of a weight."""
    return root(w)

def is_weight(w):
    """Whether w is a weight, not a mobile."""
    return root(w) != None

def examples():
    t = mobile(side(1, weight(2)),
               side(2, weight(1)))
    u = mobile(side(5, weight(1)),
               side(1, mobile(side(2, weight(3)),
                              side(3, weight(2)))))
    v = mobile(side(4, t), side(2, u))
    return (t, u, v)


def total_weight(m):
    """Return the total weight of m, a weight or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    """
    if is_weight(m):
        return size(m)
    else:
        return sum([total_weight(end(s)) for s in sides(m)])

def balanced(m):
    """Return whether m is balanced.

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(side(3, t), side(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(side(1, v), side(1, w)))
    False
    >>> balanced(mobile(side(1, w), side(1, v)))
    False
    """

    # if both sides are weight
    if not False in [is_weight(end(s)) for s in sides(m)]:

        # store torques in list and see if they're equal by set
        torques = [length(s) * size(end(s)) for s in sides(m)]
        return len(set(torques)) == 1
    else:

        # if bothe sides' torques are equal, check its sub-moblie
        torques = [length(s) * total_weight(end(s)) for s in sides(m)]
        if len(set(torques)) == 1:
            
            return not False in [balanced(end(s)) for s in sides(m) if not is_weight(end(s))]

        else:
            return False

        return False




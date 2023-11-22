import bisect
import collections
import collections.abc
import functools
import heapq
import operator
import os.path
import random
from itertools import chain, combinations
from statistics import mean

import numpy as np

def sequence(iterable):
    return iterable if isinstance(iterable, collections.abc.Sequence) else tuple([iterable])

def remove_all(item, seq):
    if isinstance(seq, str):
        return seq.replace(item, '')
    elif isinstance(seq, set):
        rest = seq.copy()
        rest.remove(item)
        return rest
    else:
        return [x for x in seq if x != item]

def unique(seq):
    return list(set(seq))

def count(seq):
    return sum(map(bool, seq))

def multimap(items):
    result = collections.defaultdict(list)
    for (key, val) in items:
        result[key].append(val)
    return dict(result)

def multimap_items(mmap):
    for (key, vals) in mmap.items():
        for val in vals:
            yield key, val

def product(numbers):
    result = 1
    for x in numbers:
        result *= x
    return result

def first(iterable, default=None):
    return next(iter(iterable), default)

def is_in(elt, seq):
    return any(x is elt for x in seq)

def mode(data):
    [(item, count)] = collections.Counter(data).most_common(1)
    return item

def power_set(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))[1:]

def extend(s, var, val):
    return {**s, var: val}

def flatten(seqs):
    return sum(seqs, [])

identity = lambda x: x

def argmin_random_tie(seq, key=identity):
    return min(shuffled(seq), key=key)

def argmax_random_tie(seq, key=identity):
    return max(shuffled(seq), key=key)

def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items

# Statistical and mathematical functions...

# Grid Functions...

orientations = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]
turns = LEFT, RIGHT = (+1, -1)

def turn_heading(heading, inc, headings=orientations):
    return headings[(headings.index(heading) + inc) % len(headings)]

def turn_right(heading):
    return turn_heading(heading, RIGHT)

def turn_left(heading):
    return turn_heading(heading, LEFT)

def distance(a, b):
    xA, yA = a
    xB, yB = b
    return np.hypot((xA - xB), (yA - yB))

def distance_squared(a, b):
    xA, yA = a
    xB, yB = b
    return (xA - xB) ** 2 + (yA - yB) ** 2

# Misc Functions...

class injection:
    def __init__(self, **kwds):
        self.new = kwds

    def __enter__(self):
        self.old = {v: globals()[v] for v in self.new}
        globals().update(self.new)

    def __exit__(self, type, value, traceback):
        globals().update(self.old)

def memoize(fn, slot=None, maxsize=32):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

def name(obj):
    return (getattr(obj, 'name', 0) or getattr(obj, '__name__', 0) or
            getattr(getattr(obj, '__class__', 0), '__name__', 0) or
            str(obj))

def isnumber(x):
    return hasattr(x, '__int__')

def issequence(x):
    return isinstance(x, collections.abc.Sequence)

# Expressions...

class Expr:
    def __init__(self, op, *args):
        self.op = str(op)
        self.args = args

    def __neg__(self):
        return Expr('-', self)

    def __pos__(self):
        return Expr('+', self)

    def __invert__(self):
        return Expr('~', self)

    # Other operator overloads...

    def __repr__(self):
        op = self.op
        args = [str(arg) for arg in self.args]
        if op.isidentifier():
            return '{}({})'.format(op, ', '.join(args)) if args else op
        elif len(args) == 1:
            return op + args[0]
        else:
            opp = (' ' + op + ' ')
            return '(' + opp.join(args) + ')'

# Bool...

class Bool(int):
    __str__ = __repr__ = lambda self: 'T' if self else 'F'

T = Bool(True)
F = Bool(False)

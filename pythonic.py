# http://cafepy.com/article/be_pythonic/

import os
import random


def do_something(x):
    pass

################################################################################
# You need counters rarely, and iterators only occasionally
################################################################################

# Wrong:
i = 0
while i < 10:
    do_something(i)
    i += 1

# Pythonic:
for i in xrange(10):
    do_something(i)

print type(xrange(10, 20))  # => <type 'xrange'>
print range(10, 20)         # => <type 'list'>


# The following example indexes a list.
lst = range(100, 200)

# Wrong:
i = 0
while i < len(lst):
    do_something(lst[i])
    i += 1

# Pythonic:
for item in lst:
    do_something(item)

# An iterator variable is useful when you want to
# maintain looping state between two 'runs':
itr_lst = iter(lst)

for item in itr_lst:
    do_something(item)
    if item > 150:
        break

for item in itr_lst:  # continues where previous loop left off
    do_something(item)


################################################################################
# You may not need that for loop
################################################################################

# Python provides many higher level facilities to operate on sequences,
# such as zip(), max(), min(), list comprehensions, generator expressions
# and so on. See Built-in Functions for these functions and more.

# Keep data in tuples, lists and dictionaries, and operate on entire collections
# for that fuzzy Pythonic feeling.

# For example, here is some code that reads a CSV file
# (with first row being the field names), converts each line into a dictionary
# record, and calculates the sum on the 'quantity' column:

# f is an iterator
f = open('data.csv')

# get the first item from the iterator using next()
field_names = f.next().split(',')

# this will pull remaining lines (the expression inside the list is a generator)
records = [dict(zip(field_names, line.split(','))) for line in f]

print sum(int(record['quantity']) for record in records)

# Though a little naive (you should be using the csv module anyway, which is
# part of the Python Standard Library), this example demonstrates some useful
# features.

# Using zip() with dict() you can combine a tuple of field names with a tuple of
# values and make a dictionary - combine with list comprehensions you can do
# this to an entire list in one go.

################################################################################
# Tuples are not read-only lists
################################################################################

# Tuples usually indicate a heterogenous collection
# for example (first_name, last_name) or (ip_address, port).
# Note that the type may be same (as in first_name and last_name may both be
# strings), but the real world meaning is usually different.
# You can think of a tuple as a row in a relational database - in fact the
# database row is even called a tuple in formal descriptions of the relational
# model. By contrast, a list of names is always a list, even though a particular
# function may not change it, that does not make it a tuple.

# Tuple unpacking is a useful technique to extract values from a tuple.
# For example:

all_connections = [('127.0.0.1', 3128), ('127.0.0.1', 6379)]

for (ip_address, port) in all_connections:
    if port < 10000:
        print 'Connected to %s on %s' % (ip_address, port)

# Reading this code tells you that all_connections is a list (or iterable)
# contaning tuples of the form (ip_address, port). This is much clearer than
# using for item in all_connections and then poking inside item using item[0]
# or similar techniques.

# Unpacking is also useful while returning multiple values from a function. For
# example, split a file name into first part and extension.

name, ext = os.path.splitext('data.csv')
print name, ext

################################################################################
# Classes are not for grouping utility functions
################################################################################

# C# and Java can have code only within classes, and end up with many utility
# classes containing only static methods. A common example is a math functions
# such as sin(). In Python you just use a module with the top level functions.

################################################################################
# Say no to getter and setter methods
################################################################################

# Yes, encapsulation is important. No, getters and setters are not the only way
# to implement encapsulation. In Python, you can use a property to replace
# a member variable and completely change the implementation mechanism,
# with no change to any calling code.


class Foo(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")

# If then foo is an instance of Foo, foo.x will invoke the getter, foo.x = value
# will invoke the setter and del c.x the deleter.
# If given, doc will be the docstring of the property attribute.
# Otherwise, the property will copy fget's docstring (if it exists).

# This makes it possible to create read-only properties easily using property()
# as a decorator:


class Parrot(object):
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage


p = Parrot()
print p.voltage


# A property object has getter, setter, and deleter methods usable as decorators
# that create a copy of the property with the corresponding accessor function
# set to the decorated function. This is best explained with an example:


class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x

################################################################################
# Functions are objects
################################################################################

# A function is a object that happens to be callable.
# This example sorts a list of dictionaries based on the value of 'price' key
# in the dictionaries:

#  define a function that returns useful data from within an object


def get_price(ob):
    return ob['price']


lst = [dict(price=x) for x in range(10, 20)]
random.shuffle(lst)

# sort a list using the ['price'] value of objects in the list
# lst.sort(key=get_price)

print lst
# In the above case, you can also avoid defining the simple get_price()
# function and instead just generate the function using
# operator.itemgetter('price').

# You can also use:
lst.sort(key=lambda x: x['price'])

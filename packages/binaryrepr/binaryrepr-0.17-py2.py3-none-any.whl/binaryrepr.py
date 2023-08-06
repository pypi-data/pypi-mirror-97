#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: binaryrepr.py
Author: David LAMOULLER
Email: dlamouller@protonmail.com
Github: https://github.com/dlamouller
Description: binaryrep is a utility to display position of the bits of a number.
"""

import sys
from math import log
from operator import itemgetter
import click
import prettytable as pt

# option fo click
click.disable_unicode_literals_warning = True
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def binarygap(u):
    """maximal sequence of consecutive zeros
    >>> binarygap(6)
    1

    >>> binarygap(9)
    2

    >>> binarygap(129)
    6
    """
    s = format(u, 'b').split('1')
    return 0 if len(s) < 3 else len(max(s))


class BaseDepiction(object):
    """BaseDepiction

    >>> BaseDepiction((0, u'd'), True, "bin", "basic", False, True)
    +-------+--------+--------+---+---+---+---+---+---+---+---+
    | input | ffs_u8 | nlz_u8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    +-------+--------+--------+---+---+---+---+---+---+---+---+

    >>> BaseDepiction((182, u'd'), True, "bin", "basic", False, True)
    +-------+--------+--------+---+---+---+---+---+---+---+---+
    | input | ffs_u8 | nlz_u8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    +-------+--------+--------+---+---+---+---+---+---+---+---+

    >>> BaseDepiction((256, u'd'), True, "bin", "basic", False, True)
    +-------+---------+---------+----+----+----+----+----+----+---+---+---+---+---+---+---+---+---+---+
    | input | ffs_u16 | nlz_u16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    +-------+---------+---------+----+----+----+----+----+----+---+---+---+---+---+---+---+---+---+---+

    >>> BaseDepiction((2, u'd'), True, "bin", "noline", False, True)
    <BLANKLINE>

    >>> BaseDepiction((2, u'd'), True, "bin", "gfm", False, True)
    | input | ffs_u8 | nlz_u8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |

    >>> BaseDepiction((2, u'd'), True, "bin", "nohrules", False, True)
    | input | ffs_u8 | nlz_u8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |

    >>> BaseDepiction((32, u'd'), True, "bin", "basic", True, True)
    +-------+--------+--------+---+---+---+---+---+---+
    | input | ffs_u8 | nlz_u8 | 5 | 4 | 3 | 2 | 1 | 0 |
    +-------+--------+--------+---+---+---+---+---+---+

    >>> BaseDepiction((1, u'x'), False, "bin", "basic", False, True)
    +-----------+-------+--------+--------+---+---+---+---+---+---+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    +-----------+-------+--------+--------+---+---+---+---+---+---+---+---+

    >>> BaseDepiction((15, u'x'), False, "bin", "basic", True, True)
    +-----------+-------+--------+--------+---+---+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 3 | 2 | 1 | 0 |
    +-----------+-------+--------+--------+---+---+---+---+

    >>> BaseDepiction((15, u'x'), False, "hex", "basic", False, True)
    +-----------+-------+--------+--------+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 4 | 0 |
    +-----------+-------+--------+--------+---+---+

    >>> BaseDepiction((15, u'b'), False, "bin", "basic", True, True)
    +-----------+-------+--------+--------+---+---+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 3 | 2 | 1 | 0 |
    +-----------+-------+--------+--------+---+---+---+---+

    >>> BaseDepiction((31, u'b'), False, "hex", "basic", True, True)
    +-----------+-------+--------+--------+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 4 | 0 |
    +-----------+-------+--------+--------+---+---+

    >>> BaseDepiction((31, u'b'), False, "oct", "basic", True, True)
    +-----------+-------+--------+--------+---+---+
    | value dec | input | ffs_u8 | nlz_u8 | 3 | 0 |
    +-----------+-------+--------+--------+---+---+

    >>> BaseDepiction((8, u'd'), True, "oct", "basic", False, True)
    +-------+--------+--------+---+---+---+
    | input | ffs_u8 | nlz_u8 | 6 | 3 | 0 |
    +-------+--------+--------+---+---+---+
    """

    def __init__(self, x, alldecimal, type_rep="bin", outformat="basic", short_repr=False, header=True):
        super(BaseDepiction, self).__init__()
        self.table = pt.PrettyTable()
        self.x, self.base = x
        self.power = dict(hex=4, oct=3).get(type_rep, 1)
        self.outformat = outformat
        self.table.header = header
        self.table.hrules = pt.ALL
        if self.outformat == "gfm":
            self.table.junction_char = "|"
        elif self.outformat == "nohrules":
            self.table.hrules = pt.NONE
        elif self.outformat == "noline":
            self.table.border = False
            self.table.hrules = pt.NONE
            self.outformat = {"border": False,
                              "header": True,
                              "junction_char": "+",
                              "hrules": pt.NONE}
        if self.x:
            for deep in filter(lambda e: int(log(self.x, 2)) < e, [8, 16, 32, 64, 128]):
                self.depth = deep - 1
                break
        else:
            self.depth = 7
        if self.power == 4:
            self.x = format(self.x, 'x')
        elif self.power == 3:
            self.x = format(self.x, 'o')
        else:
            self.x = format(self.x, 'b')

        if not short_repr:
            self.x = int((self.depth / self.power - len(self.x) + 1)) * "0" + self.x
        if sys.byteorder == "little":
            nbbits = [i * self.power for i in range(len(self.x) - 1, -1, -1)]
        else:
            nbbits = [i * self.power for i in range(len(self.x))]
        self.position = list(map(str, nbbits))
        self.x = list(self.x)
        nlz = self.depth - int(log(x[0], 2)) if x[0] else 8
        ffs = self.depth - nlz
        # self.position.insert(0, "binarygap")
        # self.x.insert(0, binarygap(x[0]))
        self.position.insert(0, "nlz_u" + str(self.depth + 1))
        self.x.insert(0, nlz)
        self.position.insert(0, "ffs_u" + str(self.depth + 1))
        self.x.insert(0, ffs)
        self.position.insert(0, "input")
        self.x.insert(0, self.base + format(x[0], self.base))
        if not alldecimal:
            self.position.insert(0, "value dec")
            self.x.insert(0, format(x[0], 'd'))
        self.table.field_names = self.position

    def __repr__(self):
        sout = self.table.get_string()
        if self.outformat == "gfm":  # don't know how to set for gfm format
            sout = sout.split("\n")
            sout = "\n".join(sout[1:-1])
        return sout

    def __add__(self, other):
        if other.depth != self.depth:
            pad = len(self.x) - len(other.x)
            other.x[2] += (self.depth - other.depth)  # update value of nlz
            while pad > 0:
                other.x.insert(4, "0")  # first column contains values, 2nd nlz
                pad -= 1
        self.table.add_row(other.x)
        return self.table.get_string()

    def add_row(self):
        """add a new row"""
        self.table.add_row(self.x)


def convert(x):
    """
    >>> convert('0x10')
    (16, 'x')
    >>> convert('0b10')
    (2, 'b')
    >>> convert('0o7')
    (7, 'o')
    >>> convert('10')
    (10, 'd')
    >>> convert('0b11 & 0b10'), convert('0b11 | 0b10'), convert('0b11 ^ 0b10')
    ((2, 'b'), (3, 'b'), (1, 'b'))
    >>> convert('11 & 10'), convert('11 | 10'), convert('11 ^ 10')
    ((10, 'd'), (11, 'd'), (1, 'd'))
    """
    if x.startswith('0x'):
        return (eval(x), 'x')
    elif x.startswith('0b'):
        return (eval(x), 'b')
    elif x.startswith('0o'):
        return (eval(x), 'o')
    else:
        return (eval(x), 'd')


@click.command(context_settings=CONTEXT_SETTINGS,
               help="""representation of a number in binary, hexadecimal or oct according to your
               system byteorder""")
@click.option("-t", "--type_repr",
              default="bin",
              type=click.Choice(['bin', 'hex', 'oct']),
              help="type of representation of number, binary by default")
@click.option("-f", "--outformat",
              default="basic",
              type=click.Choice(['noline', 'gfm', 'basic', 'nohrules']),
              help="outpout format representation. basic by default")
@click.option("-s", "--short", count=True, help="short representation")
@click.argument("value", nargs=-1, type=click.STRING)
def binaryrepr(value, type_repr, outformat, short):
    """
    display number in binary, hexadecimal or oct in a human readable view
    """
    if not value:
        sys.exit(0)
    values = list(map(convert, value))
    alldecimal = all(y == 'd' for x, y in values)
    maxv = max(values, key=itemgetter(0))
    if len(values) > 1:
        short = False
    master = BaseDepiction(maxv, alldecimal, type_repr, outformat, short)
    for val in values:
        base = BaseDepiction(val, alldecimal, type_repr, outformat, short, header=False)
        master + base
    print(master)


if __name__ == "__main__":
    binaryrepr()

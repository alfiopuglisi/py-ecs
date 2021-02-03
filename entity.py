#!/usr/bin/env python

import itertools

_counter = itertools.count()

def new():
    return next(_counter)


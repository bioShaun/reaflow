#!/usr/bin/env python3

''' reaflow config file
'''

import pkg_resources

# load expression base functions
base_func = dict()
for entry_point in pkg_resources.iter_entry_points('ExpBase'):
    base_func.update({entry_point.name: entry_point.load()})
